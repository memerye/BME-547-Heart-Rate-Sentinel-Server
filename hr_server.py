# hr_server.py
from flask import Flask, jsonify, request
import re
import logging

app = Flask(__name__)


def validate_patient_keys(patient_info):
    expected_keys = ["patient_id", "attending_email", "patient_age"]
    for key in patient_info.keys():
        if key not in expected_keys:
            return False
    return True


def validate_patient_id(patient_info):
    p_id = patient_info["patient_id"]
    try:
        num_id = int(p_id)
    except ValueError:
        return False
    return num_id


def validate_patient_email(patient_info):
    p_email = patient_info["attending_email"]
    try:
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        assert re.search(regex, p_email)
    except AssertionError:
        return False
    return p_email


def validate_patient_age(patient_info):
    p_age = patient_info["patient_age"]
    try:
        age = int(p_age)
    except ValueError:
        return False
    return age


@app.route("/api/new_patient", methods=["POST"])
def add_patients():
    logging.info("Creating information for a new patient...")
    indata = request.get_json()
    good_keys = validate_patient_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    p_id = validate_patient_id(indata)
    p_email = validate_patient_email(indata)
    p_age = validate_patient_age(indata)
    if p_id is False:
        return "Please enter a numeric patient ID.", 400
    if p_email is False:
        return "Please enter a valid email address.", 400
    if p_age is False:
        return "Please enter an integer age.", 400
    logging.info("* ID {} has been registered in server.".format(p_id))
    return "Valid patient data!"


def init_server():
    logging.basicConfig(filename='hr_server.log',
                        level=logging.INFO,
                        filemode='w')
    # database


if __name__ == "__main__":
    init_server()
    app.run()
