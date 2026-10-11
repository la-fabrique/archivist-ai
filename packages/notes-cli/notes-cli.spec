# -*- mode: python ; coding: utf-8 -*-
# Built with PyInstaller >=6.0.0 (see pyproject.toml [dependency-groups].dev)

a = Analysis(
    ['src/notes_cli/__main__.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'notes_cli.cli',
        'notes_cli.config',
        'notes_cli.registry',
        'notes_cli.domain.ports',
        'notes_cli.application.add_idea',
        'notes_cli.adapters.agent.claude_code',
        'cli_core.registry',
        'cli_core.domain.ports',
        'cli_core.adapters.config.yaml_file',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='notes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
)
