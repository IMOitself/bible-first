print("\033[2J\033[H")  # Clear screen
print("\nBASTA WELCOME\n")
print("Press any key to continue...")
input()

with open('screen_menu.py') as f:
    exec(f.read())
    


