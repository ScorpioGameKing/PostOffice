from redmail import EmailSender

class Mailman():
    name:str
    _password:str

    def __init__(self, username:str, password:str):
        self.name = username
        self._password = password
    
    def sendMail(self, service:EmailSender, topic:str, send_to:list[str], body:str):
        print(f'TOPIC: {topic} \n SEND LIST: {send_to} \n BODY: {body}')
        service.send(
            subject=topic,
            receivers=send_to,
            text=body
            )