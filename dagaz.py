import re
import sys
from typing import Any
from yaml import safe_load


_config_dir: str = 'config'


def flatten_yaml(data: dict[str, Any], parent_key: str = None, sep: str = '_') -> dict[str, Any]:
    items = {}
    for k, v in data.items():
        new_key = (f'{parent_key}{sep}{k}' if parent_key else k).upper()
        if isinstance(v, dict):
            items.update(flatten_yaml(v, new_key, sep=sep))
        else:
            value = ','.join(map(str, v)) if isinstance(v, list) else v
            if new_key not in items:
                items[new_key] = []
            items[new_key].append(value)
    return items


def parse_config(file_path: str) -> dict[str, Any]:
    with open(file_path, 'r') as f:
        config = safe_load(f.read())
    return flatten_yaml(config)


def update_config(old_config: dict[str, Any], new_config: dict[str, Any]) -> dict[str, Any]:
    for k, v in new_config.items():
        if k in old_config:
            old_config[k] += v
        else:
            old_config[k] = v
    return old_config


def generate_env(env: str):
    cfg_file: str = f'{_config_dir}/default.yml'
    yml_file: str = f'{_config_dir}/{env}.yml'
    env_file: str = '.env'

    config_flat = parse_config(cfg_file)

    if env:
        config_flat = update_config(config_flat, parse_config(yml_file))

    for k1, v1 in config_flat.items():
        matches = re.findall(r'\${[\w.]+}', str(v1[-1]))
        for match in matches:
            k2 = match.replace('${', '').replace('}', '').replace('.', '_').upper()
            if k2 in config_flat:
                if k1 == k2:
                    v2 = '' if len(v1) == 1 else str(v1[-2])
                else:
                    v2 = str(config_flat[k2][-1])
                config_flat[k1][-1] = str(v1[-1]).replace(match, v2)
            else:
                raise KeyError(f'{match} not in config')

    env_context = []
    for k in sorted(config_flat):
        v = config_flat.get(k)[-1]
        if config_flat.get(k) is None:
            v = ''
        env_context.append(f'{k}={v}')

    with open(env_file, 'w') as f:
        f.write('\n'.join(env_context))

if __name__ == '__main__':
    generate_env(sys.argv[1] if len(sys.argv) > 1 else None)
