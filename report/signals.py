from django.dispatch import Signal
''' This file contains a list of all the signals which can be invoked whenever required
These signals are handled by the emailer App
For the implementation of each of these signals, see the emailer app, models.py file
To call these signal, invoke it as signal_name.send(sender="", feedback="")

As a writer, I shall be able to register as a listener when my Report has been validated/rejected by a reviewer

As a writer, I shall be able to register as a listener when my/following Report has been reported as inappropriate/duplicate

As a reviewer, I shall be able to register as a listener when Report is submitted for review

As a reviewer, I shall be able to register as a listener when Report is validated by other reviewers

As a reviewer, I shall be able to register as a listener when a report has been saved in the Enhanced CWE

As a writer, I shall be able to register as a listener when my/following Report has been commented on
'''
# Sent when the report is approved by the reviewer
report_accepted = Signal(providing_args=["instance"])

# Sent when the report is rejected by the reviewer
report_rejected = Signal(providing_args=["instance"])

# Sent when the report is submitted for review
report_submitted_review = Signal(providing_args=["instance"])

# Sent when the report is saved in the EnhancedCWE Application
report_saved_enhancedCWEApplication = Signal(providing_args=["instance"])

# Sent when the report is commented on
report_commented_on = Signal(providing_args=["instance"])

# Sent when the report is reviewed by any other reviewer
report_reviewed = Signal(providing_args=["instance"])







