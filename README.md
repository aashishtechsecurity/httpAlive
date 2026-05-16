# httpAlive v2.0.0 🚀

**httpAlive** is a high-performance, asynchronous web reconnaissance tool designed for security researchers and bug bounty hunters. It efficiently probes lists of subdomains and URLs to identify alive targets, extract metadata, fingerprint technology stacks, and detect WAF protection.

---

![GitHub last commit](https://img.shields.io/github/last-commit/aashishtechsecurity/httpAlive) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/aashishtechsecurity/httpAlive) [![GitHub license](https://img.shields.io/github/license/aashishtechsecurity/httpAlive)](https://github.com/aashishtechsecurity/httpAlive/blob/main/LICENSE) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/aashishsec/)

## 🛠️ Key Features

- **Blazing Fast**: Powered by `asyncio` and `httpx` for extreme concurrency.
- **Memory Efficient**: Uses a producer-consumer worker pool to handle millions of targets with negligible RAM usage.
- **Tech Fingerprinting**: Detects CMS (WordPress, Drupal), Frameworks (React, Next.js), and Web Servers.
- **WAF Detection**: Identifies protection layers like **Cloudflare**, **Akamai**, **AWS WAF**, **Imperva**, and more.
- **Asynchronous DNS**: Resolves IP addresses concurrently with HTTP probing.
- **Flexible Piping**: Seamlessly integrates into your existing recon pipeline via `stdin`.
- **Professional Exports**: Multi-format support for **Text**, **JSON (Line-delimited)**, and **CSV**.
- **Real-time Dashboard**: Live-updating UI with progress bars and statistics using `rich`.

---

## 🏗️ Architecture: The Async Worker Pool

Unlike traditional multi-threaded tools that suffer from high context-switching overhead, **httpAlive** uses a single-threaded event loop with an asynchronous worker pool:

1.  **Queue System**: URLs are fed into an `asyncio.Queue` (either from a file or `stdin`).
2.  **Worker Pool**: A set number of workers (default: 50) pull from the queue and perform non-blocking I/O.
3.  **Connection Pooling**: Reuses TCP connections via `httpx.Limits` to maximize speed and minimize socket exhaustion.

---

## 🚀 Installation

### Using Git (Recommended for Developers)
```bash
git clone https://github.com/aashishtechsecurity/httpAlive.git
cd httpAlive
pip install -r requirements.txt
```

### Global Installation
You can install it globally to use the `httpAlive` command anywhere:
```bash
pip install .
```

---

## 📖 Usage Guide

### 1. Basic Usage
Read from a file and save to default `httpAlive_output.txt`:
```bash
python httpAlive.py -l subdomains.txt
```

### 2. Piping (The Bug Bounty Workflow)
Integrate with other tools like `subfinder` or `assetfinder`:
```bash
subfinder -d example.com -silent | python httpAlive.py -mc 200 -j alive.json
```

### 3. Advanced Filtering
Match specific status codes and exclude others:
```bash
# Only find 200 OK and 302 Redirects, ignore 404s
python httpAlive.py -l targets.txt -mc 200,302 -hc 404
```

### 4. Custom Headers & Auth
```bash
python httpAlive.py -l list.txt -H "Cookie: session=xyz" -H "User-Agent: MyCustomScanner"
```

---

## 📊 Output Formats

### JSON Output (`-j results.json`)
Results are saved as line-delimited JSON (JSONL) for easy parsing with `jq`:
```json
{"url": "example.com", "ip": "93.184.216.34", "status": 200, "size": 1256, "server": "ECS", "title": "Example Domain", "tech": ["Nginx"], "final_url": "https://example.com/"}
```

### CSV Output (`--csv results.csv`)
Standard CSV structure for spreadsheet analysis:
`URL, IP Address, Status, Size, Server, Title, Tech, Final URL`

---

## 🔍 Technology & WAF Signatures
The tool currently fingerprints:
- **WAFs**: Cloudflare, Akamai, AWS WAF, Imperva, Sucuri, F5 BigIP.
- **CMS**: WordPress, Shopify, Drupal, Joomla.
- **Frameworks**: React, Angular, Vue.js, Next.js, Nuxt.js, Laravel.
- **Servers**: Nginx, Apache, IIS, LiteSpeed.

---

## ⚙️ Configuration Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-l, --list` | Input file (use `-` or omit for stdin) | `None` |
| `-c, --concurrency` | Number of concurrent workers | `50` |
| `-o, --output` | Text output file | `httpAlive_output.txt` |
| `-j, --json` | JSON output file (JSONL format) | `None` |
| `--csv` | CSV output file | `None` |
| `-mc, --match-code` | List of status codes to match (e.g. 200,302) | `All` |
| `-hc, --hide-code` | List of status codes to hide | `None` |
| `-H, --header` | Custom header (can be repeated) | `None` |
| `-t, --timeout` | Request timeout in seconds | `10` |

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.

## 🤝 Contributing
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
**Author**: [Bande Aashish](https://github.com/aashishtechsecurity)  
**Support**: If you find this tool useful, give it a ⭐ on GitHub!

