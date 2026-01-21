from collections import deque
import json
import os
# DEVICE CLASS (OOP + simple linked-list compatibility)
class Device:
    def __init__(self, name, default_setting=0):
        self.name = name
        self.is_on = False
        self.setting = default_setting
        self.next = None
        self.prev = None
    def to_dict(self):
        return {
            "name": self.name,
            "is_on": self.is_on,
            "setting": self.setting
        }
    @staticmethod
    def from_dict(data):
        d = Device(data["name"], data["setting"])
        d.is_on = data["is_on"]
        return d
    def __str__(self):
        if self.is_on:
            if self.name in ["AC", "Heater"]:
                return f"{self.name}: ON ({self.setting}°C)"
            elif self.name == "Fan":
                return f"{self.name}: ON (Speed {self.setting})"
            return f"{self.name}: ON"
        return f"{self.name}: OFF"
# DATA STRUCTURES
devices = {}                 # Dictionary (main storage)
history_log = []            # List (action history)
used_devices = set()        # Set (unique device usage)
voice_commands = deque()     # Queue (FIFO)
undo_stack = []             # Stack (LIFO)
# Files
DEVICES_FILE = "devices.json"
HISTORY_FILE = "history.txt"
# FILE HANDLING
def save_data():
    with open(DEVICES_FILE, "w") as f:
        json.dump({name: devices[name].to_dict() for name in devices}, f, indent=4)
    with open(HISTORY_FILE, "w") as f:
        for entry in history_log:
            f.write(entry + "\n")
    print("✓ Data saved successfully.\n")
def load_data():
    if os.path.exists(DEVICES_FILE):
        with open(DEVICES_FILE, "r") as f:
            data = json.load(f)
            for name in data:
                devices[name] = Device.from_dict(data[name])
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                history_log.append(line.strip())
# DSA FEATURES
def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
def search_device(name):
    name = name.lower()
    for key in devices:
        if key == name:
            return devices[key]
    return None
# DEVICE OPERATIONS
def show_devices():
    print("\nDEVICE STATUS")
    if not devices:
        print("No devices found.")
        return
    sorted_keys = bubble_sort(list(devices.keys()))
    for key in sorted_keys:
        print(devices[key])
    print("\n")
def add_device():
    name = input("Enter device name: ").strip()
    key = name.lower()
    if key in devices:
        print("Device already exists.\n")
        return
    default_setting = 0
    if name in ["AC", "Heater"]:
        default_setting = 22
    devices[key] = Device(name, default_setting)
    history_log.append(f"Added new device: {name}")
    print(f"✓ {name} successfully added.\n")
def delete_device():
    name = input("Enter device name to delete: ").lower()
    if name not in devices:
        print("Device not found.\n")
        return
    del devices[name]
    history_log.append(f"Deleted device: {name}")
    print(f"✓ {name} deleted.\n")
def turn_on(name):
    device = search_device(name)
    if not device:
        print("Device not found.\n")
        return
    if device.is_on:
        print(f"{device.name} is already ON.\n")
        return
    device.is_on = True
    undo_stack.append((device.name, "off"))
    used_devices.add(device.name)
    history_log.append(f"Turned ON: {device.name}")
    if device.name in ["AC", "Heater"]:
        device.setting = int(input("Set temperature: "))
    elif device.name == "Fan":
        device.setting = int(input("Set speed (1–5): "))
    print(f"✓ {device.name} is now ON.\n")
def turn_off(name):
    device = search_device(name)
    if not device:
        print("Device not found.\n")
        return
    if not device.is_on:
        print(f"{device.name} is already OFF.\n")
        return
    device.is_on = False
    undo_stack.append((device.name, "on"))
    used_devices.add(device.name)
    history_log.append(f"Turned OFF: {device.name}")
    print(f"✓ {device.name} is now OFF.\n")
# VOICE COMMAND SYSTEM (QUEUE)
def add_voice_command():
    cmd = input("Voice Command: ")
    voice_commands.append(cmd)
    print("✓ Voice command added.\n")
def process_voice_command():
    if not voice_commands:
        print("No voice commands.\n")
        return
    cmd = voice_commands.popleft()
    print(f"Processing: {cmd}")
    parts = cmd.lower().split()
    if "turn" in parts and "on" in parts:
        name = " ".join(parts[2:])
        turn_on(name)
    elif "turn" in parts and "off" in parts:
        name = " ".join(parts[2:])
        turn_off(name)
    else:
        print("Invalid command.\n")
# UNDO FEATURE (STACK)
def undo_action():
    if not undo_stack:
        print("Nothing to undo.\n")
        return
    name, action = undo_stack.pop()
    print(f"Undoing last action → {action.upper()} {name}")
    if action == "on":
        turn_on(name)
    else:
        turn_off(name)
# MAIN PROGRAM
def main():
    load_data()
    if not devices:
        devices.update({
            "light": Device("Light"),
            "fan": Device("Fan"),
            "tv": Device("TV"),
            "ac": Device("AC", 24),
            "heater": Device("Heater", 22)
        })
    print("\n SMART HOME AUTOMATION SYSTEM 9\n")
    while True:
        show_devices()
        print("Menu:")
        print("1. Turn ON/OFF Device")
        print("2. Add New Device")
        print("3. Delete Device")
        print("4. Add Voice Command")
        print("5. Process Voice Command")
        print("6. Undo Last Action")
        print("7. Show History")
        print("8. Save Data")
        print("9. Exit")
        choice = input("Select option: ")
        if choice == "1":
            name = input("Device name: ")
            action = input("ON or OFF: ").lower()
            turn_on(name) if action == "on" else turn_off(name)
        elif choice == "2":
            add_device()
        elif choice == "3":
            delete_device()
        elif choice == "4":
            add_voice_command()
        elif choice == "5":
            process_voice_command()
        elif choice == "6":
            undo_action()
        elif choice == "7":
            print("\nActivity History:")
            for h in history_log:
                print(" -", h)
            print()
        elif choice == "8":
            save_data()
        elif choice == "9":
            save_data()
            print("Exiting system...")
            break
        else:
            print("Invalid option.\n")
main()
