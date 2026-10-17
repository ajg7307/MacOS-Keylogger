#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

python_bin="${PYTHON:-python3}"
if [[ "$(uname -s)" != Darwin ]] || [[ "$("$python_bin" -c 'import platform; print(platform.machine())')" != arm64 ]]; then
  echo 'Build requires macOS and an ARM64 Python interpreter.' >&2
  exit 1
fi

"$python_bin" -m venv .build-venv
.build-venv/bin/python -m pip install -r requirements-build.txt
export PYINSTALLER_CONFIG_DIR="$PWD/build/pyinstaller-cache"
.build-venv/bin/python -m PyInstaller \
  --noconfirm --clean --onefile --console --target-arch arm64 \
  --name InputDemo \
  --hidden-import pynput.keyboard._darwin \
  --hidden-import pynput.mouse._darwin \
  --distpath dist/InputDemo-AppleSilicon \
  --workpath build/pyinstaller --specpath build \
  src/input_demo.py
cp 'scripts/Start Input Demo.command' dist/InputDemo-AppleSilicon/
cp README.md README.txt requirements-build.txt dist/InputDemo-AppleSilicon/
cp src/input_demo.py dist/InputDemo-AppleSilicon/
chmod +x 'dist/InputDemo-AppleSilicon/Start Input Demo.command'
file dist/InputDemo-AppleSilicon/InputDemo
codesign --verify --strict dist/InputDemo-AppleSilicon/InputDemo
ditto -c -k --keepParent --norsrc dist/InputDemo-AppleSilicon dist/InputDemo-AppleSilicon.zip
shasum -a 256 dist/InputDemo-AppleSilicon.zip > dist/SHA256SUMS
echo 'Created dist/InputDemo-AppleSilicon.zip and dist/SHA256SUMS'
