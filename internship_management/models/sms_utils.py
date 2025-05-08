from twilio.rest import Client

def send_sms(to_number, message, twilio_sid, twilio_token, twilio_number):
    client = Client(twilio_sid, twilio_token)
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number
    )
