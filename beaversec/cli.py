"""CLI entrypoint for BeaverSec."""
import asyncio
import sys
import argparse
import logging
import json
import inspect
from typing import List

from beaversec.modules import MODULES

logger = logging.getLogger("beaversec.cli")


def cli():
    parser = argparse.ArgumentParser(description="BeaverSec - Modular Offensive Security")
    parser.add_argument("-v", "--version", action="version", version="3.0.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # List command
    subparsers.add_parser("list", help="List available modules")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run a module")
    run_parser.add_argument("module", type=str, help="Module name")
    run_parser.add_argument("targets", nargs="+", help="Targets (IPs, domains, etc.)")
    run_parser.add_argument("-p", "--ports", type=str, default="", help="Comma separated ports")
    run_parser.add_argument("-o", "--output", type=str, default=None, help="Output file (JSON)")
    run_parser.add_argument("--format", type=str, default="json", choices=["json", "html", "csv"], help="Output format")
    run_parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.command == "list":
        print("Available modules:")
        for name in sorted(MODULES.keys()):
            print(f"  - {name}")
        return
    
    if args.command == "run":
        module_name = args.module
        if module_name not in MODULES:
            print(f"Module '{module_name}' not found.")
            print("Use 'beaversec list' to see available modules.")
            sys.exit(1)
        
        # Parse ports
        port_list = []
        if args.ports:
            port_list = [int(p.strip()) for p in args.ports.split(",") if p.strip()]
        
        # Instantiate module
        module_cls = MODULES[module_name]
        module = module_cls()
        
        # Run module
        async def run_async():
            sig = inspect.signature(module.run)
            params = list(sig.parameters.keys())
            
            kwargs = {}
            if 'target' in params:
                kwargs['target'] = args.targets[0] if len(args.targets) == 1 else args.targets
            elif 'targets' in params:
                kwargs['targets'] = args.targets
            elif 'domains' in params:
                kwargs['domains'] = args.targets
            elif 'networks' in params:
                kwargs['networks'] = args.targets
            elif 'hosts' in params:
                kwargs['hosts'] = args.targets
            elif 'domain' in params:
                kwargs['domain'] = args.targets[0] if args.targets else None
            
            if 'ports' in params and port_list:
                kwargs['ports'] = port_list
            
            if asyncio.iscoroutinefunction(module.run):
                return await module.run(**kwargs)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, lambda: module.run(**kwargs))
        
        print(f"Running {module_name} against {len(args.targets)} target(s)...")
        result = asyncio.run(run_async())
        
        # Salvar resultado se output for especificado
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"Result saved to {args.output}")
        else:
            print("Result:")
            print(result)
        return
    
    parser.print_help()


if __name__ == "__main__":
    cli()
