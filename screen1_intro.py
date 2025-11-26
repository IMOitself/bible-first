print("\033[H\033[2J")  # Clear screen

import UI
UI.print_title()

print("\nPress any key to continue...")
input()

# install readchar once for all files if not installed
try:
    from readchar import readkey, key
except ImportError:
    import os
    print("\nwait lang pu...")
    os.system("python -m pip install readchar")

import screen2_menu
screen2_menu.start()