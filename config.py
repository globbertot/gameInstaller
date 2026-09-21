from configparser import ConfigParser
from pathlib import Path


class Config:
    def __init__(self):
        self.conf_path = Path("~/.config/glob/conf.ini").expanduser()
        self.config = ConfigParser()

        self.settings = {
            "default_wine": "system",
            "install_path": Path("~/Documents/GAMES/").expanduser()
        }
        self.load()

    def save(self):
        self.conf_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.config.has_section("main"):
            self.config.add_section("main")

        for key, val in self.settings.items():
            self.config.set("main", key, str(val))

        with self.conf_path.open('w') as f:
            self.config.write(f)

    def load(self):
        if not self.conf_path.exists():
            self.save()
            return

        self.config.read(self.conf_path)
        for key in self.settings:
            if self.config.has_option("main", key):
                val = self.config.get("main", key)
                self.settings[key] = val

    def get(self, setting):
        return self.settings.get(setting)

    def set(self, setting, value):
        self.settings[setting] = value
        self.save()
