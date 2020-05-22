import steamclient as steam
import sys
import os

# Settings
SCUMMVM_EXE = "C:/Program Files/ScummVM/scummvm.exe"

# Get a list of Steam users.
users = steam.get_users()

# Make sure someone is logged in.
if len(users) == 0:
    print("No users detected. Are you logged into Steam?")
    sys.exit(1)

user = users[0]
shortcuts = user.shortcuts

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [path to folder containing ScummVM games]")
    sys.exit(2)

# First argument is the path containing games.
root = sys.argv[1]
if not os.path.isdir(root):
    print(f"Input path is not a directory: {root}")
    sys.exit(3)

# Find all subdirectories in the given path.
for path in os.listdir(root):
    path = os.path.join(root, path)

    # Skip files.
    if not os.path.isdir(path):
        continue

    # Folder name is the game name.
    name = os.path.basename(path)
    icon = os.path.join(path, "icon.png")
    grid = os.path.join(path, "grid.png")
    hero = os.path.join(path, "hero.png")
    logo = os.path.join(path, "logo.png")

    print(f"Adding shortcut for {name}")

    # Set the icon only if it exists.
    if not os.path.isfile(icon):
        icon = ""

    # Add the shortcut.
    res = user.add_shortcut(
        name=name,
        exe=SCUMMVM_EXE, 
        start_dir=os.path.dirname(SCUMMVM_EXE),
        icon=icon, 
        shortcut_path="",
        launch_options=f"--path={os.path.realpath(path)}",
        tags=["ScummVM"])
    if res == 0:
        print("  - Success")
    if res == 1:
        print("  - Shortcut already exists!")
    elif res == 2:
        print("  - Something went wrong (name/exe is empty)")
        sys.exit(4)

    for shortcut in user.shortcuts:
        if shortcut.name == name:
            if os.path.isfile(grid):
                shortcut.set_grid(grid)
                print(f"  - Set the grid image: {grid}")
            if os.path.isfile(hero):
                shortcut.set_hero(hero)
                print(f"  - Set the hero image: {hero}")
            if os.path.isfile(logo):
                print(f"  - Set the logo image: {logo}")
                shortcut.set_logo(logo)

print("Done! Restart Steam to see changes.")