# TBH-Recon v1.1 - Web Recon + SSL & CVE

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Version-v1.1-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Purpose-Bug%20Bounty-green?style=for-the-badge">
</p>

> **v1.1 Update** - Tambah **SSL Check** & **CVE Hints** biar lebih lengkap untuk edukasi bug bounty.

## ✨ v1.1 vs v1.0
- ✅ **SSL Check** (`--ssl`) - Cek issuer, expire, sisa hari
- ✅ **CVE Hints** - Tiap port ada hint CVE (ex: 445 EternalBlue)
- ✅ `--top100` support

## 🚀 Usage
```bash
# Header + SSL
python3 main.py -u https://example.com --ssl

# Full recon
python3 main.py -u https://example.com --ssl --ports --top100 --subdomain

# Contoh output SSL
[+] SSL Check for example.com...
[✓] Issuer: Cloudflare
[✓] Expire: May 20 00:00:00 2027 GMT
[✓] Valid for 210 days
```

## 📦 Install
```bash
git clone https://github.com/TulungagungBlackHat/TBH-Recon
cd TBH-Recon
pip install requests
python3 main.py -u https://example.com --ssl
```

## 🛡️ Edukasi
- Missing headers → low finding
- SSL expire <30 hari → medium
- Port terbuka + CVE hint → info disclosure

## 👥 TBH
uchil404 - Tulungagung Black Hat - Always Smile :)

## 📄 License
MIT
