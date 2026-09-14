#!/usr/bin/env python3
# TBH-Recon v2.0 Pro - JSON + HTML Report
import socket, requests, argparse, sys, ssl, json
from datetime import datetime
from urllib.parse import urlparse

BANNER = """\033[91m╔════════════════════════════════════════╗
\033[91m║  \033[97m TBH-RECON v2.0 Pro \033[91m- JSON/HTML Report \033[91m║
\033[91m║  \033[90m Tulungagung Black Hat | uchil404 \033[91m║
\033[91m╚════════════════════════════════════════╝\033[0m"""

PORT_CVE = {21:"FTP anon",22:"SSH",80:"HTTP",443:"HTTPS",445:"SMB MS17-010",3306:"MySQL",3389:"RDP BlueKeep",6379:"Redis",8080:"HTTP-Alt"}

def check_headers(url):
    r = requests.get(url, timeout=5, headers={'User-Agent':'TBH-Recon/2.0'})
    headers = dict(r.headers)
    missing = [h for h in ['Strict-Transport-Security','Content-Security-Policy','X-Frame-Options'] if h not in headers]
    return {"status":r.status_code,"server":headers.get('Server','Unknown'),"missing":missing,"headers":headers}

def check_ssl(domain):
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3); s.connect((domain,443)); cert=s.getpeercert()
            expire=cert.get('notAfter'); issuer=dict(x[0] for x in cert.get('issuer',[])).get('organizationName','Unknown')
            exp_dt=datetime.strptime(expire, "%b %d %H:%M:%S %Y %Z")
            days=(exp_dt - datetime.utcnow()).days
            return {"issuer":issuer,"expire":expire,"days":days}
    except Exception as e:
        return {"error":str(e)}

def port_scan(target, ports):
    open_ports=[]
    for port in ports:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.settimeout(1)
        if s.connect_ex((target,port))==0:
            open_ports.append({"port":port,"info":PORT_CVE.get(port,"Unknown")})
        s.close()
    return open_ports

def main():
    print(BANNER)
    parser=argparse.ArgumentParser(description="TBH-Recon v2.0 Pro")
    parser.add_argument("-u","--url",required=True,help="Target URL")
    parser.add_argument("--ssl",action="store_true",help="SSL check")
    parser.add_argument("-p","--ports",action="store_true",help="Port scan")
    parser.add_argument("-s","--subdomain",action="store_true")
    parser.add_argument("--json",help="Save JSON report")
    parser.add_argument("--html",help="Save HTML report")
    args=parser.parse_args()
    url=args.url if args.url.startswith("http") else "https://"+args.url
    domain=urlparse(url).netloc
    ip=socket.gethostbyname(domain)
    print(f"\033[96m[*] {domain} ({ip})\033[0m")
    report={"target":domain,"ip":ip,"url":url,"time":str(datetime.now())}
    report["headers"]=check_headers(url)
    print(f"\033[92m[+] Status {report['headers']['status']} | Missing: {report['headers']['missing'] or 'none'}\033[0m")
    if args.ssl:
        report["ssl"]=check_ssl(domain)
        print(f"\033[92m[+] SSL: {report['ssl']}\033[0m")
    if args.ports:
        report["ports"]=port_scan(ip, list(PORT_CVE.keys()))
        print(f"\033[92m[+] Ports: {report['ports']}\033[0m")
    if args.subdomain:
        common=['www','mail','api']; found=[]
        for sub in common:
            try: socket.gethostbyname(f"{sub}.{domain}"); found.append(f"{sub}.{domain}")
            except: pass
        report["subdomains"]=found
        print(f"\033[92m[+] Subdomains: {found}\033[0m")
    if args.json:
        open(args.json,'w').write(json.dumps(report,indent=2))
        print(f"\033[92m[✓] JSON saved: {args.json}\033[0m")
    if args.html:
        html=f"<html><body><h1>TBH-Recon Pro Report {domain}</h1><pre>{json.dumps(report,indent=2)}</pre></body></html>"
        open(args.html,'w').write(html)
        print(f"\033[92m[✓] HTML saved: {args.html}\033[0m")
    print("\033[92m[✓] Pro Done\033[0m")

if __name__=="__main__": main()
