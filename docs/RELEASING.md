# Releasing to PyPI

The `publish.yml` workflow builds a source distribution and wheel, runs the
test suite, checks distribution metadata, and uploads through PyPI Trusted
Publishing. It runs when a `vVERSION` tag is pushed. The tag must match the
versions in `pyproject.toml` and `pythontextstats/__init__.py` and point to a
commit on `main`.

## One-time PyPI setup

As a project owner, open the PyPI project's **Manage → Publishing** page and
add a GitHub Actions Trusted Publisher with:

| Field | Value |
| --- | --- |
| GitHub owner | `Vigneshselvaraj1811` |
| Repository | `pythontextstats` |
| Workflow filename | `publish.yml` |
| Environment | `pypi` |

Create a GitHub environment named `pypi` in the repository settings. The
environment name must match the PyPI configuration. Restrict who may approve
deployments if your repository uses multiple maintainers.

## Release checklist

1. Decide whether this is a preview or stable release. Update the version in
   both `pyproject.toml` and `pythontextstats/__init__.py`, then update the
   README, migration guide, and changelog release status.
2. Run `python -m unittest discover -s tests -v`.
3. Run `python -m build` and `python -m twine check dist/*` locally when
   build tools are available. CI repeats these checks.
4. Merge the release changes into `main` and wait for CI to pass.
5. Tag the exact release commit: `git tag vVERSION && git push origin vVERSION`.
6. Watch the **Publish to PyPI** workflow. Once it succeeds, verify the
   release and files at `https://pypi.org/project/pythontextstats/VERSION/`.

PyPI does not allow replacing an uploaded file for the same version. If the
upload or package needs correction, increment the version and publish again.
Do not put PyPI API tokens in this repository or GitHub Actions secrets for
this workflow.
