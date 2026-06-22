"""
utils/config_loader.py

Correções principais:
- Trata arquivo ausente/erro no YAML com mensagens amigáveis.
- Retorna um dicionário vazio se não houver config.
- Evita crashes ao chamar get_setting quando config está ausente.
"""
import os
import yaml

_CONFIG = None

def load_config():
    global _CONFIG
    if _CONFIG is None:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
        if not os.path.isfile(config_path):
            # Não existe config.yaml — retorna {} e evita exceção
            _CONFIG = {}
            return _CONFIG
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                _CONFIG = yaml.safe_load(f) or {}
        except Exception as e:
            # Falha ao ler/parsear YAML — grava aviso e retorna {}
            print(f"[-] Falha ao carregar config.yaml ({config_path}): {e}")
            _CONFIG = {}
    return _CONFIG

def get_setting(key, default=None):
    config = load_config() or {}
    if not key:
        return default
    keys = key.split('.')
    data = config
    for k in keys:
        if isinstance(data, dict) and k in data:
            data = data[k]
        else:
            return default
    return data
