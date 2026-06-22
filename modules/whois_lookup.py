"""
modules/whois_lookup.py

Correções principais:
- Trata expiration_date quando é list, datetime ou string.
- Evita crash se a data não puder ser convertida; faz checagens robustas.
- Retorna objeto WHOIS e/ou dicionário com informações úteis.
"""
import whois
from datetime import datetime, timezone

def run(target, **kwargs):
    """
    Consulta informações WHOIS de um domínio.
    Exemplo: python main.py whois_lookup google.com
    """
    try:
        w = whois.whois(target)

        print(f"\n[+] WHOIS Lookup for {target}")
        print(f"  Registrar: {w.get('registrar') if isinstance(w, dict) else getattr(w, 'registrar', None)}")
        print(f"  Creation Date: {w.get('creation_date') if isinstance(w, dict) else getattr(w, 'creation_date', None)}")
        print(f"  Expiration Date: {w.get('expiration_date') if isinstance(w, dict) else getattr(w, 'expiration_date', None)}")
        print(f"  Name Servers: {w.get('name_servers') if isinstance(w, dict) else getattr(w, 'name_servers', None)}")
        print(f"  Status: {w.get('status') if isinstance(w, dict) else getattr(w, 'status', None)}")
        print(f"  Emails: {w.get('emails') if isinstance(w, dict) else getattr(w, 'emails', None)}")

        # Verifica expiração de forma robusta
        exp_raw = None
        if isinstance(w, dict):
            exp_raw = w.get('expiration_date')
        else:
            exp_raw = getattr(w, 'expiration_date', None)

        exp = None
        if exp_raw:
            # whois lib frequentemente retorna list ou datetime
            if isinstance(exp_raw, list) and exp_raw:
                exp = exp_raw[0]
            else:
                exp = exp_raw

            if isinstance(exp, str):
                # Se for string, tentar parse básico (ISO-like), senão ignorar
                try:
                    exp = datetime.fromisoformat(exp)
                except Exception:
                    try:
                        # Tentar remover timezone string GMT, etc (fallback simples)
                        exp = datetime.strptime(exp, "%b %d %H:%M:%S %Y")
                    except Exception:
                        exp = None

            if isinstance(exp, datetime):
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                days_left = (exp - now).days
                if days_left < 30:
                    print(f"  ⚠️ Domínio expira em {days_left} dias!")
        else:
            print("  ⚠️ Expiration date não disponível ou não reconhecida.")

        # Retorno estruturado (mantém objeto w para quem quiser detalhes)
        return {"whois": w, "expiration_date": exp}

    except Exception as e:
        print(f"[-] WHOIS lookup failed: {e}")
        return None
