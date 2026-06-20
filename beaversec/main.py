#!/usr/bin/env python3
"""Ponto de entrada principal do BeaverSec."""

import sys
import argparse
import importlib
import json
import datetime

def list_modules():
    """Lista os módulos disponíveis."""
    print("📋 Módulos disponíveis:")
    print("  - ping_sweep     - Verifica hosts ativos via ICMP")
    print("  - port_scanner   - Escaneia portas TCP abertas")
    print("  - dns_enum       - Enumera registros DNS")
    print("  - ssl_scan       - Analisa certificados SSL/TLS")
    print("  - http_headers   - Analisa headers HTTP de segurança")

def save_report(data, output_file):
    """Salva o resultado em um arquivo JSON."""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"📄 Relatório salvo em: {output_file}")

def run_module(module_name: str, target: str, args: str = "", **kwargs):
    """Executa um módulo específico."""
    try:
        module = importlib.import_module(f"beaversec.modules.{module_name}")
        
        parsed_args = {}
        if args:
            try:
                parsed_args = json.loads(args)
            except:
                for item in args.split():
                    if "=" in item:
                        key, value = item.split("=", 1)
                        parsed_args[key] = value
        
        parsed_args.update(kwargs)
        
        print(f"▶️ Executando {module_name} contra {target}...")
        result = module.run(target, **parsed_args)
        
        print("\n📊 RESULTADO:")
        if 'error' in result:
            print(f"  ❌ {result['error']}")
        else:
            for key, value in result.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for k, v in value.items():
                        print(f"    {k}: {v}")
                elif isinstance(value, list):
                    print(f"  {key}: {len(value)} itens")
                    for item in value[:5]:
                        print(f"    - {item}")
                    if len(value) > 5:
                        print(f"    ... e mais {len(value)-5} itens")
                else:
                    print(f"  {key}: {value}")
        
        output_file = kwargs.get('output_file')
        if output_file:
            report_data = {
                'module': module_name,
                'target': target,
                'timestamp': datetime.datetime.now().isoformat(),
                'result': result
            }
            save_report(report_data, output_file)
        
    except ModuleNotFoundError:
        print(f"❌ Módulo '{module_name}' não encontrado")
        list_modules()
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Erro de validação: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao executar: {str(e)}")
        sys.exit(1)

def cli():
    """Interface de linha de comando principal."""
    parser = argparse.ArgumentParser(
        description="BeaverSec - Ferramenta de cibersegurança",
        epilog="Exemplo: beaversec run ping_sweep --target 8.8.8.8"
    )
    
    parser.add_argument("-v", "--version", action="version", version="BeaverSec v0.2.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos")
    subparsers.add_parser("list", help="Lista módulos")
    
    run_parser = subparsers.add_parser("run", help="Executa módulo")
    run_parser.add_argument("module", help="Nome do módulo")
    run_parser.add_argument("--target", required=True, help="Alvo (IP/domínio/URL)")
    run_parser.add_argument("--args", default="", help="Argumentos (JSON ou key=value)")
    run_parser.add_argument("--output-file", help="Salva resultado em arquivo JSON")
    run_parser.add_argument("--verbose", action="store_true", help="Logs detalhados")
    run_parser.add_argument("--timeout", type=int, default=5, help="Timeout em segundos")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_modules()
    elif args.command == "run":
        run_module(args.module, args.target, args.args, 
                   verbose=args.verbose, timeout=args.timeout,
                   output_file=args.output_file)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()