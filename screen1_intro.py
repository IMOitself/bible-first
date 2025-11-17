print("\033[H\033[2J")  # Clear screen
print("\nBASTA WELCOME\n")
print("hello world")
print("Press any key to continue...")
input()

with open('screen2_menu.py', encoding='utf-8') as f: exec(f.read())