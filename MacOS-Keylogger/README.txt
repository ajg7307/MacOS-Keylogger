MacOS-Keylogger

A visible keyboard and mouse event logger for Apple Silicon.

Observe keyboard and mouse events in a visible terminal session, replace digits with markers, and stop monitoring with Escape. This cybersecurity portfolio project explores event callbacks, shared state, macOS privacy permissions, and standalone Python packaging.

Platform: macOS / ARM64 · Library: pynput · Output: standard output

Plain-text README (README.txt) · Build notes (docs/BUILD.md) · Example output (examples/session.txt)

Demo

Typing ji42, then pressing Space, clicking the left mouse button, and pressing Escape produces:

Monitoring ACTIVE — press Escape to stop.
ji[DIGIT ENTERED][DIGIT ENTERED][SPACE]
[MOUSE LEFT CLICK]
Monitoring stopped.

This is a synthetic example. The exact formatting comes from the supplied source: digit markers are printed without a newline.

What it does

| Input | Output |
| --- | --- |
| Printable letters and punctuation | Buffered until a flush event |
| Digits | [DIGIT ENTERED] for each digit |
| Space / Backspace | Flushes the buffer and prints the corresponding marker |
| Other special keys | Flushes the buffer and prints the key name |
| Mouse-button press | Flushes the buffer and prints the button name |
| Escape | Flushes the buffer and stops monitoring |

The program observes input across applications. Run it only on a system where you have explicit permission, using dummy text. Digit masking is a display transformation, not comprehensive redaction: letters and punctuation may still contain sensitive information.

Run from source

Use an ARM64 Python installation on an Apple Silicon Mac. The original build used Python 3.9.6; a compatible environment is required for the pinned native dependencies.

python3 -c 'import platform; print(platform.machine())'
Expected: arm64
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/input_demo.py

macOS may require authorization for your terminal or launching application in System Settings → Privacy & Security → Input Monitoring / Accessibility. Restart that application after changing permissions. See Apple's input monitoring guide (https://support.apple.com/en-euro/guide/mac-help/mchl4cedafb6/27/mac/27) and pynput's platform limitations (https://pynput.readthedocs.io/en/latest/limitations.html).

Press Escape to stop. The script also handles a keyboard interrupt.

Save a local transcript

The program itself only prints to the terminal. To display and save a session:

mkdir -p logs
python src/input_demo.py | tee logs/session.txt

Use tee -a logs/session.txt to append instead of overwriting. From an extracted standalone package, use ./InputDemo | tee output.txt; that file is created in the current directory. Local logs are excluded from this repository by .gitignore.

Build the standalone Mac executable

On an Apple Silicon Mac:

bash scripts/build_macos.sh

The build creates dist/InputDemo-AppleSilicon.zip. Extract it and double-click Start Input Demo.command, or run ./InputDemo in Terminal from the extracted folder. Python and dependencies are bundled; recipients do not need to install them separately.

The binary uses an ad-hoc signature. It is not Developer ID signed or notarized, and macOS may block a downloaded copy. Packaging does not remove privacy-permission requirements. See build details (docs/BUILD.md).

Engineering notes

The source is intentionally preserved exactly as supplied. This is a small demonstration with documented limitations:

- Concurrency: only the Escape branch of the keyboard callback holds the lock. Other keyboard events can race with the mouse callback while accessing the shared buffer.
- Text semantics: Backspace records an event rather than editing previously buffered text. This is an event stream, not a reconstruction of final text.
- Readiness: the startup banner prints before listeners have established that monitoring is available.
- Startup cleanup: the mouse listener starts before the try block; an exception during that start is outside the cleanup handler.
- Coverage: protected input, keyboard layouts, and OS permission behavior may affect the events available to the program. This project makes no claim to capture every input.

Possible future improvements include protecting all buffer operations with the same lock, explicit readiness/error reporting, and an optional mode restricted to a dedicated test window. These are proposals, not implemented features.

Validation

python3 -m unittest discover -s tests -v

Tests substitute synthetic listeners and do not capture real keyboard or mouse input. They check output formatting, Escape behavior, and cleanup after normal completion and interruption. GitHub Actions runs these tests and syntax checks.

The initial executable was built on macOS 26.6.2 / ARM64; its architecture and ad-hoc signature were verified. A user-provided screenshot shows input events and the stopped message during a local run. Other macOS versions and separate machines have not been verified. Synthetic tests do not validate the macOS input backend or resolve the known concurrency issue.

Repository layout

src/input_demo.py              Original monitoring script
scripts/build_macos.sh         ARM64 packaging script
scripts/Start Input Demo.command
tests/test_input_demo.py       Synthetic listener tests
examples/session.txt          Synthetic output example
docs/BUILD.md                 Packaging and release notes
requirements.txt              Runtime dependencies
requirements-build.txt        Pinned original build environment

Built with pynput (https://pynput.readthedocs.io/) and PyInstaller (https://pyinstaller.org/). Dependency licenses remain with their respective authors. No project license has been selected yet.
