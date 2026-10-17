# Packaging and release notes

The original package was built with Python 3.9.6, pynput 1.8.2, PyObjC 11.1, and PyInstaller 6.22.3 on macOS 26.6.2 / ARM64. Exact dependency versions are recorded in `requirements-build.txt`. PyObjC is pinned to avoid resolving a release incompatible with the original Python environment.

Run `bash scripts/build_macos.sh` from the repository. Set `PYTHON=/absolute/path/to/python3` to select an interpreter. The script checks that Python reports ARM64, creates a local build environment, and packages the source with the Darwin keyboard and mouse backends included explicitly.

## Distribution

The standalone console binary is named `InputDemo`; a `.exe` extension is not used on macOS. The `.command` launcher opens it through Terminal and waits for Return after it exits. The source program stops on Escape.

The generated ZIP belongs in a GitHub Release rather than Git history. Attach `InputDemo-AppleSilicon.zip` and `SHA256SUMS` to the release. Release notes should state the build platform, verification performed, known race condition, and that the binary is ad-hoc signed and not notarized. Do not claim support for untested macOS releases.

## Verification

```sh
python3 -m unittest discover -s tests -v
file dist/InputDemo-AppleSilicon/InputDemo
codesign --verify --strict --verbose=2 dist/InputDemo-AppleSilicon/InputDemo
shasum -a 256 dist/InputDemo-AppleSilicon.zip
```

For a manual test, run the package in an authorized test session, enter synthetic text, click once, and press Escape. Confirm the stopped message appears. Test the actual downloaded release on a separate Mac before claiming distributable compatibility. Check the dependency licenses before distributing binaries publicly.

## Troubleshooting

- **No input:** check the launching application's macOS privacy permissions and restart it after changes. The active banner alone does not establish readiness.
- **Blocked download:** the package is not notarized. Follow your organization's software policy; this repository does not disable platform protections.
- **Unexpected formatting:** digits deliberately print without a newline; Backspace records an event, and mouse clicks flush buffered text.
- **No saved file:** output goes to the terminal unless explicitly redirected with `tee` or another shell redirection.

See the [PyInstaller manual](https://pyinstaller.org/en/stable/usage.html) for packaging options.
