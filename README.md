# Game Installer Script

This Python script simplifies creating a game installation setup for Lutris. It generates a YAML configuration file and runs Lutris to complete the setup.

## Features
- Automatically sanitizes game names to prevent invalid characters.
- Creates necessary directories for the game and prefix.
- Generates a YAML installation script for games with or without an installer.
- Automates launching Lutris with the generated installation script.

## Requirements
- Python 3.x
- Lutris installed on your system


## Usage
1. Clone or get the latest release.
2. Run the file you downloaded or if you are running from source, run it using Python:
   ```bash
   python3 game_installer.py
   ```
    1) Follow the prompts:
        - Enter the path where you want to store games (default: ~/Documents/GAMES/).
        - Provide the name of the game.
        - Indicate if the game has an installer (Y for yes, n for no).
    2) The script will:
        - Create necessary directories.
        - Generate a YAML file for Lutris.
        - Launch Lutris with the generated YAML script.
    3) After installation, the script cleans up the YAML file.

# Updates #
This project will get updates from time to time, making the installs scripts easier to use.
