import smtplib, ssl

class Notification_sink:

    def __init__(self, ssl_port, smtp_server, sender_email, receiver_email, password):
        self.ssl_port = ssl_port
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = password

    def notify(self, text):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        with smtplib.SMTP_SSL(self.smtp_server, self.ssl_port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, text)
            server.close()


