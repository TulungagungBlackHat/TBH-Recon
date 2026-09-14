#!/usr/bin/env python3
# TBH-Recon - Web Reconnaissance Tool for Bug Bounty & Education
# Team: Tulungagung Black Hat - Ethical Hacking
# Disclaimer: For Educational & Authorized Testing Only

import socket
import requests
import argparse
import sys
from datetime import datetime
from urllib.parse import urlparse

BANNER = """
\033[91m╔════════════════════════════════════════╗
\033[91m║  \033[97m TBH-RECON \033[91m- Web Reconnaissance Tool  \033[91m║
\033[91m║  \033[90m Tulungagung Black Hat | Always Smile \033[91m║
\033[91m╚════════════════════════════════════════╝\033[0m
"""

def check_headers(url):
    try:
        r = requests.get(url, timeout=5, headers={'User-Agent': 'TBH-Recon/1.0'})
        print(f"\033[92m[+] Status: {r.status_code} | Server: {r.headers.get('Server','Unknown')}\033[0m")
        print(f"\033[96m[+] Headers:\033[0m")
        for k,v in r.headers.items():
            if k.lower() in ['server','x-powered-by','x-frame-options','strict-transport-security','content-security-policy','x-xss-protection']:
                color = "\033[92m" if k.lower() in ['strict-transport-security','content-security-policy'] else "\033[93m"
                print(f"  {color}{k}: {v}\033[0m")
        # Check security headers missing
        missing = []
        for h in ['Strict-Transport-Security','Content-Security-Policy','X-Frame-Options']:
            if h not in r.headers:
                missing.append(h)
        if missing:
            print(f"\033[91m[!] Missing Security Headers: {', '.join(missing)}\033[0m")
        else:
            print(f"\033[92m[✓] All key security headers present\033[0m")
        return True
    except Exception as e:
        print(f"\033[91m[!] Error: {e}\033[0m")
        return False

def port_scan(target, ports=[21,22,80,443,3306,8080,8443]):
    print(f"\n\033[96m[+] Scanning {target}...\033[0m")
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            result = s.connect_ex((target, port))
            if result == 0:
                try:
                    banner = socket.getservbyport(port)
                except:
                    banner = "unknown"
                print(f"\033[92m[OPEN] {port}/{banner}\033[0m")
                open_ports.append(port)
            else:
                print(f"\033[90m[CLOSED] {port}\033[0m")
            s.close()
        except:
            pass
    return open_ports

def subdomain_check(domain):
    # Simple passive check via common subdomains (educational)
    common = ['www','mail','ftp','admin','api','blog','shop','m','mobile']
    print(f"\n\033[96m[+] Checking common subdomains for {domain}...\033[0m")
    for sub in common:
        host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            print(f"\033[92m[FOUND] {host} -> {ip}\033[0m")
        except:
            print(f"\033[90m[NOT FOUND] {host}\033[0m")

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="TBH-Recon - Educational Web Recon Tool")
    parser.add_argument("-u","--url", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("-p","--ports", action="store_true", help="Enable port scan")
    parser.add_argument("-s","--subdomain", action="store_true", help="Check common subdomains")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    target_ip = None
    try:
        target_ip = socket.gethostbyname(domain)
        print(f"\033[96m[*] Target: {domain} ({target_ip}) | {datetime.now()}\033[0m\n")
    except:
        print(f"\033[91m[!] Cannot resolve {domain}\033[0m")
        sys.exit(1)

    print(f"\033[93m{'='*50}\n[1] HTTP Header Analysis\n{'='*50}\033[0m")
    check_headers(url)

    if args.ports:
        print(f"\n\033[93m{'='*50}\n[2] Port Scanning\n{'='*50}\033[0m")
        port_scan(target_ip)

    if args.subdomain:
        print(f"\n\033[93m{'='*50}\n[3] Subdomain Enumeration\n{'='*50}\033[0m")
        subdomain_check(domain)

    print(f"\n\033[92m[✓] Recon completed. Use findings for hardening, not exploitation.\033[0m")

if __name__ == "__main__":
    main()
