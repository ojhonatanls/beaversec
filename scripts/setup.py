#!/usr/bin/env python3
"""Setup script for BeaverSec installation."""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Main installation entry point."""
    print("BeaverSec Setup")
    print("===============")

    # Check Python version
    if sys.version_info < (3, 8):
        print(f"Error: Python 3.8+ required (found {sys.version_info.major}.{sys.version_info.minor})")
        sys.exit(1)

    print(f"Found Python {sys.version_info.major}.{sys.version_info.minor}")

    # Setup steps
    steps = [
        ("Creating virtual environment", create_venv),
        ("Installing dependencies", install_deps),
        ("Installing BeaverSec", install_beaversec),
        ("Creating configuration", create_config),
    ]

    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            step_func()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    print("\nInstallation complete!")
    print("\nTo start using BeaverSec:")
    print("  source venv/bin/activate")
    print("  beaversec --help")


def create_venv():
    """Create virtual environment."""
    if not Path("venv").exists():
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)


def install_deps():
    """Install dependencies."""
    if sys.platform == "win32":
        python = Path("venv") / "Scripts" / "python.exe"
        pip = Path("venv") / "Scripts" / "pip.exe"
    else:
        python = Path("venv") / "bin" / "python"
        pip = Path("venv") / "bin" / "pip"

    subprocess.run([str(pip), "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(pip), "install", "-r", "requirements.txt"], check=True)

    if len(sys.argv) > 1 and sys.argv[1] == "--dev":
        subprocess.run([str(pip), "install", "-r", "requirements-dev.txt"], check=True)


def install_beaversec():
    """Install BeaverSec package."""
    if sys.platform == "win32":
        pip = Path("venv") / "Scripts" / "pip.exe"
    else:
        pip = Path("venv") / "bin" / "pip"

    subprocess.run([str(pip), "install", "-e", "."], check=True)


def create_config():
    """Create configuration directory and default config."""
    config_dir = Path.home() / ".beaversec"
    config_dir.mkdir(exist_ok=True)
    (config_dir / "logs").mkdir(exist_ok=True)
    (config_dir / "credentials").mkdir(exist_ok=True)

    # Set permissions on Unix
    if sys.platform != "win32":
        os.chmod(str(config_dir), 0o755)
        os.chmod(str(config_dir / "credentials"), 0o700)

    config_file = config_dir / "config.yaml"
    if not config_file.exists():
        template = Path("beaversec") / "config" / "templates" / "config.yaml.template"
        if template.exists():
            import shutil
            shutil.copy2(str(template), str(config_file))


if __name__ == "__main__":
    main()