from threading import Lock
from pynput import keyboard, mouse
word = []
lock = Lock()
def flush_word():
    if word:
        print("".join(word), flush=True)
        word.clear()
def on_press(key):
    with lock:
        if key == keyboard.Key.esc:
            flush_word()
            return False
    if key == keyboard.Key.space:
        flush_word()
        print("[SPACE]", flush=True)
    elif key == keyboard.Key.backspace:
        flush_word()
        print("[BACKSPACE]", flush=True)
    else:
        char = getattr(key, "char", None)
        if char and char.isdigit():
            if word:
                print("".join(word), end="", flush=True)
                word.clear()
            print("[DIGIT ENTERED]", end="", flush=True)
        elif char and char.isprintable():
            word.append(char)
        else:
            flush_word()
            name = getattr(key, "name", str(key))
            print(f"[{name.upper()}]", flush=True)
def on_click(x, y, button, pressed):
    if pressed:
        with lock:
            flush_word()
            print(f"[MOUSE {button.name.upper()} CLICK]", flush=True)
print("Monitoring ACTIVE — press Escape to stop.", flush=True)
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()
try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    pass
finally:
    mouse_listener.stop()
    mouse_listener.join()
    with lock:
        flush_word()
    print("Monitoring stopped.", flush=True)
