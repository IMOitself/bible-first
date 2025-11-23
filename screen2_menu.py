try:
    from readchar import readkey, key
except ImportError:
    import os
    print("\nwait lang pu...")
    os.system("pip install readchar")
    from readchar import readkey, key

options = [
    "📖 START READING",  # 0
    "🔖 BOOKMARKS",      # 1
    "🔎 FIND IN BIBLE",  # 2
    "🔙 BACK TO TITLE",  # 3
    "❌ QUIT"            # 4
]

def open_screen(index):
    if index == 0:
        import screen3_read_bible_books
        screen3_read_bible_books.start()
    elif index == 1:
        import screen4_bookmarks
        screen4_bookmarks.start()
    elif index == 2:
        import screen5_find_in_bible
        screen5_find_in_bible.start()
    elif index == 3:
        import screen1_intro
        screen1_intro.start()
    elif index == 4:
        exit()


# =====
# START
# =====

def start():
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
        
        # navigation hehe

        pressed_key = readkey()

        if pressed_key == key.DOWN:
            selected_option = (selected_option + 1) % len(options)

        elif pressed_key == key.UP:
            selected_option = (selected_option - 1) % len(options)

        elif pressed_key == key.ENTER:
            open_screen(selected_option)