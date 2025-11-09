import os
import configparser
import yaml

class ConfigUtils:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.abspath(os.path.join(base_dir, ".."))
        self.ini_path = os.path.join(self.project_root, "config", "config.ini")
        self.env_path = os.path.join(self.project_root, "config", "environment.yaml")
        self._ini = configparser.ConfigParser()
        self._ini.read(self.ini_path, encoding="utf-8")

        with open(self.env_path, "r", encoding="utf-8") as f:
            self._envs = yaml.safe_load(f)

    def get(self, section, key, fallback=None):
        return self._ini.get(section, key, fallback=fallback)

    def get_environment(self, env_name="dev"):
        return self._envs.get(env_name, {})