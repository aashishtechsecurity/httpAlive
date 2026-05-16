#!/usr/bin/python3

import asyncio
import random
import argparse
import sys
import time
import csv
import socket
from datetime import datetime
import re
import json
from typing import List, Optional, Set, Dict

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn, TimeElapsedColumn
from rich.theme import Theme
from rich.table import Table

# Custom Theme for Security Tooling
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "status_200": "bold green",
    "status_300": "bold yellow",
    "status_400": "bold red",
    "status_500": "bold magenta",
    "url": "underline blue",
})

console = Console(theme=custom_theme)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]

VERSION = "1.1.0" # Removed 'v' prefix for easier comparison

def get_banner():
    banner_text = f"""
[bold cyan]██╗░░██╗████████╗████████╗██████╗░░░░░░░░█████╗░██╗░░░░░██╗██╗░░░██╗███████╗[/bold cyan]
[bold cyan]██║░░██║╚══██╔══╝╚══██╔══╝██╔══██╗░░░░░░██╔══██╗██║░░░░░██║██║░░░██║██╔════╝[/bold cyan]
[bold cyan]███████║░░░██║░░░░░░██║░░░██████╔╝█████╗███████║██║░░░░░██║╚██╗░██╔╝█████╗░░[/bold cyan]
[bold cyan]██╔══██║░░░██║░░░░░░██║░░░██╔═══╝░╚════╝██╔══██║██║░░░░░██║░╚████╔╝░██╔══╝░░[/bold cyan]
[bold cyan]██║░░██║░░░██║░░░░░░██║░░░██║░░░░░░░░░░░██║░░██║███████╗██║░░╚██╔╝░░███████╗[/bold cyan]
[bold cyan]╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚═╝░░░░░░░░░░░╚═╝░░╚═╝╚══════╝╚═╝░░░╚═╝░░░╚══════╝[/bold cyan]
                                                                        
[bold yellow]Author   :[/bold yellow] [bold white]Bande Aashish💕[/bold white]
[bold yellow]Github   :[/bold yellow] [blue]https://github.com/aashishtechsecurity[/blue]
[bold yellow]Version  :[/bold yellow] [bold green]{VERSION}[/bold green]
    """
    return Panel(banner_text, border_style="cyan", expand=False)

async def check_version():
    url = "https://api.github.com/repos/aashishtechsecurity/httpAlive/releases/latest"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                latest = data.get('tag_name', '').lstrip('v')
                
                # Basic semantic versioning check
                curr_v = [int(x) for x in VERSION.split('.')]
                late_v = [int(x) for x in latest.split('.')]
                
                if late_v > curr_v:
                    console.print(f"[info]●[/info] [bold white]Status:[/bold white] [warning]Update available: v{latest}[/warning]")
                else:
                    console.print(f"[info]●[/info] [bold white]Status:[/bold white] [success]Up to date (v{VERSION})[/success]")
    except Exception:
        pass

def extract_title(html: str) -> str:
    """Extract page title using regex to avoid heavy dependencies."""
    match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if match:
        title = match.group(1).strip()
        # Clean up some common issues like double spaces or newlines in title
        title = " ".join(title.split())
        return (title[:50] + '...') if len(title) > 50 else title
    return "N/A"

