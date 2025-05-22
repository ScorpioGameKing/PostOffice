import logging
from redmail import gmail
from postoffice.directory import OfficeDirectory
from os import system, name
from pytermgui import YamlLoader

logger = logging.getLogger(__name__)
logging.basicConfig(filename='./logs/debug.log', encoding='utf-8', format='%(levelname)s:%(message)s', filemode='w', level=logging.DEBUG)
logger.info("Logger Initialized")

def offices() -> OfficeDirectory:

    office_dir = OfficeDirectory()

    logger.info(f"Blank Directory [{office_dir}] and Home ref created")

    #with YamlLoader() as loader, open("./modtest/ui/testUI.yml", "r") as datafile:
    #    loader.load(datafile)

    # Adding a random comment
    office_dir.welcome_prompt()
    return office_dir

def main() -> None:
    office_space = offices()
    office_space.run()

if __name__ == "__main__":
    system('cls' if name == 'nt' else 'clear')
    main()
