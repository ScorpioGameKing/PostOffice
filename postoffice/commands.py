from enum import StrEnum

class Commands(StrEnum):
    EXIT = "exit"
    HELP = "help"

    CREATE_OFFICE = "create_office"
    OPEN_OFFICE = "open_office"
    CLOSE_OFFICE = "close_office"

    HIRE_MAILMAN = "hire_mailman"
    FIRE_MAILMAN = "fire_mailman"
    SET_ACTIVE_MAILMAN = "set_active_mailman"
    SEND_MAIL = "send_mail"

class Help(StrEnum):
    EXIT = "CMD: exit USEAGE: To exit out of the application"
    HELP = "CMD: help USEAGE: To Print this menu"

    CREATE_OFFICE = "CMD: create_office USEAGE: Create new Office to handle a service"
    OPEN_OFFICE = "CMD: open_office USEAGE: Set the Active Office"
    CLOSE_OFFICE = "CMD: close_office USEAGE: Destroy the Active Office"

    HIRE_MAILMAN = "CMD: hire_mailman USEAGE: Create a new Mailman for the current office"
    FIRE_MAILMAN = "CMD: fire_mailman USEAGE: Delete the selected Mailman"
    SET_ACTIVE_MAILMAN = "CMD: set_active_mailman USEAGE: Select the Mailman to send emails with"
    SEND_MAIL = "CMD: send_mail USEAGE: Send an email with the Active Mailman"
