import firebase_admin
from firebase_admin import credentials, messaging


if not firebase_admin._apps:

    cred = credentials.Certificate(
        "firebase-service-account.json"
    )

    firebase_admin.initialize_app(cred)



class NotificationService:

    @staticmethod
    def send_sos_notification(tokens):

        message = messaging.MulticastMessage(

            notification=messaging.Notification(
                title="SOS ALERT",
                body="Your guardian needs help"
            ),

            data={
                "type": "SOS",
                "title": "SOS ALERT",
                "body": "Your guardian needs help"
            },

            tokens=tokens

        )


        response = messaging.send_each_for_multicast(
            message
        )


        return response