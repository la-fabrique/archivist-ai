from pathlib import Path

import pytest

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.domain.ports import FilesystemError


def test_make_dir_creates_nested(tmp_path: Path):
    fs = LocalFilesystem()
    uri = f"file://{tmp_path}/a/b/c"
    fs.make_dir(uri)
    assert (tmp_path / "a" / "b" / "c").is_dir()


def test_make_dir_idempotent(tmp_path: Path):
    fs = LocalFilesystem()
    uri = f"file://{tmp_path}/a"
    fs.make_dir(uri)
    fs.make_dir(uri)
    assert (tmp_path / "a").is_dir()


def test_exists_true(tmp_path: Path):
    fs = LocalFilesystem()
    (tmp_path / "x").mkdir()
    assert fs.exists(f"file://{tmp_path}/x") is True


def test_exists_false(tmp_path: Path):
    fs = LocalFilesystem()
    assert fs.exists(f"file://{tmp_path}/nope") is False


def test_is_dir_true(tmp_path: Path):
    fs = LocalFilesystem()
    (tmp_path / "d").mkdir()
    assert fs.is_dir(f"file://{tmp_path}/d") is True


def test_is_dir_false_on_file(tmp_path: Path):
    fs = LocalFilesystem()
    (tmp_path / "f").write_text("x")
    assert fs.is_dir(f"file://{tmp_path}/f") is False


def test_make_dir_raises_on_file_conflict(tmp_path: Path):
    fs = LocalFilesystem()
    (tmp_path / "conflict").write_text("x")
    with pytest.raises(FilesystemError, match="exists.*not a directory"):
        fs.make_dir(f"file://{tmp_path}/conflict")


def test_rejects_non_file_scheme():
    fs = LocalFilesystem()
    with pytest.raises(FilesystemError, match="unsupported scheme"):
        fs.make_dir("s3://bucket/path")


@pytest.mark.parametrize("traversal_uri", [
    "file:///archive/../../../etc/passwd",
    "file:///archive/sub/../../secret",
    "file:///docs/../.ssh/id_rsa",
    "file:///../root",
])
def test_rejects_path_traversal_make_dir(traversal_uri: str):
    fs = LocalFilesystem()
    with pytest.raises(FilesystemError, match="traversal"):
        fs.make_dir(traversal_uri)


def test_rejects_path_traversal_zip_src():
    fs = LocalFilesystem()
    with pytest.raises(FilesystemError, match="traversal"):
        fs.zip_file("file:///archive/../secret.pdf", "file:///archive/out.zip")


def test_rejects_path_traversal_zip_dest():
    fs = LocalFilesystem()
    with pytest.raises(FilesystemError, match="traversal"):
        fs.zip_file("file:///archive/src.pdf", "file:///archive/../../out.zip")


def test_rejects_path_traversal_move_src():
    fs = LocalFilesystem()
    with pytest.raises(FilesystemError, match="traversal"):
        fs.move_file("file:///archive/../../../etc/hosts", "file:///archive/dest.txt")


def test_rejects_path_traversal_move_dest():
    fs = LocalFilesystem()
    with pytest.raises(FilesystemError, match="traversal"):
        fs.move_file("file:///archive/src.txt", "file:///archive/../../../etc/hosts")


def test_rejects_path_traversal_delete():
    fs = LocalFilesystem()
    with pytest.raises(FilesystemError, match="traversal"):
        fs.delete_file("file:///archive/../../../etc/hosts")


def test_normal_nested_path_accepted(tmp_path: Path):
    fs = LocalFilesystem()
    uri = f"file://{tmp_path}/a/b/c"
    fs.make_dir(uri)
    assert (tmp_path / "a" / "b" / "c").is_dir()
