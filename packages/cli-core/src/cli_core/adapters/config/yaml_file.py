from __future__ import annotations

from pathlib import Path

import yaml
from platformdirs import user_data_dir

from cli_core.domain.ports import ConfigError, ConfigStore


class YamlFileConfigStore(ConfigStore):
    def __init__(self, app_name: str, data_dir: Path | None = None) -> None:
        base = data_dir if data_dir is not None else Path(user_data_dir(app_name, app_name))
        self.path: Path = base / "config.yaml"

    def load(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        try:
            with self.path.open(encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigError(f"Config invalide ({self.path}) : {e}") from e
        except UnicodeDecodeError as e:
            raise ConfigError(f"Config invalide ({self.path}) : encodage UTF-8 attendu") from e
        except OSError as e:
            raise ConfigError(f"Lecture impossible ({self.path}) : {e}") from e
        if not isinstance(data, dict):
            raise ConfigError(f"Config invalide ({self.path}) : un mapping est attendu")
        result: dict[str, str] = {}
        for key, value in data.items():
            if value is None:
                continue
            if not isinstance(key, str) or not isinstance(value, str):
                raise ConfigError(
                    f"Config invalide ({self.path}) : la clé {key!r} doit avoir une valeur texte"
                )
            result[key] = value
        return result

    def save(self, data: dict[str, str]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, allow_unicode=True)
        except OSError as e:
            raise ConfigError(f"Écriture impossible ({self.path}) : {e}") from e
