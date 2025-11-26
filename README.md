<div align="center">

# Bible App

A simple, terminal-based Bible reader application written in Python.

replit: [https://replit.com/@IM0itself/bible-app](https://replit.com/@IM0itself/bible-app)

</div>

## Features

- **Read Bible**: Navigate through the Old and New Testaments, select books, chapters, and verses.
- **Bookmarks**: Save your favorite verses for quick access later.
- **Find in Bible**: Search for specific words or phrases across the entire Bible.
- **Verse of the Day**: Get inspired with a random verse displayed on the main menu every time you open the app.
- **Responsive Interface**: The application adapts its layout based on your terminal window size.

## Usage

1.  **Start the Application**:
    For Windows users, double-click the `RUN.bat` file.

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
    - **Select Book**: Use arrow keys to navigate the list of books. Press **ENTER** to select.
    - **Select Chapter**: Use arrow keys to select a chapter.
    - **Select Verse**: View verses and navigate between them.

4.  **General Controls**:
    - `Q`: Go back to the previous menu or quit the application.

## File Structure

- `screen1_intro.py`: Entry point of the application.
- `screen2_menu.py`: Main menu logic.
- `screen3_read_bible_*.py`: Screens for reading books, chapters, and verses.
- `screen4_bookmarks.py`: Bookmarks management.
- `screen5_find_in_bible.py`: Search functionality.
- `bible_data.py`: Contains the Bible text data.
