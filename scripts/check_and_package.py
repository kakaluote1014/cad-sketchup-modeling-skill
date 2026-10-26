"""Check and package teaching files. Does not connect to MCP or install anything."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cad-sketchup-mcp"
VERSION = "0.1.2"
FILES = {
    "SKILL.md", "README.md", "agents/openai.yaml",
    "references/install-connect.md", "references/cad-preparation.md",
    "references/modeling.md", "references/sources.md", "references/validation.md",
    "references/advanced-execution.md",
    "references/practice.md", "assets/practice/practice-source.dxf",
    "assets/practice/practice-clean-reference.dxf", "assets/practice/plan-reference.png",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    actual = {p.relative_to(SKILL).as_posix() for p in SKILL.rglob("*") if p.is_file()}
    if actual != FILES:
        raise ValueError(f"Skill file list changed; review allowlist: {actual ^ FILES}")
    contents = {name: (SKILL / name).read_bytes() for name in sorted(FILES)}
    local_links = 0
    local_targets = []
    toml_examples = 0
    planned_archive = ROOT / "dist" / f"cad-sketchup-mcp-v{VERSION}.zip"
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", "_build", "__pycache__"} for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix not in {".md", ".yaml", ".json", ".py", ".dxf"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "\ufffd" in text or (path.suffix in {".md", ".yaml"} and "[TODO:" in text):
            raise ValueError(f"Bad encoding or unfinished scaffold: {path.relative_to(ROOT)}")
        if re.search(r"(?i)(?<![a-z])[a-z]:[\\/]|/(?:Users|home)/[\w.-]+/", text):
            raise ValueError(f"Personal absolute path: {path.relative_to(ROOT)}")
        if re.search(r"\b(?:sk-|gh[pousr]_|github_pat_)[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----", text):
            raise ValueError(f"Credential pattern: {path.relative_to(ROOT)}")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://")):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.is_relative_to(ROOT) or (not resolved.is_file() and resolved != planned_archive):
                    raise ValueError(f"Broken local reference: {path.relative_to(ROOT)} -> {target}")
                local_links += 1
                local_targets.append(resolved)
            for block in re.findall(r"```toml\n(.*?)\n```", text, re.S):
                server = tomllib.loads(block)["mcp_servers"]["sketchup"]
                if server["args"] != ["sketchup-mcp2==0.3.1"]:
                    raise ValueError("Review documented MCP version before changing the package")
                toml_examples += 1
    front = re.match(r"^---\nname: cad-sketchup-mcp\ndescription: [^\n]+\n---", contents["SKILL.md"].decode("utf-8").replace("\r\n", "\n"))
    if not front:
        raise ValueError("Skill manifest must contain its name and description")
    if toml_examples != 1:
        raise ValueError("Expected one documented TOML example")

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    archive = dist / f"cad-sketchup-mcp-v{VERSION}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in contents.items():
            info = zipfile.ZipInfo(f"cad-sketchup-mcp/{name}", (2026, 10, 26, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data)
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None or set(bundle.namelist()) != {f"cad-sketchup-mcp/{name}" for name in FILES}:
            raise ValueError("Archive integrity or member list failed")
        for name, data in contents.items():
            if bundle.read(f"cad-sketchup-mcp/{name}") != data:
                raise ValueError(f"Archive byte mismatch: {name}")
        destination = ROOT / "_build" / f"install-smoke-v{VERSION}" / ".agents" / "skills"
        if not destination.resolve().is_relative_to((ROOT / "_build").resolve()):
            raise ValueError("Install smoke must remain inside the isolated build directory")
        destination.mkdir(parents=True,exist_ok=True)
        bundle.extractall(destination)
        for name, data in contents.items():
            if (destination / "cad-sketchup-mcp" / name).read_bytes() != data:
                raise ValueError(f"Install smoke byte mismatch: {name}")
    checksum = digest(archive.read_bytes())
    if not all(path.is_file() for path in local_targets):
        raise ValueError("Local reference missing after packaging")
    archive.with_suffix(".zip.sha256").write_text(f"{checksum}  {archive.name}\n", encoding="ascii")
    report = {
        "version": VERSION, "status": "passed", "skill_files": len(FILES),
        "local_links": local_links, "toml_examples": toml_examples,
        "utf8_and_private_content_scan": "passed", "zip_members_and_bytes": "passed",
        "isolated_install_layout": "passed", "codex_ui_discovery": "not tested",
        "yaml_parser": "not run by this stdlib script; see initial validation",
        "live_mcp": "not tested for v0.1.2", "student_trial": "not tested for v0.1.2",
        "archive_sha256": checksum, "skill_sha256": {name: digest(data) for name, data in contents.items()},
    }
    (ROOT / "validation" / "package-check.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(FILES)} teaching files; {local_links} local links; {toml_examples} TOML example")
    print(f"Archive: {archive.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
