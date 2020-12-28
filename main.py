import os
import re

## -- Rich Config
from rich import print
from rich.console import Console
console = Console()

from time import sleep
from selenium import webdriver

## -- Helpers
from helpers.clear import clearTerminal
from helpers.ascii import print_ascii
from helpers.urls_warning import warning_message


def main():
    clearTerminal()
    print_ascii()
    sleep(0.5)
    create_screenshot_folder()


def create_screenshot_folder():
    folder_name = console.input("\n[bold yellow]:: Type the screenshots folder name ~> [/]")
    current_path = os.getcwd()

    if(os.path.isdir(folder_name)):
        console.print("[bold red]:: The folder {} already exists. [/]".format(folder_name))
    else:
        console.print("[green]:: Folder [bold]{}[/] created successfully! [/]".format(folder_name))
        os.mkdir(current_path + '/{}'.format(folder_name))

        warning_message()

        search_for_subs_file(folder_name)
        


def search_for_subs_file(folder_name):
    if os.path.isfile("subs.txt"):
        print("\n[bold green]:: subs.txt file found. [/]\n")
        remove_empty_lines(folder_name)
    else:
        print("\n[bold red][X] subs.txt file not found, please verify if the file exists or is in the same directory.[/]")


def remove_empty_lines(folder_name):
    with open("subs.txt", "r+") as not_formated_file:
        lines = not_formated_file.readlines()
        not_formated_file.seek(0)
        not_formated_file.writelines(line for line in lines if line.strip())
        not_formated_file.truncate()

    format_urls(folder_name)



def format_urls(folder_name):
    with open("subs.txt", "r+", encoding="utf8") as domains_file:
        file_content = domains_file.readlines()

    for domain_url in file_content:
        final_url = domain_url.replace("\n", "")

        try:
            if not final_url.startswith("https://"):
                formated_url = f"https://{final_url}"
                sleep(0.5)
                domain_screenshot(formated_url, folder_name)
        except Exception as error:
            print(f"\n[bold red][X] - We are having problems in {formated_url} [/]\n")
            print(error)
            continue


def domain_screenshot(formated_url, folder_name):
    current_path = os.getcwd()
    chromedriver_path = os.getcwd() + '/driver/chromedriver.exe'

    chrome_profile = webdriver.ChromeOptions()

    chrome_profile.add_argument('--ignore-certificate-errors')
    chrome_profile.add_argument("--log-level=3")
    chrome_profile.add_argument("--incognito")
    chrome_profile.add_argument("--disable-popup-blocking")
    chrome_profile.add_argument("--disable-gpu")

    chrome_manager = webdriver.Chrome(chromedriver_path, options=chrome_profile)
    chrome_manager.get(formated_url)

    os.chdir(folder_name)
    screenshot = re.sub("[:/]", "", formated_url)
    chrome_manager.save_screenshot(screenshot + ".png")

    sleep(0.1)

    chrome_manager.close()
    chrome_manager.quit()

    # Fix screenshot file name
    fix_file_name = "https"
    for screenshots in os.listdir():
        if fix_file_name in screenshots:
            screenshot_path = os.path.join(screenshots)
            new_file = os.path.join(screenshots.replace(fix_file_name, ""))
            os.rename(screenshot_path, new_file)

    os.chdir(current_path) # Back to main path


if __name__ == '__main__':
    main()