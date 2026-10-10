from __future__ import annotations

import shutil
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname

from cli_core.adapters.config.yaml_file import YamlFileConfigStore
from platformdirs import user_data_dir


@dataclass(frozen=True)
class AppConfig:
    referentiel: str | None = None
    root: str | None = None
    llm: str | None = None


def app_data_dir() -> Path:
    return Path(user_data_dir("archivist", "archivist"))


def _store(data_dir: Path | None) -> YamlFileConfigStore:
    return YamlFileConfigStore("archivist", data_dir or app_data_dir())


def load_config(data_dir: Path | None = None) -> AppConfig:
    data = _store(data_dir).load()
    return AppConfig(
        referentiel=data.get("referentiel"),
        root=data.get("root"),
        llm=data.get("llm"),
    )


def save_config(config: AppConfig, data_dir: Path | None = None) -> None:
    data: dict[str, str] = {}
    if config.referentiel is not None:
        data["referentiel"] = config.referentiel
    if config.root is not None:
        data["root"] = config.root
    if config.llm is not None:
        data["llm"] = config.llm
    _store(data_dir).save(data)


def install_referentiel(source_uri: str, data_dir: Path | None = None) -> str:
    dir_ = data_dir or app_data_dir()
    parsed = urlparse(source_uri)
    dir_.mkdir(parents=True, exist_ok=True)
    dest = dir_ / "referentiel.yaml"
    if parsed.scheme == "file":
        source_path = Path(url2pathname(parsed.path))
        if not source_path.exists():
            raise FileNotFoundError(f"Référentiel source introuvable : {source_uri}")
        shutil.copy2(source_path, dest)
    elif parsed.scheme in ("http", "https"):
        try:
            urllib.request.urlretrieve(source_uri, dest)
        except Exception as e:
            raise ValueError(f"Impossible de télécharger le référentiel : {e}") from e
    else:
        raise ValueError(
            f"URI non supporté : {source_uri!r}. Utilisez file://, http:// ou https://."
        )
    return dest.as_uri()
