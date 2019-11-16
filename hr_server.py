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
    """Validate the keys when posting a new patient.

    The keys of this posted patient information should
    only contain "patient_id", "attending_email", and
    "patient_age", otherwise it would be regarded as
    wrong information.

    Args:
        patient_info (dict): the posted patient data.

    Returns:
        bool: True if the keys are all valid;
              False if it contains wrong keys.
    """
    expected_keys = ["patient_id", "attending_email", "patient_age"]
    for key in patient_info.keys():
        if key not in expected_keys:
            return False
    return True


def validate_patient_id(patient_info):
    """Validate the patient id when posting a new patient.

    The id should be numeric whether it is an integer or a
    string containing an integer. eg: valid for 5 or "5",
    but not valid for 5.5, "5.5", "5a", etc.

    Args:
        patient_info (dict): the posted patient data.

    Returns:
        False: if it has wrong type of id;
        int: return the integer id if the id is valid.
    """
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
    """Validate the patient email when posting a new patient.

    The email should be valid with the username, @ symbol and
    the domain name. The username have to start with word
    characters (a-z, A-Z, 0-9 and underscore) and can contain
    . and -. The domain name can contain one or more times
    of a . followed by two or three word characters.

    Args:
        patient_info (dict): the posted patient data.

    Returns:
        False: if it has wrong type of email;
        string: return the string of email if the email is valid.
    """
    p_email = patient_info["attending_email"]
    try:
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        assert re.search(regex, p_email)
    except AssertionError:
        return False
    return p_email


def validate_patient_age(patient_info):
    """Validate the patient age when posting a new patient.

    The age should be numeric whether it is an integer or a
    string containing an integer. eg: valid for 5 or "5",
    but not valid for 5.5, "5.5", "5a", etc.

    Args:
        patient_info (dict): the posted patient data.

    Returns:
        False: if it has wrong type of age;
        int: return the integer age if the age is valid.
    """
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
    """Add a new patient to database.

    When add a new patient to the database, the patient only have
    the basic information of "patient_id", "attending_email",
    and "patient_age". "heart_rate", "status", and "timestamp"
    are all initialized as a list containing with single element 0.
    All of the updated information would be saved in the database.

    Args:
        p_json (dict): the posted patient data with the keys
        of "patient_id", "attending_email", and "patient_age".

    Returns:
        None
    """
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
    return None


@app.route("/api/new_patient", methods=["POST"])
def post_add_patients():
    """Post a new patient to the database.

    Before posting a new patient to database, the keys and the
    values in the posted json should all be validated first. Then
    the new patient can be registered in the server as well as saved
    in the database. The "patient_id" is the primary key for each
    patient, so it should be unique for each patient. If we upload
    the same "patient_id" to the database, it only update the
    information of that patient. If there are anything invalid in
    the posted json, the server will return error status codes with
    reasons.

    Returns:
        string: message to indicate the status of the server.
    """
    indata = request.get_json()
    print(type(indata))
    good_keys = validate_patient_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    p_id = validate_patient_id(indata)
    if p_id is False:
        return "Please enter a numeric patient ID.", 400
    p_email = validate_patient_email(indata)
    if p_email is False:
        return "Please enter a valid email address.", 400
    p_age = validate_patient_age(indata)
    if p_age is False:
        return "Please enter an integer age.", 400
    add_new_patient_to_db(indata)
    logging.info("* ID {} has been registered in server."
                 .format(p_id))
    return "Valid patient data!"


def validate_hr_keys(patient_hr):
    """Validate the keys when posting the heart rate of a patient.

    The keys of this posted patient heart rate should
    only contain "patient_id" and "heart_rate", otherwise
    it would be regarded as wrong information.

    Args:
        patient_hr (dict): the posted patient heart rate.

    Returns:
        bool: True if the keys are all valid;
              False if it contains wrong keys.
    """
    expected_keys = ["patient_id", "heart_rate"]
    for key in patient_hr.keys():
        if key not in expected_keys:
            return False
    return True


def validate_existing_id(p_id):
    """Validate the existence of the patient id in the database.

    Args:
        p_id (int): the patient id.

    Returns:
        bool: False if the id doesn't exist in the database;
              True if the id has been registered in the database.
    """
    id_list = []
    for p in Patient.objects.raw({}):
        id_list.append(p.patient_id)
    if p_id in id_list:
        return True
    else:
        return False


