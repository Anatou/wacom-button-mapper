import os, json, subprocess
from pynput import keyboard
 
default_settings= {
    "pad": {
        1: "key +ctrl s -ctrl",
        2: "key +ctrl +shift z -ctrl -shift",
        3: "key +ctrl z -ctrl",
        8: "key +alt", # for some reason button 4 is 8 but this is button 4
    },
    "pen": {
        1: "button +1", # left click
        2: "button +2", # middle click
        3: "button +3", # right click
    },
    "settings": {
        "pad-name": "Wacom Intuos BT M Pad pad",
        "pen-name": "Wacom Intuos BT M Pen stylus",
    }
}

def read_settings():
    with open('./wacom-settings.json', 'r') as settings_file:
        return json.load(settings_file)

def save_settings(settings):
    with open('./wacom-settings.json', 'w') as settings_file:
        json.dump(settings, settings_file)


def apply_settings(settings):
    for btn, sett in settings["pad"].items():
        subprocess.run(["xsetwacom", "set", f"{settings['settings']['pad-name']}", "Button", btn, sett])
    for btn, sett in settings["pen"].items():
        subprocess.run(["xsetwacom", "set", f"{settings['settings']['pen-name']}", "Button", btn, sett])
    print("If no error code above, settings have been applied successfully")

def print_settings(settings):
    print("The current settings are:")
    print(f"Pad: {settings['settings']['pad-name']}")
    print(f"  - button 1: {settings['pad']['1']}")
    print(f"  - button 2: {settings['pad']['2']}")
    print(f"  - button 3: {settings['pad']['3']}")
    print(f"  - button 4: {settings['pad']['8']}")
    print(f"Pen: {settings['settings']['pen-name']}")
    print(f"  - button 1: {settings['pen']['1']}")
    print(f"  - button 2: {settings['pen']['2']}")
    print(f"  - button 3: {settings['pen']['3']}")

def set_settings(settings):
    # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #     print(listener, end=" ")
    #     listener.join()
    while True:
        print("\n")
        print("Which button to map\n")
        inp = ""
        while inp not in ["pad1", "pad2", "pad3", "pad4", "pen1", "pen2", "pen3", "b", "q"]:
            print("pad1: Left most button of the pad")
            print("pad2: Center left button of the pad")
            print("pad3: Center right button of the pad")
            print("pad8: Right most button of the pad")
            print("pen1: Drawing button of the pen (I don't recommand to change it)")
            print("pen2: Small button of the pen")
            print("pen3: Big button of the pen")
            print("b: Save and back")
            print("q: Save and quit")
            inp = input("? ")

        if inp == "q": 
            save_settings(settings)
            apply_settings(settings)
            exit()
        if inp == "b": 
            save_settings(settings)
            apply_settings(settings)
            return
        else: 
            print("\n")
            print("Leave blank to reset to default")
            to_map = ""
            modifiers = {
                str(keyboard.Key.shift): ["shift",0],
                str(keyboard.Key.shift_r): ["shift_r", 0],
                str(keyboard.Key.ctrl): ["ctrl", 0],
                str(keyboard.Key.ctrl_r): ["ctrl_r", 0],
                str(keyboard.Key.enter): ["enter", 0],
                str(keyboard.Key.alt): ["alt", 0],
                str(keyboard.Key.caps_lock): ["caps_lock", 0],
                str(keyboard.Key.tab): ["tab", 0],
                str(keyboard.Key.space): ["space", 0],
            }
            count_event = 1
            with keyboard.Events() as events:
                for event in events:
                    if event.key == keyboard.Key.esc:
                        break
                    else:
                        if count_event==0: 
                            if str(event.key) in modifiers.keys():
                                sign = "+" if modifiers[str(event.key)][1]==0 else "-"
                                to_map += sign+modifiers[str(event.key)][0]+" "
                                print(sign+modifiers[str(event.key)][0], end=" ")
                                modifiers[str(event.key)][1] = (modifiers[str(event.key)][1]+1)%2
                            else:
                                to_map += str(event.key)[1]+" "

                        count_event = (count_event+1)%2
                        
            print(to_map)
            if to_map == "": 
                settings[inp[:3]][inp[3:]] = default_settings[inp[:3]][inp[3:]]
                print(f"\nButton resetted to default: \"{default_settings[inp[:3]][inp[3:]]}\"")
            else:
                settings[inp[:3]][inp[3:]] = "key "+to_map
                print(f"\nButton successfuly changed to: \"{'key '+to_map}\"")
            print("Use b to back and apply settings")



def set_app_settings():
    pass


if os.path.isfile('./wacom-settings.json'):
    # if settings file already exists, read it
    settings = read_settings()
else:
    # else create it with default settings
    save_settings(default_settings)


print(" _    _                            ______       _   _               ___  ___                            ")
print("| |  | |                           | ___ \     | | | |              |  \/  |                            ")
print("| |  | | __ _  ___ ___  _ __ ___   | |_/ /_   _| |_| |_ ___  _ __   | .  . | __ _ _ __  _ __   ___ _ __ ")
print("| |/\| |/ _` |/ __/ _ \| '_ ` _ \  | ___ \ | | | __| __/ _ \| '_ \  | |\/| |/ _` | '_ \| '_ \ / _ \ '__|")
print("\  /\  / (_| | (_| (_) | | | | | | | |_/ / |_| | |_| || (_) | | | | | |  | | (_| | |_) | |_) |  __/ |   ")
print(" \/  \/ \__,_|\___\___/|_| |_| |_| \____/ \__,_|\__|\__\___/|_| |_| \_|  |_/\__,_| .__/| .__/ \___|_|   ")
print("                                                                                 | |   | |              ")
print("                                                                                 |_|   |_|              ")
print("")
print_settings(settings)

while True:
    inp = ""
    while inp not in ["a", "c", "s", "h", "q"]:
        print("\n\n")
        print("a: apply current settings")
        print("c: change bindings")
        print("s: app settings")
        print("p: print current settings")
        print("q: quit")
        print("")
        inp = input("? ")
    if inp == "a":
        apply_settings(settings)
    if inp == "c":
        set_settings(settings)
    if inp == "s":
        set_app_settings()
    if inp == "p":
        print_settings(settings)
    if inp == "q":
        exit()

