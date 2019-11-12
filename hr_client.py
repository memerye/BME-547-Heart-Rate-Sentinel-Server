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


def test_validate_infos():
    p_info = [{"patientid": "1",
               "attending_email": "dr_user_id@yourdomain.com",
               "patient_age": 50},
              {"patient_id": "2.5",
               "attending_email": "dr_user_id@yourdomain.com",
               "patient_age": 50},
              {"patient_id": "3",
               "attending_email": "dr_user_idyourdomain.com",
               "patient_age": 50},
              {"patient_id": "4",
               "attending_email": "dr_user_idyour@domain.com",
               "patient_age": "a50"},
              {"patient_id": "5",
               "attending_email": "dr_user_idyour@domain.com",
               "patient_age": 50},
              {"patient_id": "6",
               "attending_email": "6666@domain.com",
               "patient_age": 14},
              {"patient_id": "7",
               "attending_email": "7777@domain.com",
               "patient_age": 1}]
    for info in p_info:
        post_a_patient(info)
    return None


def test_validate_hr_infos():
    p_hr = [{"patientid": "5", "heart_rate": 100},
            {"patient_id": "5.5", "heart_rate": 100},
            {"patient_id": "5", "heart_rate": 100.5},
            {"patient_id": "5", "heart_rate": 100},
            {"patient_id": "5", "heart_rate": 120},
            {"patient_id": "5", "heart_rate": 80},
            {"patient_id": "6", "heart_rate": 110},
            {"patient_id": "6", "heart_rate": 130},
            {"patient_id": "6", "heart_rate": 100},
            {"patient_id": "7", "heart_rate": 140},
            {"patient_id": "7", "heart_rate": 100},
            {"patient_id": "7", "heart_rate": 160}]
    for hr in p_hr:
        post_heart_rate(hr)
    return None


if __name__ == '__main__':
    test_validate_infos()
    test_validate_hr_infos()
