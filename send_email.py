import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def email(to_email, patient):
    message = Mail(
        from_email='lx66@duke.edu',
        to_emails=to_email,
        subject='WARNING about tachycardic heart rate',
        html_content='<strong>Patient {} exhibits a tachycardic '
                     'heart rate!!</strong>'.format(patient))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
    return None


if __name__ == "__main__":
    to_email = 'liangyuxu121@gmail.com'
    patient = 'Bob'
    email(to_email, patient)
