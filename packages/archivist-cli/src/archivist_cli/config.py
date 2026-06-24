from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname

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


def install_referentiel(source_uri: str, data_dir: Path | None = None) -> str:
    dir_ = data_dir or app_data_dir()
    parsed = urlparse(source_uri)
    if parsed.scheme != "file":
        raise ValueError(f"URI non supporté : {source_uri!r}. Seuls les URI file:// sont acceptés.")
    source_path = Path(url2pathname(parsed.path))
    if not source_path.exists():
        raise FileNotFoundError(f"Référentiel source introuvable : {source_uri}")
    dir_.mkdir(parents=True, exist_ok=True)
    dest = dir_ / "referentiel.yaml"
    shutil.copy2(source_path, dest)
    return dest.as_uri()
