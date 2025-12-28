import random
import re
import os
import time
import json

# Global variables for game state
player_hp = 0
player_damage = 0
in_fight = False
enemy_hp = 0
enemy_damage = 0
enemy_name = ""

# Language settings
current_language = "en"  # Default: English
languages = {}
translations = {}
CONFIG_FILE = "engine_config.json"


def load_config():
    """Load configuration including saved language"""
    global current_language

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if "language" in config:
                    current_language = config["language"]
        except:
            pass


def save_config():
    """Save current configuration"""
    config = {
        "language": current_language,
        "last_used": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except:
        pass


def load_translations():
    """Load translations from JSON files in langs directory"""
    global translations, languages

    # Clear existing
    languages = {}
    translations = {}

    # Check if langs directory exists, create if not
    if not os.path.exists("langs"):
        os.makedirs("langs")
        # Create default English file
        create_default_english_file()

    # Look for all .json files in langs directory
    for file in os.listdir("langs"):
        if file.endswith('.json'):
            lang_code = file.replace('.json', '')

            try:
                with open(os.path.join("langs", file), 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Get language name from file or use code
                    lang_name = data.get("language_name", lang_code.upper())
                    languages[lang_code] = lang_name
                    translations[lang_code] = data

            except:
                pass

    # If no language files found, create default English
    if not languages:
        create_default_english_file()
        # Reload
        load_translations()


def create_default_english_file():
    """Create default English translation file in langs directory"""
    default_english = {
        "language_name": "English",

        # Main interface
        "emulator_title": "=== TXR GAME SYSTEM ===",
        "only_txr": "System works only with .txr files",
        "enter_help": "Enter 'help' for command list",
        "enter_list": "Enter 'list' to view available .txr files",
        "enter_command": "\n> ",
        "current_lang": "Current language: {}",

        # Commands help (page 1)
        "help_title": "help - open help page",
        "run_cmd": "run [filename.txr] - run game file, e.g.: run game1.txr",
        "say_cmd": "say(text, name, delay) - character speaks with delay (seconds)",
        "fight_cmd": "fight(hp, damage, name) - start fight with enemy",
        "player_cmd": "player(hp, damage) - set player parameters",
        "player_add_cmd": "player(add hp, add damage) - modify player parameters",
        "select_cmd": "select(option1, option2, ...) - choice from multiple options",
        "lang_cmd": "lang [code] - switch language",
        "available_languages": "Available languages: {}",

        # Fight system
        "fight_title": "=== FIGHT WITH {} ===",
        "enemy_stats": "Enemy: {} damage, {} HP",
        "player_stats": "Player: {} damage, {} HP",
        "player_turn": "--- Player's turn ---",
        "attack_option": "1. Attack",
        "block_option": "2. Block",
        "choose_action": "Choose action (1-2): ",
        "player_attacked": "You attacked {} and dealt {} damage!",
        "enemy_attacked": "{} attacked you and dealt {} damage!",
        "blocked_attack": "You attacked {}, but they blocked some damage!",
        "damage_dealt": "Dealt {} damage!",
        "enemy_blocked": "{} attacked, but you blocked some damage!",
        "damage_taken": "Took {} damage!",
        "both_blocked": "Both opponents prepared for defense!",
        "enemy_hp": "{}: {} HP",
        "player_hp": "Player: {} HP",
        "victory": "VICTORY! You defeated {}!",
        "defeat": "DEFEAT! {} defeated you!",

        # Selection system
        "choice_title": "--- CHOICE ---",
        "choose_option": "Choose option (1-{}): ",
        "chosen_option": "You chose: {}",
        "enter_number": "Please enter a number",
        "number_range": "Please enter a number from 1 to {}",
        "select_min_options": "Error: select must have at least 2 options",

        # Dialogue system
        "dialogue_format": "{} say: {}",

        # File operations
        "invalid_file_ext": "Error: file '{}' must have .txr extension",
        "example_usage": "Example: run game1.txr",
        "file_not_found": "Error: file '{}' not found in 'games' directory",
        "file_lookup": "Looked for file at: {}",
        "sys_prefix_removed": "sys:// prefix removed",
        "use_run_cmd": "Use 'run' command to run file",
        "available_files": "Available .txr files in 'games' directory:",
        "no_txr_files": "(no .txr files in 'games' directory)",
        "no_games_found": "No game files found. Place .txr files in 'games' directory.",

        # Error messages
        "unknown_cmd": "Unknown command: {}",
        "available_cmds": "Available commands: help, run, list, test, lang",
        "error": "Error: {}",

        # System messages
        "test_params": "Current parameters: HP={}, Damage={}",
        "emulator_shutdown": "Emulator shutting down...",
        "help_page": "Page number (1-2): ",

        # Language commands
        "lang_changed": "Language changed to: {}",
        "invalid_lang": "Invalid language code. Available languages: {}"
    }

    with open(os.path.join("langs", "en.json"), 'w', encoding='utf-8') as f:
        json.dump(default_english, f, ensure_ascii=False, indent=2)


def t(key, *args):
    """Get translation for current language with formatting"""
    if current_language in translations and key in translations[current_language]:
        text = translations[current_language][key]
        if args:
            try:
                return text.format(*args)
            except:
                return text
        return text
    return key  # Return key itself if translation not found


def help(page):
    if page == 1:
        print(t("help_title"))
        print(t("run_cmd"))
        print(t("say_cmd"))
        print(t("fight_cmd"))
        print(t("player_cmd"))
        print(t("player_add_cmd"))
        print(t("select_cmd"))
        print(t("lang_cmd"))
        available_langs = ', '.join([f'{code} ({name})' for code, name in languages.items()])
        print(t("available_languages", available_langs))
    elif page == 2:
        print("Command syntax in .txr files:")
        print("say(Hello world!, Character, 2) -> Character say: Hello world! (with 2 sec delay)")
        print("fight(50, 10, Goblin) -> Start fight with Goblin")
        print("player(100, 15) -> Set player health 100 and damage 15")
        print("select(Go left, Go right)")
        print("    1:")
        print("    say(You went left, System, 1)")
        print("    2:")
        print("    say(You went right, System, 1)")


def say(text, name, delay=0):
    """Display character dialogue with delay"""
    print(t("dialogue_format", name, text))
    if delay > 0:
        time.sleep(delay)


def fight(enemy_hp_value, enemy_damage_value, enemy_name_value):
    """Start fight with enemy"""
    global in_fight, enemy_hp, enemy_damage, enemy_name, player_hp, player_damage
    in_fight = True
    enemy_hp = int(enemy_hp_value)
    enemy_damage = int(enemy_damage_value)
    enemy_name = enemy_name_value

    print(t("fight_title", enemy_name.upper()))
    print(t("enemy_stats", enemy_damage, enemy_hp))
    print(t("player_stats", player_damage, player_hp))

    # Fight logic
    while in_fight and enemy_hp > 0 and player_hp > 0:
        print(t("player_turn"))
        print(t("attack_option"))
        print(t("block_option"))
        choice = input(t("choose_action"))

        player_action = "attack" if choice == "1" else "block"

        # Enemy's turn (random choice)
        enemy_action = random.choice(["attack", "block"])

        # Action processing
        if player_action == "attack":
            if enemy_action == "attack":
                # Both attack
                enemy_hp -= player_damage
                player_hp -= enemy_damage
                print(t("player_attacked", enemy_name, player_damage))
                print(t("enemy_attacked", enemy_name, enemy_damage))
            else:  # enemy_action == "block"
                # Player attacks, enemy blocks (half damage)
                damage_dealt = max(0, player_damage // 2)
                enemy_hp -= damage_dealt
                print(t("blocked_attack", enemy_name))
                print(t("damage_dealt", damage_dealt))
        else:  # player_action == "block"
            if enemy_action == "attack":
                # Enemy attacks, player blocks (half damage)
                damage_taken = max(0, enemy_damage // 2)
                player_hp -= damage_taken
                print(t("enemy_blocked", enemy_name))
                print(t("damage_taken", damage_taken))
            else:
                # Both block
                print(t("both_blocked"))

        # Display current status
        print(t("enemy_hp", enemy_name, enemy_hp))
        print(t("player_hp", player_hp))

        # Check fight end
        if enemy_hp <= 0:
            print(t("victory", enemy_name))
            in_fight = False
            return True
        elif player_hp <= 0:
            print(t("defeat", enemy_name))
            in_fight = False
            return False

    in_fight = False
    return player_hp > 0


def set_player(hp_value, damage_value):
    """Set player parameters"""
    global player_hp, player_damage

    # Check if we need to add values
    if isinstance(hp_value, str) and hp_value.startswith("add "):
        player_hp += int(hp_value[4:])
    else:
        player_hp = int(hp_value)

    if isinstance(damage_value, str) and damage_value.startswith("add "):
        player_damage += int(damage_value[4:])
    else:
        player_damage = int(damage_value)


def select(*options):
    """Provide choice from multiple options"""
    if len(options) < 2:
        print(t("select_min_options"))
        return None

    print(t("choice_title"))
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input(t("choose_option", len(options))))
            if 1 <= choice <= len(options):
                print(t("chosen_option", options[choice - 1]))
                return choice
            else:
                print(t("number_range", len(options)))
        except ValueError:
            print(t("enter_number"))


def change_language(lang_code):
    """Change system language and save to config"""
    global current_language
    if lang_code in languages:
        current_language = lang_code
        lang_name = languages[lang_code]
        print(t("lang_changed", lang_name))
        # Save configuration
        save_config()
        return True
    else:
        available = ', '.join([f'{code} ({name})' for code, name in languages.items()])
        print(t("invalid_lang", available))
        return False


def execute_command(line):
    """Execute single command from line"""
    global player_hp, player_damage

    line = line.strip()
    if not line:
        return None

    # Process say command (new format with delay)
    if line.startswith("say("):
        # Try to parse with three parameters
        match = re.match(r'say\((.*?),\s*(.*?),\s*(\d+(?:\.\d+)?)\)', line)
        if match:
            text = match.group(1)
            name = match.group(2)
            delay = float(match.group(3))
            say(text, name, delay)
        else:
            # Try old format (without delay)
            match = re.match(r'say\((.*?),\s*(.*?)\)', line)
            if match:
                text = match.group(1)
                name = match.group(2)
                say(text, name)

    # Process fight command
    elif line.startswith("fight("):
        match = re.match(r'fight\((.*?),\s*(.*?),\s*(.*?)\)', line)
        if match:
            hp = match.group(1)
            damage = match.group(2)
            name = match.group(3)
            return fight(hp, damage, name)  # Return fight result

    # Process player command
    elif line.startswith("player("):
        match = re.match(r'player\((.*?),\s*(.*?)\)', line)
        if match:
            hp = match.group(1)
            damage = match.group(2)
            set_player(hp, damage)


def validate_txr_filename(filename):
    """Check if file has .txr extension"""
    if not filename.lower().endswith('.txr'):
        return False
    return True


def run_file(filename):
    """Execute commands from .txr file in games directory"""
    # Check file extension
    if not validate_txr_filename(filename):
        print(t("invalid_file_ext", filename))
        print(t("example_usage"))
        return

    # Remove possible sys:// prefix
    if filename.startswith("sys://"):
        filename = filename[6:]
        print(t("sys_prefix_removed"))

    # Check if games directory exists, create if not
    if not os.path.exists("games"):
        os.makedirs("games")

    # Construct full path
    filepath = os.path.join("games", filename)

    if not os.path.exists(filepath):
        print(t("file_not_found", filename))
        print(t("file_lookup", filepath))
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into lines and remove comments
    lines = []
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            lines.append(line)

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if line is select command
        if line.startswith("select("):
            # Extract options
            match = re.match(r'select\((.*?)\)', line)
            if match:
                options_str = match.group(1)
                options = [opt.strip() for opt in re.split(r',(?![^()]*\))', options_str)]

                # Make choice
                choice = select(*options)
                if choice is None:
                    i += 1
                    continue

                # Find corresponding block
                i += 1
                found_block = False

                while i < len(lines):
                    # Check if line is block start (number:)
                    if re.match(r'^\s*(\d+):\s*$', lines[i]):
                        block_num = int(re.match(r'^\s*(\d+):\s*$', lines[i]).group(1))

                        if block_num == choice:
                            found_block = True
                            i += 1
                            # Execute commands in block until next block or file end
                            while i < len(lines) and not re.match(r'^\s*(\d+):\s*$', lines[i]):
                                result = execute_command(lines[i])
                                if result is False:  # Player lost
                                    return False
                                i += 1
                            # Exit block search loop
                            break
                        elif block_num > choice:
                            # Skip this block and continue searching
                            i += 1
                            while i < len(lines) and not re.match(r'^\s*(\d+):\s*$', lines[i]):
                                i += 1
                        else:
                            i += 1
                    else:
                        i += 1

                if not found_block:
                    # If block not found, continue with next line
                    continue
            else:
                i += 1
        else:
            # Execute regular command
            result = execute_command(line)
            if result is False:  # Player lost
                return False
            i += 1

    return True


def list_txr_files():
    """List all .txr files in games directory"""
    # Check if games directory exists, create if not
    if not os.path.exists("games"):
        os.makedirs("games")

    print(t("available_files"))
    files_found = False
    for file in os.listdir("games"):
        if file.lower().endswith('.txr'):
            print(f"  - {file}")
            files_found = True

    if not files_found:
        print(t("no_txr_files"))
        print(t("no_games_found"))


def main():
    global player_hp, player_damage

    # Load saved configuration first
    load_config()

    # Load translations from JSON files in langs directory
    load_translations()

    # Create games directory if it doesn't exist
    if not os.path.exists("games"):
        os.makedirs("games")

    # Display interface with translations
    print(t("emulator_title"))
    print(t("only_txr"))
    print(t("enter_help"))
    print(t("enter_list"))

    # Show current language
    lang_name = languages.get(current_language, "English")
    print(t("current_lang", lang_name))

    while True:
        try:
            cmd = input(t("enter_command")).strip()

            if cmd.lower() == "help":
                page = input(t("help_page"))
                try:
                    help(int(page))
                except ValueError:
                    print(t("enter_number"))

            elif cmd.lower().startswith("run "):
                filename = cmd[4:].strip()
                # Check extension
                if not validate_txr_filename(filename):
                    print(t("invalid_file_ext", filename))
                    print(t("example_usage"))
                    continue

                # Reset player parameters before running new file
                player_hp = 0
                player_damage = 0
                run_file(filename)

            elif cmd.lower().startswith("lang "):
                lang_code = cmd[5:].strip()
                change_language(lang_code)

            elif cmd.lower() == "list":
                list_txr_files()

            elif cmd.lower() == "test":
                # Test command to check state
                print(t("test_params", player_hp, player_damage))

            elif cmd.lower().endswith('.txr'):
                # If user entered just .txr filename
                print(t("use_run_cmd"))
                print(t("example_usage").replace("game1.txr", cmd))

            elif cmd:
                print(t("unknown_cmd", cmd))
                print(t("available_cmds"))

        except KeyboardInterrupt:
            print(t("emulator_shutdown"))
            break
        except EOFError:
            print(t("emulator_shutdown"))
            break
        except Exception as e:
            print(t("error", e))


if __name__ == "__main__":
    main()