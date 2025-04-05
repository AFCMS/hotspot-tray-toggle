import subprocess
import threading

import PIL.Image
import PIL.ImageDraw
import pystray

state = {'on': False}


def on_callback(icon: pystray.Icon, item):
    state['on'] = True
    subprocess.run(["nmcli", "connection", "up", "Hotspot"])
    update_icon(icon)
    print("Switched ON")


def off_callback(icon: pystray.Icon, item):
    state['on'] = False
    subprocess.run(["nmcli", "connection", "down", "Hotspot"])
    update_icon(icon)
    print("Switched OFF")


# Create icons
icon_off = PIL.Image.new("RGBA", (64, 64), (255, 255, 255, 0))
draw = PIL.ImageDraw.Draw(icon_off)
draw.ellipse((0, 0, 64, 64), fill=(255, 255, 255))
draw.ellipse((16, 16, 48, 48), fill='red')

icon_on = PIL.Image.new("RGBA", (64, 64), (255, 255, 255, 0))
draw = PIL.ImageDraw.Draw(icon_on)
draw.ellipse((0, 0, 64, 64), fill=(255, 255, 255))
draw.ellipse((16, 16, 48, 48), fill='green')

# Create menus
menu_off = pystray.Menu(pystray.MenuItem("Turn ON", on_callback))

menu_on = pystray.Menu(pystray.MenuItem("Turn OFF", off_callback))


def update_icon(icon: pystray.Icon):
    if state['on']:
        icon.icon = icon_on
        icon.menu = menu_on
    else:
        icon.icon = icon_off
        icon.menu = menu_off


def run_tray():
    icon = pystray.Icon("Toggle Hotspot")

    if not icon.HAS_MENU:
        print("Menu not supported on this platform.")
        return

    update_icon(icon)

    icon.run()


threading.Thread(target=run_tray, daemon=True).start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
