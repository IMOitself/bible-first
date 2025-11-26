def show_bookmarks():
    bms = load_bookmarks()
    print("\nBOOKMARKS\n")
    if not bms:
        print("No bookmarks yet. Add one from the Read Bible screen (press 'b').\n")
        return

    for i, bm in enumerate(bms):
        print(f"[{i}] {bm['book']} {bm['chapter']}:{bm['verse']} - {bm['text'][:80]}")


def start():
    while True:
        print("\033[H\033[2J")  # Clear screen
        show_bookmarks()
        print("\nCommands: v<number> view, d<number> delete, c clear all, ENTER back to menu")

        cmd = input("Action: ").strip()
        if cmd == "":
            break
        if cmd == "c":
            confirm = input("Clear all bookmarks? type YES to confirm: ")
            if confirm == "YES":
                clear_bookmarks()
                print("Bookmarks cleared.")
                input("Enter to continue...")
            continue
        if cmd.startswith("d"):
            try:
                idx = int(cmd[1:])
                ok = remove_bookmark(idx)
                if ok:
                    print("Removed.")
                else:
                    print("No bookmark at that index.")
            except ValueError:
                print("Invalid index")
            input("Enter to continue...")
            continue
        if cmd.startswith("v"):
            try:
                idx = int(cmd[1:])
                bms = load_bookmarks()
                bm = bms[idx]
                print("\n" + bm['book'] + " " + bm['chapter'] + ":" + bm['verse'] + "\n")
                print(bm['text'] + "\n")
            except Exception:
                print("Invalid index or empty bookmarks.")
            input("Enter to continue...")
            continue
        else:
            print("Unrecognized command")
            input("Enter to continue...")