import os
import requests
from lxml import html
import random
import string

class color:
    VIOLET, CYAN, DARK_CYAN, BLUE, GREEN, YELLOW, RED, WHITE, BLACK, GRAY, MAGENTA, BOLD, DIM, NORMAL, UNDERLINED, STOP = '\033[95m', '\033[96m', '\033[36m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[37m', '\033[30m','\033[38;2;88;88;88m', '\033[35m', '\033[1m', '\033[2m', '\033[22m', '\033[4m', '\033[0m'

def check_username_availability(username):
    try:
        page = requests.post('https://www.gamertagavailability.com/check.php', data={'Gamertag': username, 'Language': 'English'})
        tree = html.fromstring(page.content)
        response = tree.xpath('.//div[@id="yres"]')[0].text.strip()
        return response != "is not available!", response
    except IndexError:
        return False, "Error: Unexpected response format"
    except Exception as e:
        return None, f"Error occurred while checking availability for {username}: {e}"

def is_valid_username(username):
    if not username or len(username) > 12 or not username[0].isalpha() or not username[-1].isalnum() or '  ' in username:
        return False
    for char in username:
        if not (char.isalnum() or char == ' '):
            return False
    return True

def generate_username(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_username_with_numbers(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def clear_existing_usernames(length):
    folder_name = "Claimable"
    file_path = os.path.join(folder_name, f"{length}L.txt")
    if os.path.exists(file_path):
        with open(file_path, "w"):
            pass
        print(f"[ {color.GREEN}+{color.STOP} ] Existing {length}L usernames cleared.")
    else:
        print(f"[ {color.YELLOW}!{color.STOP} ] No existing {length}L usernames found.")

def save_valid_username_to_file(username, length):
    if username:
        folder_name = "Claimable"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_path = os.path.join(folder_name, f"{length}L.txt")
        
        # Add the new valid username to the file
        with open(file_path, "a") as file:
            if os.path.getsize(file_path) > 0:  # Check if file is not empty
                file.write('\n')  # Add newline only if the file is not empty
            file.write(username)

def main():
    # Create 'Claimable' folder if it doesn't exist
    folder_name = "Claimable"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"[ {color.GREEN}+{color.STOP} ] 'Claimable' folder created.")

    own_list = input('[ {0.MAGENTA}?{0.STOP} ] {0.GRAY}Do you have your own list of usernames you want to check? (yes/no):{0.STOP} '.format(color)).lower() == "yes"

    if own_list:
        length_to_check = int(input('[ {0.MAGENTA}?{0.STOP} ] {0.GRAY}Enter the length of usernames to check (between 3 and 12):{0.STOP} '.format(color)))
        file_path = os.path.join(folder_name, f"{length_to_check}L.txt")
        clear_existing_usernames(length_to_check)

        while True:
            file_path = input('[ {0.MAGENTA}?{0.STOP} ] {0.GRAY}Enter the file path containing the list of usernames (e.g., usernames.txt):{0.STOP} ')
            file_path = file_path.strip('"')  # Remove surrounding quotes if any
            if not os.path.isfile(file_path):
                print(f"[ {color.RED}Error{color.STOP} ] Invalid file path. Please enter a valid file path.")
            else:
                break

        with open(file_path, "r") as file:
            usernames = [username.strip() for username in file.readlines()]
    else:
        while True:
            try:
                min_length = 3
                max_length = 12
                length = int(input('[ {0.MAGENTA}?{0.STOP} ] {0.GRAY}Enter the length of usernames to generate (between 3 and 12):{0.STOP} '.format(color)))
                if length < min_length or length > max_length:
                    raise ValueError
                clear_existing = False
                file_path = os.path.join(folder_name, f"{length}L.txt")
                if os.path.exists(file_path):
                    clear_existing = input(f'[ {color.MAGENTA}?{color.STOP} ] {color.GRAY}Do you want to clear existing {length}L usernames before generating new ones? (yes/no):{color.STOP} ').lower() == "yes"
                    if clear_existing:
                        clear_existing_usernames(length)
                use_numbers = input('[ {0.MAGENTA}?{0.STOP} ] {0.GRAY}Do you want to include numbers in the usernames? (yes/no):{0.STOP} ').lower() == "yes"
                num_usernames = int(input('[ {0.MAGENTA}?{0.STOP} ] {0.GRAY}Enter the number of usernames to generate and check:{0.STOP} '.format(color)))
                if num_usernames <= 0:
                    raise ValueError
                break
            except ValueError:
                print(f"[ {color.RED}Error{color.STOP} ] Invalid input. Please enter a valid length between 3 and 12, a positive integer, and yes or no for including numbers.")

        usernames = []

        while len(usernames) < num_usernames:
            if use_numbers:
                new_username = generate_username_with_numbers(length)
            else:
                new_username = generate_username(length)
            if is_valid_username(new_username):
                usernames.append(new_username)

    for username in usernames:
        availability, response = check_username_availability(username)
        if availability:
            print(f"[ {color.GREEN}+{color.STOP} ] Gamertag '{username}' seems to be available!")
            save_valid_username_to_file(username, length)  # Save the username in real-time
        else:
            print(f"[ {color.RED}-{color.STOP} ] Gamertag '{username}' is not available!")

if __name__ == "__main__":
    main()
