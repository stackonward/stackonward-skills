#!/usr/bin/env python3
"""Validate the public files and build local distribution archives."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = (
    ".gitignore", "README.md", "LICENSE", "NOTICE.md", "CHANGELOG.md",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md",
)
PUBLIC_DIRS = (".github", "docs", "scripts", "skills")
IGNORED_PARTS = {".DS_Store", "__pycache__"}
PRIVATE_PARTS = {".git", ".private", ".runtime", "node_modules", "vendor"}
PRIVATE_FILES = {
    "account.json", "portal-account.json", "privacy-account.json",
    "signing-secrets.json", "review-credentials.json", "testers.json",
}
PRIVATE_SUFFIXES = {".p8", ".p12", ".pem", ".key", ".mobileprovision", ".ipa"}
IOS_SKILL = Path("skills/ios-app-delivery")
IOS_DELIVERY = Path("assets/starter/delivery/apple")
APPLE_CLI = ("npx", "--yes", "@stackonward/cli@1.10.0", "apple")
MARKDOWN_LINK = re.compile(r"\]\(([^)\s]+)\)")
SECRET = re.compile(
    rb"-----BEGIN [A-Z ]*PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{36}\b"
    rb"|\bgithub_pat_[A-Za-z0-9_]{30,}\b"
)


def read_public_files():
    paths = [ROOT / name for name in ROOT_FILES]
    for directory in PUBLIC_DIRS:
        location = ROOT / directory
        if location.is_symlink() or not location.is_dir():
            raise ValueError(f"Expected a regular distribution directory: {directory}")
        paths.extend(location.rglob("*"))

    files = {}
    for path in paths:
        relative = path.relative_to(ROOT)
        if IGNORED_PARTS.intersection(relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Symbolic link in the distribution: {relative}")
        if PRIVATE_PARTS.intersection(relative.parts) or any(
            part.endswith(".xcarchive") for part in relative.parts
        ):
            raise ValueError(f"Private or generated directory in the distribution: {relative}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f"Expected a regular distribution file: {relative}")
        if (
            relative.name in PRIVATE_FILES
            or relative.suffix.lower() in PRIVATE_SUFFIXES
            or relative.name.endswith(("-session.yml", "-session.yaml", ".plan.json", ".receipt.json"))
            or relative.name == ".env"
            or (relative.name.startswith(".env.") and relative.name != ".env.example")
        ):
            raise ValueError(f"Private file in the distribution: {relative}")
        contents = path.read_bytes()
        if SECRET.search(contents):
            raise ValueError(f"Credential pattern in the distribution: {relative}")
        if path.suffix == ".json":
            try:
                json.loads(contents)
            except (ValueError, UnicodeError) as error:
                raise ValueError(f"Invalid JSON in {relative}: {error}") from error
        files[relative] = contents
    return files


def verify_skills(files):
    skills = {}
    for manifest, content in sorted(files.items()):
        if manifest.match("skills/*/SKILL.md") and len(manifest.parts) == 3:
            folder = manifest.parent
            parts = content.decode().split("---", 2)
            if len(parts) != 3 or parts[0]:
                raise ValueError(f"Missing YAML frontmatter in {manifest}")
            name = re.search(r"(?m)^name:\s*(\S+)\s*$", parts[1])
            if not name or name[1].strip("\"'") != folder.name:
                raise ValueError(f"Skill name must match its folder: {manifest}")
            if not re.search(r"(?m)^license:\s*MIT\s*$", parts[1]):
                raise ValueError(f"Expected license: MIT in {manifest}")
            if files.get(folder / "LICENSE") != files[Path("LICENSE")]:
                raise ValueError(f"Bundle the repository license in {folder}")
            skills[folder] = {
                path.relative_to(folder): data for path, data in files.items()
                if path.is_relative_to(folder)
            }
    if not skills:
        raise ValueError("No skills found under skills/.")
    return skills


def verify_links(files, skills):
    for path, content in files.items():
        if path.suffix != ".md":
            continue
        scope = next((folder for folder in skills if path.is_relative_to(folder)), Path("."))
        paths_in_scope = {file for file in files if file.is_relative_to(scope)}
        for match in MARKDOWN_LINK.finditer(content.decode()):
            link = urlsplit(match[1])
            if link.scheme or link.netloc or not link.path:
                continue
            target = (ROOT / path.parent / unquote(link.path)).resolve()
            if not target.is_relative_to(ROOT / scope):
                raise ValueError(f"Link outside the distribution scope in {path}: {match[1]}")
            relative = target.relative_to(ROOT)
            if relative not in paths_in_scope and not any(
                file.is_relative_to(relative) for file in paths_in_scope
            ):
                raise ValueError(f"Broken relative link in {path}: {match[1]}")


def verify_cli_examples(skill_files):
    with tempfile.TemporaryDirectory(prefix="stackonward-ios-check-") as temporary:
        sandbox = Path(temporary)
        project = sandbox / "example-project"
        delivery = project / "delivery/apple"
        for relative, content in skill_files.items():
            if relative.is_relative_to(IOS_DELIVERY):
                destination = delivery / relative.relative_to(IOS_DELIVERY)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(content)

        def apple(*args):
            result = subprocess.run(
                (*APPLE_CLI, *args), cwd=project, check=True, capture_output=True,
                text=True, timeout=120,
            )
            return json.loads(result.stdout)

        generated = sandbox / "generated"
        apple("init", str(generated), "--bundle-id", "com.example.yourapp", "--name", "Your App")
        for name in ("manifest.schema.json", "Gemfile", "Gemfile.lock", ".gitignore"):
            if (generated / name).read_bytes() != (delivery / name).read_bytes():
                raise ValueError(f"Starter {name} differs from the pinned CLI's output")

        def preflight(scope, intent):
            result = apple(
                "preflight", "--manifest", "delivery/apple/app.json", "--scope", scope,
                "--intent", intent, "--offline", "--json",
            )
            if result.get("outcome") != "verified" or result.get("remoteVerified") is not False:
                raise ValueError(f"Expected successful offline preflight for {scope}/{intent}")

        preflight("metadata", "reconcile")
        config = project / "config/public.release.json"
        config.parent.mkdir()
        shutil.copyfile(delivery / "examples/public.release.json", config)
        for kind in ("xcode", "flutter"):
            shutil.copyfile(delivery / f"examples/app.{kind}.json", delivery / "app.json")
            preflight("build", "archive")


def write_zip(destination, prefix, files, directories):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for directory in sorted(directories):
            info = zipfile.ZipInfo(f"{prefix}/{directory.as_posix()}/")
            info.create_system = 3
            info.external_attr = (0o40755 << 16) | 0x10
            archive.writestr(info, b"")
        for path, content in sorted(files.items()):
            info = zipfile.ZipInfo(f"{prefix}/{path.as_posix()}")
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValueError(f"Unreadable archive: {destination.name}")


def package(output, files, skills):
    example_dirs = [IOS_DELIVERY / name for name in ("artwork", "screenshots", "previews")]
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".package-", dir=output) as temporary:
        workspace = Path(temporary)
        for folder, skill_files in skills.items():
            write_zip(
                workspace / f"{folder.name}.zip", folder.name, skill_files,
                example_dirs if folder == IOS_SKILL else [],
            )
        write_zip(
            workspace / "stackonward-skills.zip", "stackonward-skills", files,
            [IOS_SKILL / directory for directory in example_dirs] if IOS_SKILL in skills else [],
        )
        hashes = []
        for archive in sorted(workspace.glob("*.zip")):
            sha = hashlib.sha256(archive.read_bytes()).hexdigest()
            hashes.append(f"{sha}  {archive.name}\n")
        (workspace / "SHA256SUMS").write_text("".join(hashes), encoding="utf-8")
        for artifact in sorted(workspace.iterdir()):
            artifact.replace(output / artifact.name)
            print(output / artifact.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--verify-cli", action="store_true", help="run offline checks with the pinned npm CLI")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    try:
        if any(output.is_relative_to(ROOT / name) for name in PUBLIC_DIRS):
            raise ValueError("Choose an output folder outside the public source directories")
        files = read_public_files()
        skills = verify_skills(files)
        verify_links(files, skills)
        if args.verify_cli and IOS_SKILL in skills:
            verify_cli_examples(skills[IOS_SKILL])
            print("CLI 1.10.0: starter resources, metadata, Xcode and Flutter offline checks passed.")
        package(output, files, skills)
        print(f"Validated and packaged {len(skills)} skill(s).")
    except subprocess.CalledProcessError as error:
        parser.exit(1, f"CLI validation failed: {error.stderr or error.stdout or error}\n")
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        parser.exit(1, f"Packaging failed: {error}\n")


if __name__ == "__main__":
    main()
