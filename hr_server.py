# hr_server.py
from flask import Flask, jsonify, request
import re
import math
import logging
from datetime import datetime
from pymodm import connect
from pymodm import MongoModel, fields
from send_email import email

app = Flask(__name__)


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    patient_age = fields.FloatField()
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
        age = float(p_age)
        assert not math.isnan(age)
    except ValueError:
        return False
    except AssertionError:
        return False
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
        logging.error("The dictionary keys are not correct.")
        return "The dictionary keys are not correct.", 400
    p_id = validate_patient_id(indata)
    p_email = validate_patient_email(indata)
    p_age = validate_patient_age(indata)
    if p_id is False:
        logging.error("Please enter a numeric patient ID.")
        return "Please enter a numeric patient ID.", 400
    if p_email is False:
        logging.error("Please enter a valid email address.")
        return "Please enter a valid email address.", 400
    if p_age is False:
        logging.error("Please enter an integer age.")
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


def is_tachycardia(age, hr):
    if age <= 2/365 and hr <= 159:
        return "not tachycardic"
    elif 3/365 <= age <= 6/365 and hr <= 166:
        return "not tachycardic"
    elif 7/365 <= age <= 21/365 and hr <= 182:
        return "not tachycardic"
    elif 22/365 <= age <= 60/365 and hr <= 179:
        return "not tachycardic"
    elif 90/365 <= age <= 150/365 and hr <= 186:
        return "not tachycardic"
    elif 180/365 <= age <= 330/365 and hr <= 169:
        return "not tachycardic"
    elif 331/365 <= age <= 2 and hr <= 151:
        return "not tachycardic"
    elif 3 <= age <= 4 and hr <= 137:
        return "not tachycardic"
    elif 5 <= age <= 7 and hr <= 133:
        return "not tachycardic"
    elif 8 <= age <= 11 and hr <= 130:
        return "not tachycardic"
    elif 12 <= age <= 15 and hr <= 119:
        return "not tachycardic"
    elif age > 15 and hr <= 100:
        return "not tachycardic"
    else:
        logging.warning("Exhibiting a tachycardic heart rate")
        return "tachycardic"


def get_age(p_id):
    p_db_init = Patient.objects.raw({"_id": p_id}).first()
    return p_db_init.patient_age


def add_hr_to_db(p_json):
    p_id = int(p_json["patient_id"])
    p_db = Patient.objects.raw({"_id": p_id}).first()
    if p_db.timestamp[0] == 0:
        p_db.heart_rate[0] = int(p_json["heart_rate"])
        p_db.status[0] = p_json["status"]
        p_db.timestamp[0] = p_json["timestamp"]
        p_db.save()
    else:
        p_db.heart_rate.append(int(p_json["heart_rate"]))
        p_db.status.append(p_json["status"])
        p_db.timestamp.append(p_json["timestamp"])
        p_db.save()
    return None


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    logging.info("Receiving heart rate from a patient...")
    indata = request.get_json()
    good_keys = validate_hr_keys(indata)
    if good_keys is False:
        logging.error("The dictionary keys are not correct.")
        return "The dictionary keys are not correct.", 400
    p_id = validate_patient_id(indata)
    p_hr = validate_hr(indata)
    if p_id is False:
        logging.error("Please enter a numeric patient ID.")
        return "Please enter a numeric patient ID.", 400
    if p_hr is False:
        logging.error("The heart rate should be an integer.")
        return "The heart rate should be an integer.", 400
    p_age = get_age(p_id)
    indata["status"] = is_tachycardia(p_age, p_hr)
    indata["timestamp"] = str(datetime.now())
    logging.info("Saving the heart rate of patient into the database...")
    add_hr_to_db(indata)
    logging.info("* Saved heart rate of ID {} in database.".format(p_id))
    if indata["status"] is "tachycardic":
        global to_email
        email(to_email, p_id, p_hr, indata["timestamp"])
        logging.warning("* Sent the email to {}".format(to_email))
    logging.info("* Server receives the heart rate of ID {} "
                 "and saves it to database.".format(p_id))
    return "Valid patient heart rate and saved to database!"


@app.route("/api/status/<patient_id>", methods=["GET"])
def status(patient_id):
    p_db = Patient.objects.raw({"_id": int(patient_id)}).first()
    p_dict = {"heart_rate": p_db.heart_rate[-1],
              "status": p_db.status[-1],
              "timestamp": p_db.timestamp[-1]}
    return jsonify(p_dict)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def hr_list(patient_id):
    p_db = Patient.objects.raw({"_id": int(patient_id)}).first()
    return jsonify(p_db.heart_rate)


def init_server():
    logging.basicConfig(filename='hr_server.log',
                        level=logging.INFO,
                        filemode='w')
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")


if __name__ == "__main__":
    to_email = 'liangyuxu121@gmail.com'
    init_server()
    app.run()
