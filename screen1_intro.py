print("\033[H\033[2J")  # Clear screen
import UI
UI.print_title()
print("Press any key to continue...")
input()

import screen2_menu
screen2_menu.start()