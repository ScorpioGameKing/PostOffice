import logging
from redmail import gmail
from postoffice.office import Office
from postoffice.commands import Commands, Help
from os import system, name
from pytermgui import (
    Window,
    InputField,
    WindowManager,
    YamlLoader,
    Container,
    Label
)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', encoding='utf-8', format='%(levelname)s:%(message)s', filemode='w', level=logging.DEBUG)
logger.info("Logger Initialized")

def offices() -> WindowManager:

    home_office = Office()
    office_directory = {}
    logger.info(f"Blank Directory [{office_directory}] and Home ref created")

    with YamlLoader() as loader, open("./modtest/ui/testUI.yml", "r") as datafile:
        loader.load(datafile)

    def swap(manager:WindowManager, new_window:Window, old_window:Window|None=None) -> None:
        logger.debug("Swapping window to %s", new_window.title.split("]")[1])
        if old_window:
            manager.remove(old_window)
        manager.add(new_window)
    
    def cont(manager:WindowManager, window:Window) -> None:
        logger.debug("Continued")
        prompt = user_prompt(manager)
        swap(manager, prompt, window)

    def exit_office(manager:WindowManager, window:Window) -> None:
        logger.debug("Exiting Via Command")
        manager.remove(window)
        manager.stop()
        exit()

    def create_new_office(manager:WindowManager, window:Window, service:str, service_name:str) -> None:
        logger.debug(f"Trying to create Office for [{service}] with name [{service_name}]")
        try:
            temp_ofc = Office()
            temp_ofc.set_service(gmail)
            office_directory.update({service_name : temp_ofc})
            success = success_prompt(manager)
            swap(manager, success, window)
        except:
            failure = failure_prompt(manager)
            swap(manager, failure, window)

    def open_office(manager:WindowManager, window:Window, ofc:str) -> None:
        logger.debug(f"Trying to Open Office for with name [{ofc}]")
        try:
            home_office = office_directory[ofc]
            success = success_prompt(manager)
            swap(manager, success, window)
            logger.info(f"Opened [{home_office._office_service}]")
        except:
            failure = failure_prompt(manager)
            swap(manager, failure, window)

    def hire_mailman(manager:WindowManager, window:Window, username:str, password:str) -> None:
        logger.debug(f"Trying to create Mailman for [{username}]")
        logger.debug(f"Current Home Office: [{home_office._office_service}]")
        try:
            home_office.hireMailman(username, password)
            success = success_prompt(manager)
            swap(manager, success, window)
        except:
            failure = failure_prompt(manager)
            swap(manager, failure, window)

    def set_active_mailman(manager:WindowManager, window:Window, username:str) -> None:
        logger.debug(f"Trying to set [{username}] as Active")
        logger.debug(f"Current Home Office: [{home_office._office_service}]")
        try:
            home_office.setActiveMailman(username)
            success = success_prompt(manager)
            swap(manager, success, window)
        except:
            failure = failure_prompt(manager)
            swap(manager, failure, window)

    def send_mail(manager:WindowManager, window:Window, reciver:str, topic:str, body:str) -> None:
        logger.debug(f"Trying send Email to [{reciver}] with subject [{topic}] and body [{body}]")
        logger.debug(f"Current Home Office: [{home_office._office_service}]")
        try:
            home_office.sendMail(_topic, _reciver, _body)
            success = success_prompt(manager)
            swap(manager, success, window)
        except:
            failure = failure_prompt(manager)
            swap(manager, failure, window)

    def run_command(manager:WindowManager, window:Window, cmd:str) -> None:
        logger.debug(f"Command: [{cmd}]")
        match cmd:
            case Commands.EXIT:
                exit_office(manager, window)

            case Commands.HELP:
                new_window = help_prompt(manager)
                swap(manager, new_window, window)

            case Commands.CREATE_OFFICE:
                new_window = create_office_prompt(manager)
                swap(manager, new_window, window)
            
            case Commands.OPEN_OFFICE:
                new_window = open_office_prompt(manager)
                swap(manager, new_window, window)

            case Commands.CLOSE_OFFICE:
                new_window = close_office_prompt(manager)
                swap(manager, new_window, window)

            case Commands.HIRE_MAILMAN:
                new_window = hire_mailman_prompt(manager)
                swap(manager, new_window, window)

            case Commands.FIRE_MAILMAN:
                new_window = fire_mailman_prompt(manager)
                swap(manager, new_window, window)

            case Commands.SET_ACTIVE_MAILMAN:
                new_window = set_active_mailman_prompt(manager)
                swap(manager, new_window, window)

            case Commands.SEND_MAIL:
                new_window = send_mail_prompt(manager)
                swap(manager, new_window, window)

            case _:
                new_window = unrecognized_prompt(manager)
                swap(manager, new_window, window)

    def welcome_prompt(manager:WindowManager) -> Window:
        window = (
            Window(
                "",
                "Welcome To PostOffice Version 0.0.1",
                "",
                ["Continue", lambda *_: cont(manager, window)],
                "",
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Welcome Menu")
        )
        return window
    
    def user_prompt(manager:WindowManager) -> Window:
        cmd = InputField("help", prompt="Command: ")
        window = (
            Window(
                "",
                cmd,
                "",
                ["Run Command", lambda *_: run_command(manager, window, cmd.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Command Prompt")
        )
        return window

    def success_prompt(manager:WindowManager) -> Window:
        window = (
            Window(
                "Success!",
                "",
                ["Return", lambda *_: cont(manager, window)],
                "",
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]Success")
        )
        return window
    
    def failure_prompt(manager:WindowManager) -> Window:
        logger.warning("FAILURE IS AN OPTION")
        window = (
            Window(
                "Failure",
                "",
                ["Return", lambda *_: cont(manager, window)],
                "",
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]Failure")
        )
        return window
    
    def help_prompt(manager:WindowManager) -> Window:
        cmds = ""
        for cmd in Help:
            cmds += f"{cmd}\n"
        window = (
            Window(
                "",
                Label(cmds, parent_align=0),
                "",
                ["Continue", lambda *_: cont(manager, window)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Command Help")
        )
        return window
    
    def create_office_prompt(manager:WindowManager) -> Window:
        service = InputField("gmail", prompt="Enter Email Service: ")
        service_name = InputField("", prompt="Enter Service Name: ")
        window = (
            Window(
                "",
                service,
                "",
                service_name,
                "",
                ["Create", lambda *_: create_new_office(manager, window, service.value, service_name.value)],
                "",
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Create Office")
        )
        return window

    def open_office_prompt(manager:WindowManager) -> Window:
        ofc = InputField("", prompt="Choose an Office to use: ")
        window = (
            Window(
                "",
                ofc,
                "",
                ["Open", lambda *_: open_office(manager, window, ofc.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Open Office")
        )
        return window

    def close_office_prompt(manager:WindowManager) -> Window:
        window = (
            Window(
                "",
                "WIP",
                "",
                ["Continue", lambda *_: cont(manager, window)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Close Office")
        )
        return window

    def hire_mailman_prompt(manager:WindowManager) -> Window:
        username = InputField("", prompt="Enter Email: ")
        password = InputField("", prompt="Enter GPass: ")
        password.styles["value"] = "invisible"
        window = (
            Window(
                "",
                username,
                "",
                password,
                "",
                ["Create", lambda *_: hire_mailman(manager, window, username.value, password.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Hire Mailman")
        )
        return window

    def fire_mailman_prompt(manager:WindowManager) -> Window:
        window = (
            Window(
                "",
                "WIP",
                "",
                ["Continue", lambda *_: cont(manager, window)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Fire Mailman")
        )
        return window

    def set_active_mailman_prompt(manager:WindowManager) -> Window:
        username = InputField("", prompt="Choose the Mailman to use: ")
        window = (
            Window(
                "",
                username,
                "",
                ["Continue", lambda *_: set_active_mailman(manager, window, username.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Choose Mailman")
        )
        return window

    def send_mail_prompt(manager:WindowManager) -> Window:
        reciver = InputField("", prompt="Enter a reciving Email: ")
        topic = InputField("", prompt="Enter a subject: ")
        body = InputField("")
        body.multiline = True
        window = (
            Window(
                "",
                reciver,
                "",
                topic,
                "",
                Container(
                    "Email Body:",
                    body,
                    box="EMPTY_VERTICAL",
                ),
                "",
                ["Continue", lambda *_: send_mail(manager, window, reciver.value, topic.value, body.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Send Mail")
        )
        return window
    
    def unrecognized_prompt(manager:WindowManager) -> Window:
        window = (
            Window(
                "",
                "Command not recognized",
                "",
                ["Continue", lambda *_: cont(manager, window)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Unrecongized Command")
        )
        return window
    
    manager = WindowManager()
    welcome = welcome_prompt(manager)
    swap(manager, welcome)
    return manager

def main() -> None:
    office_space = offices()
    office_space.run()

if __name__ == "__main__":
    system('cls' if name == 'nt' else 'clear')
    main()
