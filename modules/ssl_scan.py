#!/usr/bin/env python3
"""
modules/ssl_scan.py

Correções principais:
- Captura o cipher enquanto a conexão SSL está aberta (evita usar ssock após o with).
- Usa ssl.cert_time_to_seconds para converter datas de certificado de forma robusta.
- Retorna dicionário com informações estruturadas (útil para salvar/usar em outras partes do programa).
- Tratamento de exceções melhorado.
"""
import socket
import ssl
import datetime
from utils.config_loader import get_setting

def run(target, **kwargs):
    """
    Obtém informações do certificado SSL/TLS.
    Exemplo: python main.py ssl_scan google.com
    """
    port = kwargs.get('port', 443)
    if ':' in str(target):
        host, maybe_port = target.split(':', 1)
        try:
            port = int(maybe_port)
            target = host
        except ValueError:
            pass

    try:
        context = ssl.create_default_context()
        cert = None
        cipher = None
        with socket.create_connection((target, port), timeout=10.0) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()

        if not cert:
            print(f"[-] No certificate retrieved from {target}:{port}")
            return None

        # Safe parsing of subject / issuer
        def _format_name(name):
            try:
                # name is typically a tuple of tuples of tuples: ((('commonName', 'example.com'),), ...)
                parts = []
                for rdn in name:
                    for attr in rdn:
                        parts.append(f"{attr[0]}={attr[1]}")
                return ", ".join(parts)
            except Exception:
                return str(name)

        subject = _format_name(cert.get('subject', ()))
        issuer = _format_name(cert.get('issuer', ()))
        version = cert.get('version', 'N/A')

        # Parse times using ssl helper (robust against various formats)
        not_before = None
        not_after = None
        try:
            if 'notBefore' in cert:
                not_before = datetime.datetime.utcfromtimestamp(ssl.cert_time_to_seconds(cert['notBefore']))
            if 'notAfter' in cert:
                not_after = datetime.datetime.utcfromtimestamp(ssl.cert_time_to_seconds(cert['notAfter']))
        except Exception:
            # fallback: keep raw strings
            not_before = cert.get('notBefore')
            not_after = cert.get('notAfter')

        if isinstance(not_after, datetime.datetime):
            days_left = (not_after - datetime.datetime.utcnow()).days
        else:
            days_left = None

        warn_days = get_setting('modules.ssl_scan.warn_expiry_days', 30)

        # Prints (não remove retornos estruturados)
        print(f"\n[+] SSL/TLS Info for {target}:{port}")
        print(f"  Subject: {subject}")
        print(f"  Issuer: {issuer}")
        print(f"  Version: {version}")
        if isinstance(not_before, datetime.datetime):
            print(f"  Valid From (UTC): {not_before.isoformat()}")
        else:
            print(f"  Valid From: {not_before}")
        if isinstance(not_after, datetime.datetime):
            print(f"  Valid To (UTC):   {not_after.isoformat()}")
        else:
            print(f"  Valid To: {not_after}")

        if days_left is not None:
            if days_left < 0:
                print(f"  ⚠️ EXPIRADO há {-days_left} dias!")
            elif days_left < int(warn_days):
                print(f"  ⚠️ Atenção: Expira em {days_left} dias!")
            else:
                print(f"  ✅ Válido por mais {days_left} dias.")
        else:
            print("  ⚠️ Não foi possível calcular dias restantes de validade.")

        print(f"  Cipher: {cipher}")

        # Retorno estruturado
        return {
            "host": target,
            "port": port,
            "subject": subject,
            "issuer": issuer,
            "version": version,
            "not_before": not_before.isoformat() if isinstance(not_before, datetime.datetime) else not_before,
            "not_after": not_after.isoformat() if isinstance(not_after, datetime.datetime) else not_after,
            "days_left": days_left,
            "cipher": cipher,
            "raw_cert": cert
        }

    except Exception as e:
        print(f"[-] SSL Scan failed: {e}")
        return None