def detect_tech(response: httpx.Response) -> List[str]:
    """Extensible fingerprinting using signatures."""
    detected = []
    headers = response.headers
    html = response.text.lower()
    cookies = str(response.cookies).lower()
    
    signatures = {
        "Nginx": {"header": ("Server", "nginx")},
        "Apache": {"header": ("Server", "apache")},
        "LiteSpeed": {"header": ("Server", "litespeed")},
        "IIS": {"header": ("Server", "microsoft-iis")},
        "Cloudflare": {"header": ("Server", "cloudflare")},
        "PHP": {"header": ("X-Powered-By", "php"), "cookie": "phpsessid"},
        "ASP.NET": {"header": ("X-Powered-By", "asp.net")},
        "Express.js": {"header": ("X-Powered-By", "express")},
        "WordPress": {"body": "wp-content"},
        "Drupal": {"body": "drupal", "header": ("X-Generator", "drupal")},
        "Joomla": {"body": "joomla"},
        "Shopify": {"body": "shopify"},
        "Next.js": {"body": "_next/static"},
        "Nuxt.js": {"body": "nuxt"},
        "React": {"body": "react"},
        "Angular": {"body": "angular"},
        "Vue.js": {"body": "vue"},
        "Laravel": {"cookie": "laravel_session"},
        "Java/JSP": {"cookie": "jsessionid"},
        # WAF Signatures
        "WAF:Cloudflare": {"header": ("cf-ray", "")},
        "WAF:Akamai": {"header": ("x-akamai-transformed", "")},
        "WAF:Imperva": {"header": ("x-iinfo", ""), "cookie": "visid_incap"},
        "WAF:Sucuri": {"header": ("x-sucuri-id", "")},
        "WAF:AWS-WAF": {"header": ("x-amz-cf-id", "")},
        "WAF:F5-BigIP": {"header": ("x-wa-info", ""), "cookie": "bigipserver"},
    }

    for tech, sig in signatures.items():
        if "header" in sig:
            h_key, h_val = sig["header"]
            if h_key in headers:
                if not h_val or h_val in headers.get(h_key, '').lower():
                    detected.append(tech)
        if "body" in sig and sig["body"] in html:
            detected.append(tech)
        if "cookie" in sig and sig["cookie"] in cookies:
            detected.append(tech)
    
    return sorted(list(set(detected)))

async def get_ip(hostname: str) -> str:
    """Resolve hostname to IP address asynchronously."""
    try:
        # Extract hostname if URL is passed
        if "://" in hostname:
            hostname = hostname.split("://")[1].split("/")[0].split(":")[0]
        
        loop = asyncio.get_event_loop()
        info = await loop.getaddrinfo(hostname, None, family=socket.AF_INET)
        if info:
            return info[0][4][0]
    except Exception:
        pass
    return "N/A"

