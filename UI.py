def print_box(text):
    text_lines = text.split("\n")

    max_line_length = 0
    for line in text_lines:
        max_line_length = max(max_line_length, len(line))

    horizontal_line = "═" * (max_line_length + 2)

    print("╔" + horizontal_line + "╗")
    for line in text_lines:
        remaining_space = max_line_length - len(line)
        print("║" + " " + line + (" " * remaining_space) + " " + "║")
    print("╚" + horizontal_line + "╝")

def print_title():
    print("▀██▀▀█▄    ██  ▀██      ▀██             ▀██▀▀▀▀█  ██                   ▄   ")
    print(" ██   ██  ▄▄▄   ██ ▄▄▄   ██    ▄▄▄▄      ██  ▄   ▄▄▄  ▄▄▄ ▄▄   ▄▄▄▄  ▄██▄  ")
    print(" ██▀▀▀█▄   ██   ██▀  ██  ██  ▄█▄▄▄██     ██▀▀█    ██   ██▀ ▀▀ ██▄ ▀   ██   ")
    print(" ██    ██  ██   ██    █  ██  ██          ██       ██   ██     ▄ ▀█▄▄  ██   ")
    print("▄██▄▄▄█▀  ▄██▄  ▀█▄▄▄▀  ▄██▄  ▀█▄▄▄▀    ▄██▄     ▄██▄ ▄██▄    █▀▄▄█▀  ▀█▄▀ ")