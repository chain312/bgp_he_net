import yaml
yaml_file = "../config/config.yaml"

with open(yaml_file, 'r') as f:
    cfg = yaml.safe_load(f)

print(cfg)