"""Exercise the original script without installing or starting input hooks."""
import contextlib
import io
from pathlib import Path
import runpy
import sys
from enum import Enum
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'src' / 'input_demo.py'

class Key(Enum):
    esc = 1
    space = 2
    backspace = 3
    enter = 4

def run_session(events, interrupt=False):
    state = {}
    class MouseListener:
        def __init__(self, on_click):
            state['click'] = on_click
        def start(self):
            state['started'] = True
        def stop(self):
            state['stopped'] = True
        def join(self):
            state['joined'] = True

    class KeyboardListener:
        def __init__(self, on_press):
            self.press = on_press
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def join(self):
            for event in events:
                if isinstance(event, tuple):
                    state['click'](0, 0, SimpleNamespace(name=event[0]), event[1])
                else:
                    key = SimpleNamespace(char=event) if isinstance(event, str) else event
                    if self.press(key) is False:
                        state['escape_stopped'] = True
                        break
            if interrupt:
                raise KeyboardInterrupt

    mock = ModuleType('pynput')
    mock.keyboard = SimpleNamespace(Key=Key, Listener=KeyboardListener)
    mock.mouse = SimpleNamespace(Listener=MouseListener)
    output = io.StringIO()
    with patch.dict(sys.modules, {'pynput': mock}), contextlib.redirect_stdout(output):
        runpy.run_path(str(SOURCE))
    return output.getvalue(), state

class InputDemoTests(unittest.TestCase):
    def test_digit_formatting_and_escape(self):
        output, state = run_session(list('ji42') + [Key.space, ('left', True), Key.esc, 'ignored'])
        expected = (SOURCE.parents[1] / 'examples' / 'session.txt').read_text()
        self.assertEqual(output, expected)
        self.assertTrue(state['escape_stopped'])
        self.assertTrue(state['stopped'])
        self.assertTrue(state['joined'])

    def test_special_keys_flush_and_mouse_release_is_ignored(self):
        output, _ = run_session(['a', Key.backspace, 'b', Key.enter, ('left', False), 'z', Key.esc])
        self.assertIn('a\n[BACKSPACE]\nb\n[ENTER]\nz\nMonitoring stopped.', output)
        self.assertNotIn('MOUSE', output)

    def test_interrupt_flushes_pending_word_and_cleans_up(self):
        output, state = run_session(list('pending'), interrupt=True)
        self.assertTrue(output.endswith('pending\nMonitoring stopped.\n'))
        self.assertTrue(state['started'])
        self.assertTrue(state['stopped'])
        self.assertTrue(state['joined'])

if __name__ == '__main__':
    unittest.main()
