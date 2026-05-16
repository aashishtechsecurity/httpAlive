#!/usr/bin/python3

import asyncio
import random
import argparse
import sys
import time
from datetime import datetime
import re
from typing import List, Optional, Set

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

VERSION = "v1.1.0"

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
    url = "https://api.github.com/repos/aashishsec/httpAlive/releases/latest"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                latest = data.get('name', '')
                if latest == VERSION:
                    console.print(f"[info]●[/info] [bold white]Status:[/bold white] [success]Up to date ({VERSION})[/success]")
                else:
                    console.print(f"[info]●[/info] [bold white]Status:[/bold white] [warning]Update available: {latest}[/warning]")
    except Exception:
        pass

def extract_title(html: str) -> str:
    """Extract page title using regex to avoid heavy dependencies."""
    match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if match:
        title = match.group(1).strip()
        return (title[:50] + '...') if len(title) > 50 else title
    return "N/A"

async def probe_url(
    url: str, 
    client: httpx.AsyncClient, 
    output_file: Optional[str], 
    progress, 
    task_id,
    filter_status: Optional[Set[int]] = None,
    hide_status: Optional[Set[int]] = None
) -> None:
    # Ensure URL has protocol
    target = url if url.startswith(('http://', 'https://')) else f"http://{url}"
    
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
    try:
        # We don't follow redirects here so we can see the hop info, 
        # but for simplicity in "is it alive", following is fine.
        # Let's track redirects if they happen.
        response = await client.get(target, headers=headers, follow_redirects=True)
        status = response.status_code
        
        # Filtering logic
        if filter_status and status not in filter_status:
            return
        if hide_status and status in hide_status:
            return

        size = response.headers.get('Content-Length', len(response.content))
        server = response.headers.get('Server', 'N/A')
        title = extract_title(response.text)
        
        # Track if it was a redirect
        redirect_info = ""
        if len(response.history) > 0:
            final_url = str(response.url)
            redirect_info = f" [yellow]→[/][italic white] {final_url}[/]"

        # Color coding status codes
        status_style = "status_200" if 200 <= status < 300 else "status_300" if 300 <= status < 400 else "status_400"
        
        result_text = f"[{status_style}](Status: {status})[/] --[Size: {size}]--[Server: {server}]--[Title: {title}]---> [url]{url}[/url]{redirect_info}"
        console.print(result_text)
        
        if output_file:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"(Status: {status}) --[Size: {size}]--[Server: {server}]--[Title: {title}]---> {url}{' -> ' + str(response.url) if redirect_info else ''}\n")
                
    except (httpx.TimeoutException, httpx.ConnectError):
        pass 
    except Exception as e:
        # Uncomment for debugging: console.print(f"[error]Error probing {url}: {str(e)}[/error]")
        pass
    finally:
        progress.update(task_id, advance=1)

async def main():
    parser = argparse.ArgumentParser(description="httpAlive: Efficiently probe for alive subdomains and URLs.")
    parser.add_argument('-l', '--list', required=True, help="File containing list of subdomains or URLs.")
    parser.add_argument('-o', '--output', default="httpAlive_output.txt", help="File to save results.")
    parser.add_argument('-c', '--concurrency', type=int, default=50, help="Concurrency level (default: 50).")
    parser.add_argument('-t', '--timeout', type=int, default=10, help="Timeout per request (default: 10s).")
    parser.add_argument('-mc', '--match-code', help="Match specific status codes (e.g., 200,301).")
    parser.add_argument('-hc', '--hide-code', help="Hide specific status codes (e.g., 404,403).")
    
    args = parser.parse_args()

    # Parse status codes
    filter_status = set(int(c.strip()) for c in args.match_code.split(',')) if args.match_code else None
    hide_status = set(int(c.strip()) for c in args.hide_code.split(',')) if args.hide_code else None

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

    # Clear output file if it exists or create new
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# httpAlive Scan - {datetime.now()}\n")

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
            
            # Using semaphore to control concurrency
            semaphore = asyncio.Semaphore(args.concurrency)
            
            async def bounded_probe(url):
                async with semaphore:
                    await probe_url(url, client, args.output, progress, task_id, filter_status, hide_status)
            
            tasks = [bounded_probe(url) for url in urls]
            await asyncio.gather(*tasks)

    console.print("-" * 60)
    console.print(f"[bold success][+][/bold success] Scan complete. Results saved to: [bold white]{args.output}[/bold white]")
    console.print(f"[bold success][+][/bold success] Finished at: [bold white]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold white]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Interrupted by user. Exiting...[/bold red]")
        sys.exit(0)
