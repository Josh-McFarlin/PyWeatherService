from twilio.rest import Client


class Twilio:
    account_sid = ""
    auth_token = ""
    from_number = ""

    def __init__(self, sid, token, from_number):
        self.account_sid = sid
        self.auth_token = token
        self.from_number = from_number
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, to, message_text, image_url=None):
        if image_url:
            message = self.client.messages.create(
                to=to,
                body=message_text,
                from_=self.from_number,
                media_url=image_url)
        else:
            message = self.client.messages.create(
                to=to,
                body=message_text,
                from_=self.from_number)
