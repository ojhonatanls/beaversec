"""
Interface de linha de comando usando Click.
"""
import sys
from pathlib import Path

import click
import yaml

from beaversec.core.beaver import Beaver
from beaversec.modules.dns_enum import DNSEnum
from beaversec.modules.http_headers import HTTPHeaders
from beaversec.modules.ping_sweep import PingSweep
from beaversec.modules.port_scanner import PortScanner
from beaversec.modules.ssl_scan import SSLScan
from beaversec.modules.subdomain_brute import SubdomainBrute
from beaversec.modules.traceroute import Traceroute
from beaversec.modules.whois_lookup import WhoisLookup


def load_config(config_file: str) -> dict:
    """Carrega configuração de arquivo YAML."""
    if config_file and Path(config_file).exists():
        with open(config_file, "r") as f:
            return yaml.safe_load(f) or {}
    return {}


@click.group()
@click.option("--config", "-c", type=str, help="Arquivo de configuração YAML")
@click.option("--verbose", "-v", is_flag=True, help="Modo verboso")
@click.pass_context
def cli(ctx, config: str, verbose: bool):
    """BeaverSec - Ferramenta modular de segurança ofensiva."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = load_config(config) if config else {}
    beaver = Beaver(verbose=verbose)
    # Registra todos os módulos
    for mod in [
        PingSweep(),
        PortScanner(),
        DNSEnum(),
        SSLScan(),
        HTTPHeaders(),
        SubdomainBrute(),
        Traceroute(),
        WhoisLookup(),
    ]:
        beaver.register_module(mod)
    ctx.obj["beaver"] = beaver


@cli.command()
@click.argument("module_name")
@click.argument("target")
@click.option("--threads", "-t", default=10, help="Número de threads")
@click.option("--timeout", default=5.0, help="Timeout em segundos")
@click.option("--rate-limit", default=0.1, help="Delay entre requisições")
@click.option("--proxy", help="Proxy (ex: http://user:pass@host:port)")
@click.option("--output", "-o", help="Arquivo de saída")
@click.option("--format", "-f", default="json", help="Formato de saída (json, html, csv)")
@click.option("--dry-run", is_flag=True, help="Simula a execução")
@click.pass_context
def run(ctx, module_name, target, threads, timeout, rate_limit, proxy, output, format, dry_run):
    """Executa um módulo contra um alvo."""
    beaver = ctx.obj["beaver"]
    verbose = ctx.obj["verbose"]

    if dry_run:
        click.echo(f"[DRY RUN] Executaria {module_name} em {target}")
        return

    click.echo(f"🚀 Executando {module_name} em {target}...")
    result = beaver.run_module(
        module_name,
        target,
        threads=threads,
        timeout=timeout,
        rate_limit=rate_limit,
        proxy=proxy,
        verbose=verbose,
    )

    if output:
        beaver.export(format, output)

    if result.success:
        click.echo(f"✅ Sucesso!")
        if verbose:
            click.echo(result.data)
    else:
        click.echo(f"❌ Falha: {result.errors}")
        sys.exit(1)


@cli.command()
@click.pass_context
def list_modules(ctx):
    """Lista todos os módulos disponíveis."""
    from beaversec.modules import MODULES

    click.echo("📦 Módulos disponíveis:")
    for name, desc in MODULES.items():
        click.echo(f"  - {name}: {desc}")


if __name__ == "__main__":
    cli()
