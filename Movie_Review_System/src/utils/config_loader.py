import yaml
import os

def load_config(env="dev"):
    # Path to the single config file relative to this script
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "../../config/config.yaml")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with open(config_path, 'r') as file:
        try:
            all_configs = yaml.safe_load(file)
            # Return the specific environment config
            config = all_configs.get(env.lower())
            if not config:
                raise ValueError(f"Environment '{env}' not found in config file.")
            return config
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")
            return None

