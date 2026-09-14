# TBH-Recon - Web Reconnaissance Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Purpose-Bug%20Bounty%20%7C%20Educational-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
  <img src="https://img.shields.io/github/stars/TulungagungBlackHat/TBH-Recon?style=social">
</p>

> **⚠️ FOR EDUCATIONAL & AUTHORIZED TESTING ONLY**
> Tool ini untuk **Bug Bounty, Penetration Testing dengan izin, dan pembelajaran Cyber Security**. Jangan gunakan pada target tanpa izin tertulis. Developer tidak bertanggung jawab atas penyalahgunaan.

Oleh **Tulungagung Black Hat** - *Always Smile :)* | Tulungagung, Jawa Timur

---

### ✨ Features

- 🔍 **HTTP Header Analysis** - Deteksi missing security headers (HSTS, CSP, X-Frame-Options)
- 🚪 **Port Scanner** - Scan port umum (21,22,80,443,3306,8080,8443) + banner
- 🌐 **Subdomain Enumeration** - Cek subdomain umum secara pasif
- ⚡ **Lightweight** - Hanya butuh `requests`, jalan di Termux/Kali/Linux
- 📊 **Colored Output** - Mudah dibaca untuk report

### 📦 Installation

**Termux / Kali / Linux:**
```bash
pkg update && git clone https://github.com/TulungagungBlackHat/TBH-Recon
cd TBH-Recon
pip install -r requirements.txt
```

### 🚀 Usage

```bash
# Basic header analysis
python3 main.py -u https://example.com

# Dengan port scan
python3 main.py -u https://example.com --ports

# Dengan subdomain check
python3 main.py -u https://example.com --subdomain

# Full recon (recommended untuk bug bounty)
python3 main.py -u https://example.com --ports --subdomain
```

**Contoh output:**
```
[*] Target: example.com (93.184.216.34)
[+] Status: 200 | Server: ECS
[+] Headers:
  Strict-Transport-Security: max-age=315...
[!] Missing Security Headers: Content-Security-Policy
[OPEN] 80/http
[OPEN] 443/https
```

### 🛡️ Untuk Bug Bounty Hunter

1. Cari target dengan header yang missing (CSPR, HSTS) -> potensi low/medium finding
2. Port terbuka yang tidak perlu (misal 3306 MySQL) -> info disclosure
3. Subdomain yang terlupakan -> takeover & recon lebih dalam

> Selalu baca `scope` program bug bounty sebelum scan!

### 📚 Learning Path

Tool ini cocok untuk pemula yang mau belajar:
- OWASP Top 10 (Security Misconfiguration)
- Reconnaissance phase di Penetration Testing
- Python untuk Cyber Security

### 👥 Credits

- Team: [Tulungagung Black Hat](https://github.com/TulungagungBlackHat)
- Location: Tulungagung, Jawa Timur, Indonesia
- Tagline: Always Smile :)

### 📄 License

MIT License - Bebas untuk edukasi & pengembangan.

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=TulungagungBlackHat-TBH-Recon&label=Views&color=red&style=flat" />
</p>
