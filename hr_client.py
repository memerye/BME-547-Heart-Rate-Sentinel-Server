# hr_client.py
import requests


def post_a_patient(info):
    r = requests.post("http://127.0.0.1:5000/api/new_patient",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)


def post_heart_rate(info):
    r = requests.post("http://127.0.0.1:5000/api/heart_rate",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)


if __name__ == '__main__':
    info1 = {"patientid": "1",
             "attending_email": "dr_user_id@yourdomain.com",
             "patient_age": 50}
    post_a_patient(info1)
    info2 = {"patient_id": "2.5",
             "attending_email": "dr_user_id@yourdomain.com",
             "patient_age": 50}
    post_a_patient(info2)
    info3 = {"patient_id": "3",
             "attending_email": "dr_user_idyourdomain.com",
             "patient_age": 50}
    post_a_patient(info3)
    info4 = {"patient_id": "3",
             "attending_email": "dr_user_idyour@domain.com",
             "patient_age": "a50"}
    post_a_patient(info4)
    info5 = {"patient_id": "1",
             "attending_email": "dr_user_idyour@domain.com",
             "patient_age": 50}
    post_a_patient(info5)
    hr1 = {"patientid": "1", "heart_rate": 100}
    post_heart_rate(hr1)
    hr2 = {"patient_id": "1.5", "heart_rate": 100}
    post_heart_rate(hr2)
    hr3 = {"patient_id": "1", "heart_rate": 100.5}
    post_heart_rate(hr3)
    hr4 = {"patient_id": "1", "heart_rate": 100}
    post_heart_rate(hr4)
