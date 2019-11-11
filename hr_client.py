# hr_client.py
import requests


def post_a_patient(info):
    r = requests.post("http://127.0.0.1:5000/api/new_patient",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)


if __name__ == '__main__':
    info1 = {"patient_id": "1",
             "attending_email": "dr_user_id@yourdomain.com",
             "patient_age": 50}
    post_a_patient(info1)
    info2 = {"patientid": "2",
             "attending_email": "dr_user_id@yourdomain.com",
             "patient_age": 50}
    post_a_patient(info2)
    info3 = {"patient_id": "3",
             "attending_email": "dr_user_idyourdomain.com",
             "patient_age": 50}
    post_a_patient(info3)
