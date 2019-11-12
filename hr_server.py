# hr_server.py
from flask import Flask, jsonify, request
import re
import logging
from datetime import datetime
from pymodm import connect
from pymodm import MongoModel, fields

app = Flask(__name__)


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    patient_age = fields.IntegerField()
    heart_rate = fields.ListField()
    status = fields.ListField()
    timestamp = fields.ListField()


def validate_patient_keys(patient_info):
    expected_keys = ["patient_id", "attending_email", "patient_age"]
    for key in patient_info.keys():
        if key not in expected_keys:
            return False
    return True


def validate_patient_id(patient_info):
    p_id = patient_info["patient_id"]
    try:
        float(p_id)
    except ValueError:
        return False
    try:
        assert float(p_id).is_integer()
    except AssertionError:
        return False
    else:
        num_id = int(p_id)
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
        float(p_age)
    except ValueError:
        return False
    try:
        assert float(p_age).is_integer()
    except AssertionError:
        return False
    else:
        age = int(p_age)
    return age


def add_new_patient_to_db(p_json):
    logging.info("Saving the new patient into the database...")
    p_id = int(p_json["patient_id"])
    p_email = p_json["attending_email"]
    p_age = int(p_json["patient_age"])
    p = Patient(patient_id=p_id,
                attending_email=p_email,
                patient_age=p_age,
                heart_rate=[0],
                status=[0],
                timestamp=[0])
    p.save()
    logging.info("* ID {} has been saved in database.".format(p_id))
    return None


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
    add_new_patient_to_db(indata)
    return "Valid patient data!"


def validate_hr_keys(patient_hr):
    expected_keys = ["patient_id", "heart_rate"]
    for key in patient_hr.keys():
        if key not in expected_keys:
            return False
    return True


def validate_hr(patient_hr):
    p_hr = patient_hr["heart_rate"]
    try:
        float(p_hr)
    except ValueError:
        return False
    try:
        assert float(p_hr).is_integer()
    except AssertionError:
        return False
    else:
        num_hr = int(p_hr)
    return num_hr


def add_hr_to_db(p_json):
    logging.info("Saving the heart rate of patient into the database...")
    p_id = int(p_json["patient_id"])
    p_db = Patient.objects.raw({"_id": p_id}).first()
    p_db.heart_rate = int(p_json["heart_rate"])
    p_db.status = p_json["status"]
    p_db.timestamp = p_json["timestamp"]
    p_db.save()
    logging.info("* Saved heart rate of ID {} in database.".format(p_id))
    return None


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    logging.info("Receiving heart rate from a patient...")
    indata = request.get_json()
    good_keys = validate_hr_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    p_id = validate_patient_id(indata)
    p_hr = validate_hr(indata)
    if p_id is False:
        return "Please enter a numeric patient ID.", 400
    if p_hr is False:
        return "The heart rate should be an integer.", 400
    logging.info("* Server receives the heart rate of ID {}.".format(p_id))
    timestamp = str(datetime.now())
    # add_hr_to_db(indata)
    return "Valid patient heart rate!"


def init_server():
    logging.basicConfig(filename='hr_server.log',
                        level=logging.INFO,
                        filemode='w')
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")


if __name__ == "__main__":
    init_server()
    app.run()
