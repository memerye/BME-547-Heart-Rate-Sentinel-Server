import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def email(to_email, p_id, hr, time):
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
