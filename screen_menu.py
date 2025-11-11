try:
    from readchar import readkey, key
except ImportError:
    import os
    print("Installing readchar...")
    os.system("pip install readchar")
    from readchar import readkey, key

options = [
    "start reading",   # 0
    "find in bible",   # 1
    "verse of the day",# 2
    "back to menu",    # 3
    "exit"             # 4
]

def open_file(index):
    python_file = ""
    if index == 0:
        python_file = "screen_read_bible.py"
    elif index == 1:
        python_file = "screen_find_bible.py"
    elif index == 2:
        python_file = "screen_verse_of_the_day.py"
    elif index == 3:
        python_file = "screen_intro.py"
    elif index == 4:
        exit()
    
    try:
        with open(python_file) as f:
            exec(f.read())
    except FileNotFoundError:
        input("\ncoming soon..\nwala pang file na " + python_file)
        # RESTART
        with open("screen_menu.py") as f:
            exec(f.read())


# =====
# START
# =====

selected_option = 0
while True:
    print("\033[2J\033[H")  # Clear screen
    print("\nBASTA TITLE NATIN\n")
    
    i = 0
    for option in options:
        if selected_option == i:
            print(f"o {option}")
        else:
            print(f"  {option}")

        i += 1
    
    pressed_key = readkey()
    press_down = pressed_key == key.DOWN or pressed_key == 's'
    press_up = pressed_key == key.UP or pressed_key == 'w'
    press_enter = pressed_key == key.ENTER
    
    if press_down:
        selected_option = (selected_option + 1) % len(options)
    elif press_up:
        selected_option = (selected_option - 1) % len(options)
    elif press_enter:
        open_file(selected_option)