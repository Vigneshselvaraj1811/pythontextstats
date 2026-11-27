"""Verify that a release tag matches both package version declarations."""

import ast
import sys
import tomllib
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/check_release.py vVERSION", file=sys.stderr)
        return 2

    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    version = project["project"]["version"]
    tag = sys.argv[1]
    package_source = ast.parse(
        Path("pythontextstats/__init__.py").read_text(encoding="utf-8")
    )
    package_version = next(
        ast.literal_eval(node.value)
        for node in package_source.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "__version__"
            for target in node.targets
        )
    )
    if package_version != version:
        print("Package and pyproject.toml versions differ", file=sys.stderr)
        return 1
    if tag != f"v{version}":
        print(f"Tag {tag!r} must be v{version}", file=sys.stderr)
        return 1
    print(f"Release version verified: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
