from configparser import ConfigParser
from pathlib import Path


class IniConfig:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.data = {}

        self._load()

    def _load(self):
        if not self.filepath.exists():
            raise FileNotFoundError(f"INI file not found: {self.filepath}")

        parser = ConfigParser()
        parser.read(self.filepath)

        for section in parser.sections():
            for key, value in parser.items(section):
                self.data[key.upper()] = self._auto_cast(value)

    def _auto_cast(self, value):
        """Convertit auto: int, float, bool ou laisse string"""
        v = value.strip()

        if v.lower() in ("true", "false"):
            return v.lower() == "true"

        try:
            return int(v)
        except ValueError:
            pass

        try:
            return float(v)
        except ValueError:
            pass

        return v

    # Permet: config["VAR"]
    def __getitem__(self, key):
        return self.data[key.upper()]

    # Optionnel: utiliser `in`
    def __contains__(self, key):
        return key.upper() in self.data

    # Optionnel: accéder avec .get_like un dict
    def get(self, key, default=None):
        return self.data.get(key.upper(), default)

    # Debug print
    def __repr__(self):
        return f"<IniConfig {self.filepath.name}: {len(self.data)} vars>"