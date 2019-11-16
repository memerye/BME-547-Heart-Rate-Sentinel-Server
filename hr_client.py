# hr_client.py
import requests


def post_a_patient(info):
    """The client function of posting a new patient.

    Args:
        info (dict): the dictionary of patient's information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/new_patient",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)


def post_heart_rate(info):
    """The client function of posting a new heart rate.

    Args:
        info (dict): the dictionary of patient's information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/heart_rate",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)


def post_ave_heart_rate_since(info):
    """The client function of posting a timestamp to get the interval average.

    Args:
        info (dict): the dictionary of patient's information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)


def test_add_patients():
    """Create a pseudo-list of patients information to
    add into the server and database.

    The pseudo-list of patients contains error of:
    (1) wrong dictionary keys
    (2) invalid patient id
    (3) invalid patient email address
    (4) invalid patient age
    And three valid patient information with the id of 5, 6, and 7.

    Returns:
        None
    """
    p_info = [{"patientid": "1",
               "attending_email": "dr_user_id@yourdomain.com",
               "patient_age": 50},
              {"patient_id": "2.5a",
               "attending_email": "dr_user_id@yourdomain.com",
               "patient_age": 50},
              {"patient_id": "3",
               "attending_email": "dr_user_idyourdomain.com",
               "patient_age": 50},
              {"patient_id": "4",
               "attending_email": "dr_user_idyour@domain.com",
               "patient_age": "a50"},
              {"patient_id": "5",
               "attending_email": "5555@domain.com",
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


def test_heart_rate():
    """Create a pseudo-list of patients heart rate information to
    add into the server and database.

    The pseudo-list of patients contains error of:
    (1) wrong dictionary keys
    (2) invalid patient id
    (3) not exist patient id
    (4) invalid patient heart rate
    And nine valid patient hear rate information equally distributed
    with the id of 5, 6, and 7.

    Returns:
        None
    """
    p_hr = [{"patientid": "5", "heart_rate": 100},
            {"patient_id": "5.5", "heart_rate": 100},
            {"patient_id": "8", "heart_rate": 100},
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


def test_ave_hr_since():
    """Create a pseudo-list of time information to calculate the
    interval average heart rate.

    The pseudo-list of patients contains error of:
    (1) wrong dictionary keys
    (2) invalid patient id
    (3) not exist patient id
    (3) invalid timestamp
    (4) no timestamp in database is ahead of given timestamp
    And one valid time information to calculate the interval average
    heart rate of id 5 since "2019-11-12 16:16:38.991052".

    Returns:
        None
    """
    hr_since = [{"patientid": "5",
                 "heart_rate_average_since": "2020-11-12 16:15:38.991052"},
                {"patient_id": "5a",
                 "heart_rate_average_since": "2020-11-12 16:15:38.991052"},
                {"patient_id": "8",
                 "heart_rate_average_since": "2020-11-12 16:15:38.991052"},
                {"patient_id": "5",
                 "heart_rate_average_since": "2020-11-12 16:15:38"},
                {"patient_id": "5",
                 "heart_rate_average_since": "2020-11-12 16:15:38.991052"},
                {"patient_id": "5",
                 "heart_rate_average_since": "2019-11-12 16:16:38.991052"}]
    for hr in hr_since:
        post_ave_heart_rate_since(hr)
    return None


def request_on_status():
    """The client function of getting heart rate status of a patient

    The result will be printed out.

    Returns:
        None
    """
    ids = [8, 5]
    for p_id in ids:
        r = requests.get("http://127.0.0.1:5000/api/status/{}".format(p_id))
        print(r)
        print(r.text)
        print(r.status_code)
        if r.status_code == 200:
            answer = r.json()
            print(answer)


def request_on_hr_list():
    """The client function of getting heart rate list of a patient

    The result will be printed out.

    Returns:
        None
    """
    ids = [8, 5]
    for p_id in ids:
        r = requests.get("http://127.0.0.1:5000/api/heart_rate/{}"
                         .format(p_id))
        print(r)
        print(r.text)
        print(r.status_code)
        if r.status_code == 200:
            answer = r.json()
            print(answer)


def request_on_ave_hr():
    """The client function of getting average heart rate of a patient

    The result will be printed out.

    Returns:
        None
    """
    ids = [8, 5]
    for p_id in ids:
        r = requests.get("http://127.0.0.1:5000/api/heart_rate/average/{}"
                         .format(p_id))
        print(r)
        print(r.text)
        print(r.status_code)
        if r.status_code == 200:
            answer = r.json()
            print(answer)


if __name__ == '__main__':
    test_add_patients()
    test_heart_rate()
    test_ave_hr_since()
    request_on_status()
    request_on_hr_list()
    request_on_ave_hr()
