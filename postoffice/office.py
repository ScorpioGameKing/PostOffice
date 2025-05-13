from postoffice.mailman import Mailman
from redmail import gmail, EmailSender
from redbox import EmailBox

class Office():
    _office_service:EmailSender
    _mailmen:dict[str:Mailman]
    _activeMailman:Mailman

    def __init__(self, service:EmailSender):
        self._office_service = service
        self._mailmen = {}

    def hireMailman(self, username:str, password:str):
        _temp_mailman = Mailman(username, password)
        self._mailmen.update({username : _temp_mailman})

    def fireMailman(self, username:str):
        self._mailmen.pop(username)

    def setActiveMailman(self, username:str):
        self._activeMailman = self._mailmen[username]
        self._office_service.username = self._activeMailman.name
        self._office_service.password = self._activeMailman._password
    
    def sendMail(self, topic:str, send_to:list[str], body:str):
        self._activeMailman.sendMail(self._office_service, topic, send_to, body)
