#!/bin/python3

import os, re, subprocess

def check(name):
    """Check name for invalid characters and replace them, or raise an error if sanitized is empty."""
    sanitized = re.sub(r'[<>:"/\\|?*\x00]', '', name); # invalid chars
    sanitized = sanitized.strip(); # remove leading space
    sanitized = sanitized[:255]  # max length for a name fix
    if (not sanitized):
        raise ValueError("Please enter a valid game name, as it is empty or contains invalid characters.");
    return sanitized;

def createDir(dirName):
    """Attempt to make a directory dirName"""
    try:
        os.makedirs(dirName, exist_ok=True);
        print(f"Directory: {dirName} created.");
    except Exception as e:
        print(f"Error creating directory: {e}");


def generateYAMLTemplate(gameName, hasInstaller, fixedName):
    """Generates the YAML to install the game"""
    if hasInstaller:
        return f""" name: "{gameName}"
            game_slug: {fixedName.lower()}
            version: GameInstaller 0.0
            slug: {fixedName.lower()}_installer
            runner: wine
            description: "Generated By gameInstaller 0.0"

            script:
              files:
                - installer: "N/A: Select the game's setup file."
              game:
                exe: $GAMEDIR/replace.exe
                prefix: $GAMEDIR/../prefix/
              installer:
                - task:
                    name: wineexec
                    executable: installer
        """;
    else:
        return f"""
            name: "{gameName}"
            game_slug: {fixedName.lower()}
            version: GameInstaller 0.0
            slug: {fixedName.lower()}_installer
            runner: wine
            description: "Generated By gameInstaller 0.0"

            script:
              game:
                exe: $GAMEDIR/replace.exe
                prefix: $GAMEDIR/../prefix/
              installer:
                - task:
                    name: create_prefix
                    arch: win64
        """;


def runLutris(installScriptPath):
    """Run the lutris with the install script generated"""
    try:
        print("Starting lutris..");
        print("Press CTRL + C to exit when the installation is complete.");
        res = subprocess.call(
            ["lutris", "-i", installScriptPath], # For some reason, lutris just hangs.
        );
    except KeyboardInterrupt as e:
        print(""); # We do nothing as this is expected.
    except Exception as e:
        print(f"Error installing game: {e}");
    finally:
        print("Done!");
        print("Cleaning up install script..");
        try:
            os.remove(installScriptPath);
            print("Removed, game should be installed! Have fun!");
        except Exception as e:
            print(f"Error removing install script: {e}");

def main():
    gamesPath = input("Enter games path (empty is ~/Documents/GAMES/): ");
    if (not gamesPath):
        gamesPath = "~/Documents/GAMES/";

    gameName = input("Game name you are installing: ");
    hasInstaller = input("Does the game include an installer (Y/n): ").lower() == 'y';
    checkedName = check(gameName);
    fixedName = "_".join(checkedName.split());

    base = os.path.expanduser(os.path.join(gamesPath + checkedName));
    game = os.path.join(base, "game");
    prefix = os.path.join(base, "prefix");

    createDir(base);
    createDir(game);
    createDir(prefix);

    yamlTemplate = generateYAMLTemplate(gameName, hasInstaller, fixedName);
    installScriptPath = os.path.join(base, "install.yaml");

    with open(installScriptPath, 'w') as f:
        f.write(yamlTemplate);

    runLutris(installScriptPath);

if __name__ == "__main__":
    main();
