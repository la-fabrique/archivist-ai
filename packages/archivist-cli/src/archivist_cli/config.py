from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml
from platformdirs import user_data_dir


@dataclass(frozen=True)
class AppConfig:
    referentiel: str | None = None
    root: str | None = None
    llm: str | None = None


def app_data_dir() -> Path:
    return Path(user_data_dir("archivist", "archivist"))


def load_config(data_dir: Path | None = None) -> AppConfig:
    dir_ = data_dir or app_data_dir()
    config_file = dir_ / "config.yaml"
    if not config_file.exists():
        return AppConfig()
    with config_file.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return AppConfig(
        referentiel=data.get("referentiel"),
        root=data.get("root"),
        llm=data.get("llm"),
    )


def save_config(config: AppConfig, data_dir: Path | None = None) -> None:
    dir_ = data_dir or app_data_dir()
    dir_.mkdir(parents=True, exist_ok=True)
    data: dict[str, str] = {}
    if config.referentiel is not None:
        data["referentiel"] = config.referentiel
    if config.root is not None:
        data["root"] = config.root
    if config.llm is not None:
        data["llm"] = config.llm
    with (dir_ / "config.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)
