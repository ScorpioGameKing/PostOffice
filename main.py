from redmail import gmail
from postoffice.office import Office
from postoffice.commands import Commands, Help
from os import system, name
from pytermgui import (
    Window,
    InputField,
    WindowManager,
    YamlLoader,
    Container
)

def offices() -> WindowManager:

    def swap(manager:WindowManager, new_window:Window, old_window:Window|None=None):
        if old_window:
            manager.remove(old_window)
        manager.add(new_window)
    
    def cont(manager:WindowManager, window:Window):
        prompt = user_prompt(manager)
        swap(manager, prompt, window)

    def run_command(manager:WindowManager, window:Window, cmd:str):
        match cmd:
            case Commands.EXIT:
                exit_office(manager, window)

            case Commands.HELP:
                new_window = show_help(manager)
                swap(manager, new_window, window)

            case Commands.CREATE_OFFICE:
                pass

            case Commands.CLOSE_OFFICE:
                pass

            case Commands.HIRE_MAILMAN:
                pass

            case Commands.FIRE_MAILMAN:
               pass

            case Commands.SET_ACTIVE_MAILMAN:
                pass

            case Commands.SEND_MAIL:
                pass

            case _:
                new_window = unrecognized(manager)
                swap(manager, new_window, window)

    def welcome_menu(manager:WindowManager) -> Window:
        window = (
            Window(
                "",
                "Welcome To PostOffice Version 0.0.1",
                "",
                ["Continue", lambda *_: cont(manager, window)],
                "",
                width=60,
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
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]Command Prompt")
        )
        return window
    
    def exit_office(manager:WindowManager, window:Window) -> None:
        manager.remove(window)
        manager.stop()
        exit()
    
    def show_help(manager:WindowManager) -> Window:
        window = (
            Window(
                "",
                "WIP",
                "",
                ["Continue", lambda *_: cont(manager, window)],
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]Command Help")
        )
        return window
    
    def unrecognized(manager:WindowManager) -> Window:
        window = (
            Window(
                "",
                "Command not recognized",
                "",
                ["Continue", lambda *_: cont(manager, window)],
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]Unrecongized Command")
        )
        return window
    
    manager = WindowManager()
    welcome = welcome_menu(manager)
    swap(manager, welcome)
    return manager

def main():
    home_office:Office
    office_space = offices()
    office_space.run()

    '''
    TODO
            case Commands.CREATE_OFFICE:
                _ofc_name = input("Please enter a name for the Office: ")
                _temp_ofc = Office(gmail)
                office_space.update({_ofc_name : _temp_ofc})

            case Commands.OPEN_OFFICE:
                _ofc = input("Choice: ")
                print(_ofc)
                home_office = office_space[_ofc]

            case Commands.CLOSE_OFFICE:
                print("Not Supported Yet")

            case Commands.HIRE_MAILMAN:
                print("Hire a Mailman")
                _usr = input("Enter an email: ")
                _pas = input("Enter GApp Password: ")
                home_office.hireMailman(_usr, _pas)
            
            case Commands.FIRE_MAILMAN:
                print("Not Supported Yet")

            case Commands.SET_ACTIVE_MAILMAN:
                _active = input("Choose the Mailman to use: ")
                home_office.setActiveMailman(_active)

            case Commands.SEND_MAIL:
                _reciver = input("Enter a reciving Email: ")
                _topic = input("Enter a subject: ")
                _body = input("Type your msg: ")
                home_office.sendMail(_topic, _reciver, _body)
    '''

if __name__ == "__main__":
    system('cls' if name == 'nt' else 'clear')
    main()
