from redmail import gmail
from postoffice.office import Office
from postoffice.commands import Commands, Help

def main():
    home_office:Office
    office_space = {}

    print("WELCOME TO MAILMAN!")
    while True:
        print("Please enter command")
        cmd = input()
        match cmd:
            case Commands.EXIT:
                print("Exiting Mailman, have a nice day!")
                exit()

            case Commands.HELP:
                for tip in Help:
                    print(tip)

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

            case _:
                print("Command not reconigzed")

if __name__ == "__main__":
    main()