# httpAlive v2.0.0 🚀

**httpAlive** is a high-performance, asynchronous web reconnaissance tool designed for security researchers and bug bounty hunters. It efficiently probes lists of subdomains and URLs to identify alive targets, extract metadata, and fingerprint technology stacks.

---

![GitHub last commit](https://img.shields.io/github/last-commit/aashishtechsecurity/httpAlive) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/aashishtechsecurity/httpAlive) [![GitHub license](https://img.shields.io/github/license/aashishtechsecurity/httpAlive)](https://github.com/aashishtechsecurity/httpAlive/blob/main/LICENSE) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/aashishsec/)

## 🛠️ Key Features

- **Blazing Fast**: Built on `asyncio` and `httpx` for high-concurrency probing.
- **Memory Efficient**: Uses a worker-pool architecture to handle millions of URLs with minimal RAM usage.
- **Tech Fingerprinting**: Automatically detects CMS (WordPress, Drupal), Frameworks (React, Next.js), and Web Servers.
- **Rich Metadata**: Extracts HTML Page Titles, resolves **IP Addresses**, and follows redirects.
- **WAF Detection**: Identifies if a target is protected by Cloudflare, Akamai, AWS WAF, and more.
- **Flexible Filtering**: Match or hide specific HTTP status codes (e.g., `-mc 200` or `-hc 404`).
- **Professional Exports**: Save results in **Text**, **JSON**, or **CSV** formats.
- **Custom Headers**: Pass custom cookies or authorization tokens via the `-H` flag.

---

## 🏗️ Architecture & How It Works

### Asynchronous Worker Pool (Senior Design)
Unlike traditional tools that create a thread for every URL, **httpAlive** utilizes a **Producer-Consumer pattern**:

1.  **Producer**: Reads URLs from your input file line-by-line and feeds them into an `asyncio.Queue`.
2.  **Worker Pool**: A fixed number of asynchronous workers (controlled by `--concurrency`) pull URLs from the queue.
3.  **Connection Pooling**: Uses `httpx.AsyncClient` with custom limits to reuse TCP connections, reducing overhead and avoiding socket exhaustion.

This architecture ensures that the tool remains responsive and stable even when scanning massive datasets.

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
git clone https://github.com/aashishtechsecurity/httpAlive.git
cd httpAlive
pip install -r requirements.txt
```

---

## 📖 Usage Guide

### Basic Probing
```bash
python ./httpAlive/httpAlive.py -l subdomains.txt
```

### Advanced Filtering & Export
Find only valid pages (200 OK) and save to JSON and CSV:
```bash
python ./httpAlive/httpAlive.py -l list.txt -mc 200 -j results.json --csv results.csv
```

### Authenticated Scanning (Custom Headers)
```bash
python ./httpAlive/httpAlive.py -l list.txt -H "Cookie: session=123" -H "X-Forwarded-For: 127.0.0.1"
```

### Full Options
| Flag | Description | Default |
|------|-------------|---------|
| `-l, --list` | File containing list of URLs | **Required** |
| `-c, --concurrency` | Number of concurrent workers | `50` |
| `-o, --output` | Text output file | `httpAlive_output.txt` |
| `-j, --json` | JSON output file | `None` |
| `--csv` | CSV output file | `None` |
| `-mc, --match-code` | Match specific status codes | `All` |
| `-hc, --hide-code` | Hide specific status codes | `None` |
| `-H, --header` | Add custom header (can use multiple) | `None` |
| `-t, --timeout` | Request timeout in seconds | `10` |

---

## 🔍 Technology & WAF Detection
The tool identifies stacks and protection layers using:
- **WAFs**: Cloudflare, Akamai, AWS WAF, Imperva, Sucuri, F5 BigIP.
- **CMS**: WordPress, Shopify, Drupal, Joomla.
- **Frameworks**: React, Angular, Vue.js, Next.js, Nuxt.js.
- **Infrastructure**: Nginx, Apache, IIS, LiteSpeed.

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
**Author**: [Bande Aashish](https://github.com/aashishtechsecurity)
