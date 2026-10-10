# TBH-Recon

<p align="center">
  <a href="https://github.com/TulungagungBlackHat/TBH-Recon/actions/workflows/ci.yml"><img src="https://github.com/TulungagungBlackHat/TBH-Recon/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-red.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Termux%20%7C%20Linux%20%7C%20Kali-000000.svg" alt="Platform">
</p>

Single-file web reconnaissance for bug bounty engagements. Headers, SSL, ports, and subdomains in one pass — with JSON and HTML reports ready to attach to a submission.

Part of the [Tulungagung Black Hat](https://github.com/TulungagungBlackHat) toolset.

## Features

- **Security header audit** — flags missing HSTS, CSP, X-Frame-Options, and friends
- **SSL certificate check** — issuer, expiry, SANs
- **Port scan** — top ports with banner hints
- **Subdomain enumeration** — passive wordlist expansion with liveness check
- **Reports** — `--json` for tooling pipelines, `--html` for reports you can send to a program
- **Zero dependencies beyond `requests`** — runs on a stock Termux install

## Install

```bash
git clone https://github.com/TulungagungBlackHat/TBH-Recon
cd TBH-Recon
pip install -r requirements.txt
```

Or install the whole TBH toolset with [TBH-Toolkit](https://github.com/TulungagungBlackHat/TBH-Toolkit):

```bash
curl -sSL https://raw.githubusercontent.com/TulungagungBlackHat/TBH-Toolkit/main/install.sh | bash
```

## Usage

```bash
python3 main.py --help
```

```
usage: main.py [-h] -u URL [--ssl] [-p] [-s] [--json JSON] [--html HTML]

options:
  -u, --url URL       Target URL
  --ssl               SSL check
  -p, --ports         Port scan
  -s, --subdomain     Subdomain enumeration
  --json JSON         Save JSON report
  --html HTML         Save HTML report
```

### Examples

Full recon with both report formats:

```bash
python3 main.py -u https://example.com --ssl --ports --subdomain \
  --json report.json --html report.html
```

Headers only (fastest):

```bash
python3 main.py -u https://example.com
```

## Sample Output

```
[*] example.com (93.184.216.34)
[+] Status 200 | Missing: strict-transport-security, content-security-policy
[+] SSL: valid, expires 2027-01-15
[+] Ports: 80/http, 443/https
[+] Subdomains: www.example.com, mail.example.com
[✓] JSON saved: report.json
[✓] HTML saved: report.html
```

## Authorized Use Only

Run this against domains you own or have explicit written permission to test. Reconnaissance without authorization is illegal in most jurisdictions. See [SECURITY.md](SECURITY.md) for responsible disclosure of bugs in TBH itself.

## Related Tools

- [TBH-AllScan](https://github.com/TulungagungBlackHat/TBH-AllScan) — 10-in-one scanner with risk scoring
- [TBH-SubFinder](https://github.com/TulungagungBlackHat/TBH-SubFinder) — deeper subdomain enum + takeover checks
- [TBH-BugBounty](https://github.com/TulungagungBlackHat/TBH-BugBounty) — hunter workflow toolkit

## License

[MIT](LICENSE) — Tulungagung Black Hat, East Java, Indonesia. Always Smile :)
