from django.dispatch import Signal
''' This file contains a list of all the signals which can be invoked whenever required
These signals are handled by the report_mailer App
For the implementation of each of these signals, see the report_mailer app, signal_handlers.py file
To call these signal, invoke it as signal_name.send(sender="", feedback="")
'''

# Sent when the report is approved by the reviewer
report_accepted = Signal(providing_args=["instance"])

# Sent when the report is rejected by the reviewer
report_rejected = Signal(providing_args=["instance"])

# Sent when the report is submitted for review
report_submitted_review = Signal(providing_args=["instance"])

# Sent when the report is saved in the EnhancedCWE Application - Not tested
report_saved_enhancedCWEApplication = Signal(providing_args=["instance"])





