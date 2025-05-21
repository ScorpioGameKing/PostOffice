from pytermgui import WindowManager, Window, Container, InputField, Label
from postoffice.office import Office
from postoffice.commands import Commands, Help
from redmail import gmail
import logging

class OfficeDirectory(WindowManager):
    logger = logging.getLogger(__name__)

    home_office:Office
    ofc_dir:dict[str:Office]

    old_window:Window|None

    def __init__(self):
        super().__init__()
        self.home_office = Office()
        self.ofc_dir = {}
        self.old_window = None

    def set_home_office(self, office_name:str, office:Office):
        self.ofc_dir.update({office_name:office})
        self.home_office = self.ofc_dir[office_name]

    def create_new_office(self, service:str, office_name:str):
        try:
            new_office = Office()
            if service == "gmail":
                new_office.set_service(gmail)
            else:
                self.failure_prompt()
            self.set_home_office(office_name, new_office)
            self.success_prompt()
        except:
            self.failure_prompt()

    def hire_mailman(self, username:str, password:str):
        try:
            self.home_office.hireMailman(username, password)
            self.set_active_mailman(username, True)
            self.success_prompt()
        except:
            self.failure_prompt()
    
    def set_active_mailman(self, username:str, _auto:bool=False):
        try:
            self.home_office.setActiveMailman(username)
            if not _auto:
                self.success_prompt()
        except:
            if not _auto:
                self.failure_prompt()

    def send_mail(self, reciver:str, topic:str, body:str):
        self.logger.debug(f"Trying to send Email {topic} to {reciver} with body {body}")
        self.logger.debug(f"Home Office {self.home_office} Active Mailman {self.home_office._activeMailman}")
        self.logger.debug(f"Mailman User {self.home_office._activeMailman.username} Mail Password {self.home_office._activeMailman._password}")
        try:
            self.home_office.sendMail(topic, reciver, body)
            self.success_prompt()
        except:
            self.failure_prompt()

    def swap(self, new_window:Window|None=None) -> None:
        if self.old_window:
            self.logger.debug("Removing %s", self.old_window)
            self.remove(self.old_window)

        self.logger.debug("Set new target for removal %s", new_window)
        self.old_window = new_window

        if new_window:
            self.logger.debug("Swapping window to %s", new_window.title.split("]")[1])
            self.add(new_window)
        else:
            self.logger.debug("Swapping window to User Prompt")
            self.user_prompt()

    def exit_office(self) -> None:
        self.logger.debug("Exiting Via Command")
        self.remove(self.old_window)
        self.stop()
        exit()

    def run_command(self, cmd:str) -> None:
        self.logger.debug(f"Command: [{cmd}]")
        match cmd:
            case Commands.EXIT:
                self.exit_office()

            case Commands.HELP:
                self.help_prompt()

            case Commands.CREATE_OFFICE:
                self.create_office_prompt()
                
            case Commands.OPEN_OFFICE:
                self.open_office_prompt()
                
            case Commands.CLOSE_OFFICE:
                self.close_office_prompt()
                
            case Commands.HIRE_MAILMAN:
                self.hire_mailman_prompt()
                
            case Commands.FIRE_MAILMAN:
                self.fire_mailman_prompt()
                
            case Commands.SET_ACTIVE_MAILMAN:
                self.set_active_mailman_prompt()
                
            case Commands.SEND_MAIL:
                self.send_mail_prompt()

            case _:
                self.unrecognized_prompt()
                
    def welcome_prompt(self):
        window = (
            Window(
                "",
                "Welcome To PostOffice Version 0.0.1",
                "",
                ["Continue", lambda *_: self.swap()],
                "",
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Welcome Menu")
        )
        self.swap(window)

    def user_prompt(self):
        cmd = InputField("help", prompt="Command: ")
        window = (
            Window(
                "",
                cmd,
                "",
                ["Run Command", lambda *_: self.run_command(cmd.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Command Prompt")
        )
        self.swap(window)

    def success_prompt(self):
        window = (
            Window(
                "Success!",
                "",
                ["Return", lambda *_: self.swap()],
                "",
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]Success")
        )
        self.swap(window)
    
    def failure_prompt(self):
        self.logger.warning("FAILURE IS AN OPTION")
        window = (
            Window(
                "Failure",
                "",
                ["Return", lambda *_: self.swap()],
                "",
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]Failure")
        )
        self.swap(window)
    
    def help_prompt(self):
        cmds = ""
        for cmd in Help:
            cmds += f"{cmd}\n"
        window = (
            Window(
                "",
                Label(cmds, parent_align=0),
                "",
                ["Continue", lambda *_: self.swap()],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Command Help")
        )
        self.swap(window)

    def create_office_prompt(self):
        service = InputField("gmail", prompt="Enter Email Service: ")
        service_name = InputField("", prompt="Enter Service Name: ")
        window = (
            Window(
                "",
                service,
                "",
                service_name,
                "",
                ["Create", lambda *_: self.create_new_office(service.value, service_name.value)],
                "",
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Create Office")
        )
        self.swap(window)

    def open_office_prompt(self):
        ofc = InputField("", prompt="Choose an Office to use: ")
        window = (
            Window(
                "",
                ofc,
                "",
                ["Open", lambda *_: open_office(window, ofc.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Open Office")
        )
        self.swap(window)

    def close_office_prompt(self):
        window = (
            Window(
                "",
                "WIP",
                "",
                ["Continue", lambda *_: self.swap()],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Close Office")
        )
        self.swap(window)

    def hire_mailman_prompt(self):
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
                ["Create", lambda *_: self.hire_mailman(username.value, password.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Hire Mailman")
        )
        self.swap(window)

    def fire_mailman_prompt(self):
        window = (
            Window(
                "",
                "WIP",
                "",
                ["Continue", lambda *_: self.swap()],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Fire Mailman")
        )
        self.swap(window)

    def set_active_mailman_prompt(self):
        username = InputField("", prompt="Choose the Mailman to use: ")
        window = (
            Window(
                "",
                username,
                "",
                ["Continue", lambda *_: self.set_active_mailman(username.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Choose Mailman")
        )
        self.swap(window)

    def send_mail_prompt(self):
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
                ["Continue", lambda *_: self.send_mail(reciver.value, topic.value, body.value)],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Send Mail")
        )
        self.swap(window)
    
    def unrecognized_prompt(self):
        window = (
            Window(
                "",
                "Command not recognized",
                "",
                ["Continue", lambda *_: self.swap()],
                width=135,
                box="DOUBLE",
            )
            .set_title("[210 bold]Unrecongized Command")
        )
        self.swap(window)

    
