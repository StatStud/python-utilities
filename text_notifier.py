import smtplib
import os
import atexit
import sys
import traceback

class SimpleTextNotifier:
    def __init__(self):
        carrier="att"
        self.email = <your_email>
        self.password = <your_app_passcode>
        phone_number = <your_number_to_send_to>
        self.recipient = f"{phone_number}@{self._get_carrier_gateway(carrier)}"
        self.script_name = os.path.basename(sys.argv[0])
        self.error_occurred = False
        atexit.register(self._send_completion_message)
        sys.excepthook = self._handle_exception

    def _get_carrier_gateway(self, carrier):
        carriers = {
            "att": "mms.att.net",
            "tmobile": "tmomail.net",
            "verizon": "vtext.com",
            "sprint": "messaging.sprintpcs.com"
        }
        return carriers.get(carrier.lower(), "mms.att.net")

    def _send_message(self, message):
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.recipient, message)

    def _send_completion_message(self):
        if not self.error_occurred:
            self._send_message(f"Script {self.script_name} completed successfully")

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        self.error_occurred = True
        error_msg = f"Script {self.script_name} failed"
        #error_msg += f"Error: {exc_type.__name__}: {exc_value}\n"
        #error_msg += "Traceback (most recent call last):\n"
        #error_msg += "".join(traceback.format_tb(exc_traceback))
        self._send_message(error_msg)
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

def init_notifier():
    return SimpleTextNotifier()
