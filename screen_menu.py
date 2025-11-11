try:
    from readchar import readkey, key
except ImportError:
    import os
    print("\nwait lang pu...")
    os.system("pip install readchar")
    from readchar import readkey, key

options = [
    "📖 START READING",   # 0
    "🔖 BOOKMARKS",       # 1
    "🔎 SEARCH IN BIBLE", # 2
    "🔙 BACK",            # 3
    "❌ QUIT"             # 4
]

def open_file(index):
    python_file = ""
    if index == 0:
        python_file = "screen_read_bible.py"
    elif index == 1:
        python_file = "screen_bookmarks.py"
    elif index == 2:
        python_file = "screen_find_in_bible.py"
    elif index == 3:
        python_file = "screen_intro.py"
    elif index == 4:
        exit()
    
    try:
        with open(python_file, encoding='utf-8') as f:
            exec(f.read())
    
    except FileNotFoundError:
        input("\ncoming soon..\nwala pang file na " + python_file)
        with open("screen_menu.py", encoding='utf-8') as f:
            exec(f.read())


# =====
# START
# =====

selected_option = 0
while True:
    print("\033[H\033[2J")  # Clear screen
    print("\nBASTA TITLE NATIN\n")
    print("[ verse of the day dito ]\n")
    
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