def validate_hr(patient_hr):
    """Validate the heart rate when posting the heart rate of a patient.

    The heart rate should be numeric whether it is an integer or a
    string containing an integer. eg: valid for 85 or "85", but not
    valid for 85.5, "85.5", "85a", etc.

    Args:
        patient_hr (dict): the posted patient heart rate.

    Returns:
        False: if it has wrong type of heart rate;
        int: return the integer age if the heart rate is valid.

    """
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
    """Check if the heart rate is tachycardic based on the age.

    Args:
        age (int): the patient age.
        hr (int): the heart rate of the patient.

    Returns:
        string: "tachycardic" or "not tachycardic".

    """
    if 1 <= age <= 2 and hr <= 151:
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
        return "tachycardic"


def age(p_id):
    """Get the age information of a patient if knowing the id.

    Args:
        p_id (int): the patient id.

    Returns:
        int: the patient age.
    """
    p_db_init = Patient.objects.raw({"_id": p_id}).first()
    return p_db_init.patient_age


def add_hr_to_db(p_json):
    """Add a new heart rate to database.

    When add new heart rate information to the database, we extract
    the patient information from the database by "patient_id". And
    put the values in json to the corresponding "heart_rate",
    "status", and "timestamp" as a list. All of the updated
    information would be saved in the database.

    Args:
        p_json (dict): the posted patient heart rate information
        with the keys of "patient_id", "heart_rate", "status",
        and "timestamp".

    Returns:
        None
    """
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
def post_heart_rate():
    """Post new patient heart rate information to the database.

    Before posting new patient heart rate information to database,
    the keys and the values in the posted json are all validated
    first. The existence of the patient id are checked next. All
    of the failures in validation and check would raise error in
    server. Then the new patient heart rate information can be
    registered in the server as well as saved in the database. The
    "patient_id" is still the primary key for each patient, we update
    the heart rate information including "heart_rate", "status", and
    "timestamp" based on id. If we upload the information with the
    same "patient_id" to the database, it would add the heart rate
    information as a list under that id. If there are anything invalid
    in the posted json, the server will return error status codes with
    reasons. If any of the heart rate exhibits tachycardic, an email
    will be sent to doctor's email.

    Returns:
        string: message to indicate the status of the server.
    """
    indata = request.get_json()
    good_keys = validate_hr_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    p_id = validate_patient_id(indata)
    if p_id is False:
        return "Please enter a numeric patient ID.", 400
    p_id_exist = validate_existing_id(p_id)
    if p_id_exist is False:
        return "The patient ID doesn't exist.", 400
    p_hr = validate_hr(indata)
    if p_hr is False:
        return "Please enter an integer heart rate.", 400
    p_age = age(p_id)
    indata["status"] = is_tachycardia(p_age, p_hr)
    indata["timestamp"] = str(datetime.now())
    add_hr_to_db(indata)
    if indata["status"] is "tachycardic":
        global to_email
        global flag_send_email
        email(to_email, p_id, p_hr, indata["timestamp"], flag_send_email)
        logging.warning("* Sent the email to {}."
                        "\n               Patient ID: {}"
                        "\n               Heart rate: {}"
                        .format(to_email, p_id, p_hr))
    return "Valid patient heart rate and saved to database!"


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    """
    This function returns a JSON containing the latest heart rate,
    as an integer, for the specified patient, whether this patient
    is currently tachycardic based on this most recently posted heart
    rate, and the date/time stamp of this most recent heart rate. If
    the patient id doesn't exist, the server will return error
    status codes with reasons.

    Args:
        patient_id (int): the patient id.

    Returns:
        False if no existing patient.
        json: a json message containing the latest "heart_rate",
        "status" and "timestamp".
    """
    flag = validate_existing_id(int(patient_id))
    if flag is False:
        return "Not existing Patient ID", 400
    else:
        p_db = Patient.objects.raw({"_id": int(patient_id)}).first()
        p_dict = {"heart_rate": p_db.heart_rate[-1],
                  "status": p_db.status[-1],
                  "timestamp": p_db.timestamp[-1]}
        return jsonify(p_dict)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_hr_list(patient_id):
    """Return all heart rate records of a patient.

    This function returns a list of all the previous heart rate
    records for the patient with specific id, as a list of integers.
    If the patient id doesn't exist, the server will return
    error status codes with reasons.

    Args:
        patient_id (int): the patient id.

    Returns:
        False if no existing patient.
        json: a json message containing a list of integers of heart rate.
    """
    flag = validate_existing_id(int(patient_id))
    if flag is False:
        return "Not existing Patient ID", 400
    else:
        p_db = Patient.objects.raw({"_id": int(patient_id)}).first()
        return jsonify(p_db.heart_rate)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_ave_hr(patient_id):
    """Calculate and return the average of all heart rate.

    This function returns the patient's average heart rate, as an integer,
    of all measurements have stored for this patient. If the patient id
    doesn't exist, the server will return error status codes with
    reasons.

    Args:
        patient_id (int): the patient id.

    Returns:
        False if no existing patient.
        json: a json message of the averaged integer heart rate.
    """
    flag = validate_existing_id(int(patient_id))
    if flag is False:
        return "Not existing Patient ID", 400
    else:
        p_db = Patient.objects.raw({"_id": int(patient_id)}).first()
        hr = p_db.heart_rate
        hr_ave = int(sum(hr)/len(hr))
        return jsonify(hr_ave)


