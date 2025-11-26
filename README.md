<div align="center">

# Bible First

A simple, terminal-based Bible reader application written in Python.

replit: [https://replit.com/@IM0itself/bible-app](https://replit.com/@IM0itself/bible-app)

</div>

<details>
<summary>

# For Presentation.pdf natin:

</summary>

## Features

- dynamic and interactive - navigate with arrow keys instead of typing 
- responsive - the program adapts to the terminal window size. has scrollable lists.
- hand picked verses - not some random verses but ones that are most appropriate
- tried and tested algorithm - compared other algorithms and found a best one to be used in finding words in the Bible
- minimalist design - simple and easy to use
- auto install - the program will install all the required python module automatically i.e readchar

## Screens
[may image kada screen] <br>
[2 images for Read Bible screen]

- Intro: the first screen you see when you open the program. it will install required python module automatically i.e readchar. before proceeding to the menu.
- Menu: allows you to navigate to different screens. display verse-of-the-day immediately after opening the menu.
- Read Bible: easily navigate through the Old and New Testaments, select books, chapters, and verses. allows you to bookmark verses for quick access later.
- Bookmarks: see your bookmarked verses and display recommended verses. 
- Find in Bible: Search for specific words or phrases across the entire Bible using linear search algorithm.

## Replit Link

[https://replit.com/@IM0itself/bible-app](https://replit.com/@IM0itself/bible-app)

</details>

<details>
<summary>

# For Documentation.pdf natin:

</summary>

## Usage

Ensure you have Python installed on your system.

1.  **Start the Application**:
    for Windows users, double-click the `RUN.bat` file.

    Or else run the intro screen to start the app:
    ```bash
    python screen1_intro.py
    ```

2.  **Main Menu Navigation**:
    - Use **UP** and **DOWN** arrow keys to highlight options.
    - Press **ENTER** to select an option.
    - **Shortcuts**:
        - `W`: Start Reading
        - `B`: Bookmarks
        - `F`: Find in Bible
        - `Q`: Quit

3.  **Reading the Bible**:
    - **Select Book**: Use arrow keys to navigate the 3 columns of books.
    - **Select Chapter and Verse**: Use arrow keys to navigate the number grid of chapters and verses. 
    - **Read Verse**: Use **LEFT** and **RIGHT** arrow keys to navigate.

4.  **General Controls**:
    - Use **UP** and **DOWN** arrow keys to navigate.
    - Press **ENTER** to select an option.
    - `Q`: Go back to the previous menu or quit the application.

## File Structure

### Main Python Files
- `screen1_intro.py`: Entry point of the application.
- `screen2_menu.py`: navigate through screens here. display verse-of-the-day immediately after opening the menu. uses recommended_verses.py.
- `screen3_read_bible_books.py`: navigate through 66 books separated by 3 columns.
- `screen3_read_bible_chapters_and_verses.py`: navigate through chapters and verses of a selected book as a number grid.
- `screen3_read_bible_verse.py`: display the verse selected from previous screens on screen 3 or from screen 4 (bookmarks) or in screen 5 (find in bible)
- `screen4_bookmarks.py`: display bookmarked verses and recommended verses. uses bookmarks.json and recommended_verses.py.
- `screen5_find_in_bible.py`: Search functionality.
- `UI.py`: contains functions for the UI design i.e print string in a box (print_box) and print title logo (print_title)

### Data Files
- `bible_data.py`: contains the Bible text data i.e KJV Bible.
- `recommended_verses.py`: contains verses that are hand picked. used in verse-of-the-day and bookmarks screen as recommended verses.
- `bookmarks.json`: contains the bookmarked verses. add data through the screen3_read_bible_verse.py. remove data through the screen4_bookmarks.py.

### Other Files
- `RUN.bat`: batch file for Windows users to easily run the program.
- `a.txt`: contains the design prototypes of the program.

## Reflection
- We decided that we start at an intro screen before the menu. This is because if the program crashes, we got to see at least one working screen:D.
- When we are designing the UI for the main menu, instead of having the verse of the day as an option, we have decided to just display it immediately.
- Instead of the user typing 1, 2, 3.. in navigating, we have decided to just use arrow keys. It turns out to be more interactive and user-friendly.
- Speaking of which, we use ANSII escape codes to highlight the selected option. The highlight color was first a yellow text. But it blends with the white texts that is why we changed it to a yellow background and black text.
- There are 3 columns of books in the Read Bible screen. Each column has maximum row of 27. This is done to visibly fit all the books of the New Testament which has 27 books. The Old Testament has 39, so we just split the Old Testament into 2 columns. 
- Instead of getting a random verse on the Bible, we hand picked it. Randomly getting a verse is not a good idea because it may not be the most appropriate verse to be displayed. for example, what if we got Joshua 19:20 by chance, it has "And Rabbith, and Kishion, and Abez,". It does not make any sense as a standalone verse.
- Also we have measured the time it takes for 3 algorithms for searching for a word in the Bible. Linear Search, Binary Search, and Indexed Search. It actually turns out that indexed search technically the fastest but it comes at a cost of building an index for the Bible which takes additional time. Linear search is the best because it is super simple and has no extra steps.

## Lessons Learned
- Design the UI first before implementing it. Although it sounds good to see the UI already in action, it actually turns out that it is faster to design it first as a raw text before implementing it. Because it allows us to simplify it quicker and visualize the flow better. We actually have a file `a.txt` that contains the design prototypes of the program.
- Do not rely heavily on AI. It is actually more rewarding when we got to understand the logic behind the code. Although AI can help us with the implementation, using it as a hand instead of a hammer is not a good idea. 

</details>

<details>
<summary>

# For Contributions.pdf:

</summary>

- Santos, Jay R - screen 3 (read bible)
- Buen, Louise - screen 4 (bookmarks)
- Calimlim, Jarelle - screen 5 (find in bible)
- Bautista, Russell Jonn - screen 1 & 2, refactoring
- Bautista, Anthony Daniel - documentation, resources for verses
</details>
