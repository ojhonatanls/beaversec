"""
modules/dns_enum.py

Correções principais:
- Remove import não usado.
- Mantém tratamento de exceções e formatação de saída.
- Retorna estrutura consistente.
"""
import dns.resolver
import dns.exception

def run(target, **kwargs):
    """
    Módulo de enumeração DNS.
    Exemplo: python main.py dns_enum google.com
    """
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
    results = {target: {}}

    for record in record_types:
        try:
            answers = dns.resolver.resolve(target, record)
            results[target][record] = [str(r).strip() for r in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers):
            results[target][record] = []
        except Exception as e:
            results[target][record] = f"Error: {str(e)}"

    # Exibe formatado
    print(f"\n[+] DNS Enumeration for {target}")
    for rec, data in results[target].items():
        if data:
            if isinstance(data, list):
                print(f"  {rec}: {', '.join(data)}")
            else:
                print(f"  {rec}: {data}")
        else:
            print(f"  {rec}: No records found")

    return results
