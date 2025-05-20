import logging
from postoffice.mailman import Mailman
from redmail import gmail, EmailSender
from redbox import EmailBox

class Office():
    _office_service:EmailSender
    _mailmen:dict[str:Mailman]
    _activeMailman:Mailman

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._office_service = gmail # Default to gmail
        self._mailmen = {}
        self.logger.info(f"Created Mailman Directory As [{self._mailmen}]")
    
    def set_service(self, service:EmailSender) -> None:
        self._office_service = service
        self.logger.info(f"Set Service to [{self._office_service}]")

    def hireMailman(self, username:str, password:str):
        _temp_mailman = Mailman(username, password)
        self._mailmen.update({username : _temp_mailman})
        self.logger.info(f"Created Mailman [{username}] as [{_temp_mailman}] in [{self._mailmen}]")

    def fireMailman(self, username:str):
        self._mailmen.pop(username)
        self.logger.info(f"Popped Mailman [{username}] from [{self._mailmen}]")

    def setActiveMailman(self, username:str):
        self.logger.info(f"Searching for Mailman [{self._mailmen[username]}]")
        self._activeMailman = self._mailmen[username]
        self.logger.info(f"Setting Service Password [{self._activeMailman._password}]")
        self._office_service.password = self._activeMailman._password
        self.logger.info(f"Setting Service Username [{self._activeMailman.name}]")
        self._office_service.username = self._activeMailman.name
    
    def sendMail(self, topic:str, send_to:list[str], body:str):
        self._activeMailman.sendMail(self._office_service, topic, send_to, body)
