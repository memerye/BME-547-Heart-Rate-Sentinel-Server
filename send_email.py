import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def email(to_email, p_id, hr, time, send):
    """Send the mail to specific email address with the message of
    patient id, heart rate and the timestamp.

    Args:
        to_email (string): the receiver's email
        p_id (int): the patient id
        hr (int): the heart rate
        time (string): the timestamp
        send (bool): the flag of send email or not

    Returns:
        None
    """
    if send:
        message = Mail(
            from_email='lx66@duke.edu',
            to_emails=to_email,
            subject='WARNING about tachycardic heart rate',
            html_content='<strong><p>'
                         'Patient ID: {} <br />'
                         'time: {} <br />'
                         'heart rate: {} <br />'
                         'Exhibits tachycardic!'
                         '</p></strong>'.format(p_id, time, hr))
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))
    return None
