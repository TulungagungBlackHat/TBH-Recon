#!/usr/bin/env python3
# TBH-Recon v1.1 - Web Recon + SSL Check + CVE Hint (Educational)
# Team: Tulungagung Black Hat - uchil404

import socket
import requests
import argparse
import sys
import ssl
from datetime import datetime
from urllib.parse import urlparse

BANNER = """
\033[91m╔════════════════════════════════════════╗
\033[91m║  \033[97m TBH-RECON v1.1 \033[91m- Web Recon + SSL/CVE  \033[91m║
\033[91m║  \033[90m Tulungagung Black Hat | Always Smile \033[91m║
\033[91m╚════════════════════════════════════════╝\033[0m
"""

PORT_CVE = {
    21: "FTP - anon login, CVE-2020-15782",
    22: "SSH - CVE-2018-15473",
    80: "HTTP - OWASP, dir bust",
    443: "HTTPS - SSL/TLS",
    445: "SMB - EternalBlue MS17-010",
    3306: "MySQL - CVE-2012-2122",
    3389: "RDP - BlueKeep CVE-2019-0708",
    6379: "Redis - CVE-2022-0543",
    8080: "HTTP-Alt - Jenkins",
}

def check_headers(url):
    try:
        r = requests.get(url, timeout=5, headers={'User-Agent': 'TBH-Recon/1.1'})
        print(f"\033[92m[+] Status: {r.status_code} | Server: {r.headers.get('Server','Unknown')}\033[0m")
        for k,v in r.headers.items():
            if k.lower() in ['server','x-powered-by','x-frame-options','strict-transport-security','content-security-policy','x-xss-protection']:
                color = "\033[92m" if k.lower() in ['strict-transport-security','content-security-policy'] else "\033[93m"
                print(f"  {color}{k}: {v}\033[0m")
        missing = [h for h in ['Strict-Transport-Security','Content-Security-Policy','X-Frame-Options'] if h not in r.headers]
        if missing:
            print(f"\033[91m[!] Missing: {', '.join(missing)}\033[0m")
        else:
            print(f"\033[92m[✓] All key security headers present\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Error: {e}\033[0m")

def check_ssl(domain):
    print(f"\n\033[96m[+] SSL Check for {domain}...\033[0m")
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)
            s.connect((domain, 443))
            cert = s.getpeercert()
            expire = cert.get('notAfter')
            issuer = dict(x[0] for x in cert.get('issuer', []))
            print(f"\033[92m[✓] Issuer: {issuer.get('organizationName','Unknown')}\033[0m")
            print(f"\033[92m[✓] Expire: {expire}\033[0m")
            # Try parse expiry
            try:
                exp_dt = datetime.strptime(expire, "%b %d %H:%M:%S %Y %Z")
                days = (exp_dt - datetime.utcnow()).days
                if days < 30:
                    print(f"\033[91m[!] Expires in {days} days - soon!\033[0m")
                else:
                    print(f"\033[92m[✓] Valid for {days} days\033[0m")
            except:
                pass
    except Exception as e:
        print(f"\033[90m[-] SSL check failed/ no HTTPS: {e}\033[0m")

def port_scan(target, ports):
    print(f"\n\033[96m[+] Scanning {target}...\033[0m")
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            if s.connect_ex((target, port)) == 0:
                info = PORT_CVE.get(port, "Unknown")
                print(f"\033[92m[OPEN] {port:5d} {info}\033[0m")
                open_ports.append(port)
            else:
                print(f"\033[90m[CLOSED] {port}\033[0m")
            s.close()
        except: pass
    return open_ports

def subdomain_check(domain):
    common = ['www','mail','ftp','admin','api','blog','shop','m','mobile']
    print(f"\n\033[96m[+] Subdomains for {domain}...\033[0m")
    for sub in common:
        host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            print(f"\033[92m[FOUND] {host} -> {ip}\033[0m")
        except:
            print(f"\033[90m[NOT FOUND] {host}\033[0m")

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="TBH-Recon v1.1 - SSL + CVE")
    parser.add_argument("-u","--url", required=True, help="Target URL")
    parser.add_argument("-p","--ports", action="store_true", help="Enable port scan")
    parser.add_argument("-s","--subdomain", action="store_true", help="Subdomain check")
    parser.add_argument("--ssl", action="store_true", help="SSL certificate check")
    parser.add_argument("--top100", action="store_true", help="Use top ports")
    args = parser.parse_args()

    url = args.url if args.url.startswith("http") else "https://"+args.url
    domain = urlparse(url).netloc
    try:
        ip = socket.gethostbyname(domain)
        print(f"\033[96m[*] Target: {domain} ({ip}) | {datetime.now()}\033[0m\n")
    except:
        print(f"\033[91m[!] Cannot resolve {domain}\033[0m"); sys.exit(1)

    print(f"\033[93m{'='*50}\n[1] HTTP Header\n{'='*50}\033[0m")
    check_headers(url)

    if args.ssl:
        print(f"\n\033[93m{'='*50}\n[2] SSL Certificate\n{'='*50}\033[0m")
        check_ssl(domain)

    if args.ports:
        print(f"\n\033[93m{'='*50}\n[3] Port Scan\n{'='*50}\033[0m")
        ports = list(PORT_CVE.keys()) if args.top100 else [21,22,80,443,3306,8080,8443]
        port_scan(ip, ports)

    if args.subdomain:
        print(f"\n\033[93m{'='*50}\n[4] Subdomain\n{'='*50}\033[0m")
        subdomain_check(domain)

    print(f"\n\033[92m[✓] Done v1.1 - Use for hardening. Educational only.\033[0m")

if __name__ == "__main__":
    main()