def validate_avr_hr_keys(patient_hr):
    """Validate the keys when posting interval average.

    The keys of this posted interval average should only
    contain "patient_id" and "heart_rate_average_since",
    otherwise it would be regarded as wrong information.

    Args:
        patient_hr (dict): the posted information for interval average.

    Returns:
        bool: True if the keys are all valid;
              False if it contains wrong keys.
    """
    expected_keys = ["patient_id", "heart_rate_average_since"]
    for key in patient_hr.keys():
        if key not in expected_keys:
            return False
    return True


def validate_time(indata):
    """Validate the tiemstamp when posting interval average.

    The posted value for "heart_rate_average_since" should follow
    the format of "year-month-day hour:mimute:second.Microsecond".

    Args:
        indata (dict): the posted information for interval average.

    Returns:
        False if the timestamp is not valid;
        string: the timestamp if it is valid.
    """
    time = indata["heart_rate_average_since"]
    try:
        datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    except TypeError:
        return False
    except ValueError:
        return False
    else:
        return time


def hr_and_t(p_id):
    """Get the list of heart rate and timestamp based on patient id.

    Args:
        p_id (int): the patient id.

    Returns:
        int: the heart rate.
        string: the timestamp
    """
    p_db = Patient.objects.raw({"_id": int(p_id)}).first()
    hrs = p_db.heart_rate
    timestamps = p_db.timestamp
    return hrs, timestamps


def ave_hr_since(p_id, start_t_str):
    """Get the interval heart rate average.

    The function returns the average, as an integer, of all
    the heart rates that have been posted for the specified
    patient since the given date/time. If no heart rate before
    this given date/time, the function will return False.

    Args:
        p_id (int): the patient id.
        start_t_str (string): the start time to compute the average.

    Returns:
        False if NO heart rate before given timestamp.
        int: average interval heart rate.

    """
    start_t = datetime.strptime(start_t_str, '%Y-%m-%d %H:%M:%S.%f')
    hrs, timestamps = hr_and_t(p_id)
    hr_list = []
    for t, hr in zip(timestamps, hrs):
        record_t = datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
        if record_t > start_t:
            hr_list.append(hr)
    if len(hr_list) == 0:
        return False
    else:
        hr_ave = int(sum(hr_list) / len(hr_list))
        return hr_ave


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_ave_hr_since():
    """Post interval heart rate based on the given date/time.

    The "heart_rate_average_since" will be a datetime string in the
    format of "year-month-day hour:mimute:second.Microsecond". This
    POST returns the average, as an integer, of all the heart rates
    that have been posted for the specified patient since the given
    date/time. If no heart rate before this given date/time, the
    server will return error status code.

    Returns:
        string: message to indicate the status of the server.
    """
    indata = request.get_json()
    good_keys = validate_avr_hr_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    p_id = validate_patient_id(indata)
    if p_id is False:
        return "Please enter a numeric patient ID.", 400
    p_id_exist = validate_existing_id(p_id)
    if p_id_exist is False:
        return "The patient ID doesn't exist.", 400
    t_start = validate_time(indata)
    if t_start is False:
        return "Please enter the valid datetime with " \
               "format '%Y-%m-%d %H:%M:%S.%f'", 400
    hr_ave = ave_hr_since(p_id, t_start)
    if hr_ave:
        return jsonify(hr_ave)
    else:
        return "No heart rate record before this timestamp.", 400


def init_server():
    """Initialize the logging configuration and database connection.

    Returns:
        None.
    """
    logging.basicConfig(filename='hr_server.log',
                        level=logging.INFO,
                        filemode='w')
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")
    return None


if __name__ == "__main__":
    to_email = 'liangyuxu121@gmail.com'
    flag_send_email = True
    init_server()
    app.run()
