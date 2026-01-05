import json
import ssl
import http.client

from utils import write_log
from config import LOG_DOH


# DoH settings (safe to change provider)
DNS_SERVER = "cloudflare-dns.com"
DNS_PATH = "/dns-query"
DNS_TIMEOUT = 5

dns_cache = {}

def resolve_domain(name):
    if name in dns_cache:
        return dns_cache[name]

    if LOG_DOH:
        write_log(f"DoH resolve → {name}")

    for _ in range(3):
        try:
            tls_context = ssl.create_default_context()
            https = http.client.HTTPSConnection(
                DNS_SERVER,
                443,
                context=tls_context,
                timeout=DNS_TIMEOUT
            )

            https.request(
                "GET",
                f"{DNS_PATH}?name={name}&type=A",
                headers={"Accept": "application/dns-json"}
            )

            response = https.getresponse()
            if response.status != 200:
                continue

            result = json.loads(response.read().decode())

            for record in result.get("Answer", []):
                if record.get("type") == 1:  # IPv4
                    ip = record.get("data")
                    dns_cache[name] = ip
                    return ip

        except Exception:
            continue

    return None