async def probe_url(
    url: str, 
    client: httpx.AsyncClient, 
    output_file: Optional[str], 
    json_output: Optional[str],
    csv_output: Optional[str],
    progress, 
    task_id,
    filter_status: Optional[Set[int]] = None,
    hide_status: Optional[Set[int]] = None,
    custom_headers: Optional[Dict[str, str]] = None
) -> None:
    target = url if url.startswith(('http://', 'https://')) else f"http://{url}"
    
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    if custom_headers:
        headers.update(custom_headers)
    
    try:
        ip_address = await get_ip(url)
        response = await client.get(target, headers=headers, follow_redirects=True)
        status = response.status_code
        
        if filter_status and status not in filter_status: return
        if hide_status and status in hide_status: return

        size = response.headers.get('Content-Length', len(response.content))
        server = response.headers.get('Server', 'N/A')
        title = extract_title(response.text)
        tech = detect_tech(response)
        
        # Color coding tech vs WAF
        tech_display = []
        for t in tech:
            if t.startswith("WAF:"):
                tech_display.append(f"[bold red]{t}[/]")
            else:
                tech_display.append(f"[bold magenta]{t}[/]")
        
        tech_str = f"[{','.join(tech_display)}]" if tech_display else ""
        
        redirect_info = ""
        if len(response.history) > 0:
            redirect_info = f" [yellow]→[/][italic white] {str(response.url)}[/]"

        status_style = "status_200" if 200 <= status < 300 else "status_300" if 300 <= status < 400 else "status_400"
        
        result_text = f"[{status_style}](Status: {status})[/] --[IP: {ip_address}]--[Size: {size}]--[Server: {server}]--[Title: {title}] {tech_str}---> [url]{url}[/url]{redirect_info}"
        console.print(result_text)
        
        # Save to Text
        if output_file:
            with open(output_file, 'a', encoding='utf-8') as f:
                tech_log = f"[{','.join(tech)}]" if tech else ""
                f.write(f"(Status: {status}) --[IP: {ip_address}]--[Size: {size}]--[Server: {server}]--[Title: {title}] {tech_log}---> {url}{' -> ' + str(response.url) if redirect_info else ''}\n")
        
        # Save to JSON
        if json_output:
            result_data = {
                "url": url,
                "ip": ip_address,
                "status": status,
                "size": size,
                "server": server,
                "title": title,
                "tech": tech,
                "final_url": str(response.url) if redirect_info else url
            }
            with open(json_output, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result_data) + "\n")
        
        # Save to CSV
        if csv_output:
            with open(csv_output, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([url, ip_address, status, size, server, title, ",".join(tech), str(response.url)])
                
    except Exception:
        pass
    finally:
        progress.update(task_id, advance=1)

async def worker(queue, client, args, progress, task_id, filter_status, hide_status, custom_headers):
    """Worker task that processes URLs from the queue."""
    while True:
        url = await queue.get()
        try:
            await probe_url(url, client, args.output, args.json, args.csv, progress, task_id, filter_status, hide_status, custom_headers)
        finally:
            queue.task_done()

async def main():
    parser = argparse.ArgumentParser(description="httpAlive: Efficiently probe for alive subdomains and URLs.")
    parser.add_argument('-l', '--list', required=True, help="File containing list of subdomains or URLs.")
    parser.add_argument('-o', '--output', default="httpAlive_output.txt", help="File to save text results.")
    parser.add_argument('-j', '--json', help="File to save JSON results.")
    parser.add_argument('--csv', help="File to save CSV results.")
    parser.add_argument('-c', '--concurrency', type=int, default=50, help="Concurrency level (default: 50).")
    parser.add_argument('-t', '--timeout', type=int, default=10, help="Timeout per request (default: 10s).")
    parser.add_argument('-mc', '--match-code', help="Match specific status codes (e.g., 200,301).")
    parser.add_argument('-hc', '--hide-code', help="Hide specific status codes (e.g., 404,403).")
    parser.add_argument('-H', '--header', action='append', help="Custom header (e.g., 'Cookie: session=123'). Can be used multiple times.")
    
    args = parser.parse_args()

    # Parse status codes
    filter_status = set(int(c.strip()) for c in args.match_code.split(',')) if args.match_code else None
    hide_status = set(int(c.strip()) for c in args.hide_code.split(',')) if args.hide_code else None

    # Parse custom headers
    custom_headers = {}
    if args.header:
        for h in args.header:
            if ':' in h:
                key, val = h.split(':', 1)
                custom_headers[key.strip()] = val.strip()

    console.print(get_banner())
    await check_version()
    
    try:
        with open(args.list, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print(f"[error]Error: File '{args.list}' not found.[/error]")
        sys.exit(1)

    console.print(f"\n[bold info][*][/bold info] Starting at: [bold white]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold white]")
    console.print(f"[bold info][*][/bold info] Target count: [bold yellow]{len(urls)}[/bold yellow]")
    console.print(f"[bold info][*][/bold info] Concurrency : [bold yellow]{args.concurrency}[/bold yellow]\n")
    console.print("-" * 60)

    # Clear output files
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# httpAlive Scan - {datetime.now()}\n")
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            pass
    if args.csv:
        with open(args.csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "IP Address", "Status", "Size", "Server", "Title", "Tech", "Final URL"])

    limits = httpx.Limits(max_keepalive_connections=20, max_connections=args.concurrency)
    
    async with httpx.AsyncClient(verify=False, timeout=args.timeout, limits=limits) as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            console=console,
            expand=True
        ) as progress:
            
            task_id = progress.add_task("[cyan]Probing URLs...", total=len(urls))
            
            queue = asyncio.Queue()
            for url in urls:
                queue.put_nowait(url)
            
            # Start workers
            workers = [
                asyncio.create_task(worker(queue, client, args, progress, task_id, filter_status, hide_status, custom_headers))
                for _ in range(args.concurrency)
            ]
            
            await queue.join()
            for w in workers:
                w.cancel()

    console.print("-" * 60)
    output_msg = f"[bold success][+][/bold success] Scan complete."
    if args.output: output_msg += f" Text: [bold white]{args.output}[/bold white]"
    if args.json: output_msg += f" JSON: [bold white]{args.json}[/bold white]"
    if args.csv: output_msg += f" CSV: [bold white]{args.csv}[/bold white]"
    console.print(output_msg)
    console.print(f"[bold success][+][/bold success] Finished at: [bold white]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold white]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Interrupted by user. Exiting...[/bold red]")
        sys.exit(0)
