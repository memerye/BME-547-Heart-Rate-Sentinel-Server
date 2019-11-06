# hr_client.py
import requests


def add_a_patient(info):
    r = requests.post("http://vcm-11671.vm.duke.edu:5000/api/new_patient",
                      json=info)
    print(r.json())


if __name__ == '__main__':
    patient_info = {
        "patient_id": "1",
        "attending_email": "dr_user_id@yourdomain.com",
        "patient_age": "50"
    }
    add_a_patient(patient_info)
