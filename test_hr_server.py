# test_hr_server.py
import pytest
from pymodm import connect


@pytest.mark.parametrize("patient_info, expected", [
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, True),
    ({"patient_ID": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, False),
    ({"patient_id": "1",
      "attending_mail": "dr_user_id@yourdomain.com",
      "patient_age": 50}, False)
])
def test_validate_patient_keys(patient_info, expected):
    """Test the function validate_patient_keys.

    Args:
        patient_info (dict): the posted patient data.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_patient_keys
    result = validate_patient_keys(patient_info)
    assert result == expected


@pytest.mark.parametrize("patient_info, expected", [
    ({"patient_id": 1,
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, 1),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, 1),
    ({"patient_id": "nan",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, False),
    ({"patient_id": "1.5",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, False),
    ({"patient_id": "A1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, False)
])
def test_validate_patient_id(patient_info, expected):
    """Test function validate_patient_id.

    Args:
        patient_info (dict): the posted patient data.
        expected (bool or int): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_patient_id
    result = validate_patient_id(patient_info)
    assert result == expected


@pytest.mark.parametrize("patient_info, expected", [
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, "dr_user_id@yourdomain.com"),
    ({"patient_id": "1",
      "attending_email": "dr_user_idyourdomain.com",
      "patient_age": 50}, False),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomaincom",
      "patient_age": 50}, False)
])
def test_validate_patient_email(patient_info, expected):
    """Test function validate_patient_email.

    Args:
        patient_info (dict): the posted patient data.
        expected (bool or int): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_patient_email
    result = validate_patient_email(patient_info)
    assert result == expected


@pytest.mark.parametrize("patient_info, expected", [
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, 50),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "50.5"}, 50.5),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "nan"}, False),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "a50"}, False)
])
def test_validate_patient_age(patient_info, expected):
    """Test function validate_patient_age.

    Args:
        patient_info (dict): the posted patient data.
        expected (bool or int): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_patient_age
    result = validate_patient_age(patient_info)
    assert result == expected


@pytest.mark.parametrize("p_info, e_id, e_email, e_age", [
    ({"patient_id": "100",
      "attending_email": "100@yourdomain.com",
      "patient_age": 50}, 100, "100@yourdomain.com", 50),
    ({"patient_id": "100",
      "attending_email": "100new@yourdomain.com",
      "patient_age": 50}, 100, "100new@yourdomain.com", 50),
    ({"patient_id": "200",
      "attending_email": "200@yourdomain.com",
      "patient_age": 10}, 200, "200@yourdomain.com", 10),
])
def test_add_new_patient_to_db(p_info, e_id, e_email, e_age):
    """Test function add_new_patient_to_db.

    Args:
        p_info (dict): the posted patient data with the keys
        e_id: expected patient id
        e_email: expected patient email
        e_age: expected patient age

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import add_new_patient_to_db, Patient
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")
    add_new_patient_to_db(p_info)
    p = Patient.objects.raw({"_id": int(p_info["patient_id"])}).first()
    assert p.patient_id == e_id
    assert p.attending_email == e_email
    assert p.patient_age == e_age


@pytest.mark.parametrize("patient_hr, expected", [
    ({"patient_id": "1",
      "heart_rate": 100}, True),
    ({"patientid": "1",
      "heart_rate": 100}, False),
    ({"patient_id": "1",
      "heart_rat": 100}, False)
])
def test_validate_hr_keys(patient_hr, expected):
    """Test the function validate_hr_keys.

    Args:
        patient_hr (dict): the posted patient heart rate.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_hr_keys
    result = validate_hr_keys(patient_hr)
    assert result == expected


@pytest.mark.parametrize("p_id, expected", [(100, True), (101, False)])
def test_validate_existing_id(p_id, expected):
    """Test function validate_existing_id

    Args:
        p_id (int): the patient id.
        expected (bool): the existence of the id in database

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_existing_id
    result = validate_existing_id(p_id)
    assert result == expected


@pytest.mark.parametrize("patient_hr, expected", [
    ({"patient_id": "1",
      "heart_rate": 100}, 100),
    ({"patient_id": "1",
      "heart_rate": "100"}, 100),
    ({"patient_id": "1",
      "heart_rate": "nan"}, False),
    ({"patient_id": "1",
      "heart_rate": "60.5"}, False),
    ({"patient_id": "1",
      "heart_rate": "a100"}, False)
])
def test_validate_hr(patient_hr, expected):
    """Test function validate_hr.

    Args:
        patient_hr (dict): the posted patient heart rate.
        expected (bool or int): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_hr
    result = validate_hr(patient_hr)
    assert result == expected


@pytest.mark.parametrize("age, hr, expected", [
    (1, 150, "not tachycardic"),
    (1, 160, "tachycardic"),
    (3, 130, "not tachycardic"),
    (3, 140, "tachycardic"),
    (6, 130, "not tachycardic"),
    (6, 140, "tachycardic"),
    (10, 120, "not tachycardic"),
    (10, 140, "tachycardic"),
    (12, 110, "not tachycardic"),
    (12, 120, "tachycardic"),
    (20, 90, "not tachycardic"),
    (20, 110, "tachycardic")
])
def test_is_tachycardia(age, hr, expected):
    """Test function is_tachycardia

    Args:
        age (int): the patient age.
        hr (int): the heart rate of the patient.
        expected (string): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import is_tachycardia
    result = is_tachycardia(age, hr)
    assert result == expected


@pytest.mark.parametrize("p_id, e_age, e_email",
                         [(100, 50, "100new@yourdomain.com")])
def test_age_and_email(p_id, e_age, e_email):
    """Test function age_and_email

    Args:
        p_id (int): the patient id.
        e_age (string): the expected result of the age.
        e_email (string): the expected result of the email.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import age_and_email, Patient
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")
    e_age, e_email = age_and_email(p_id)
    p = Patient.objects.raw({"_id": p_id}).first()
    assert p.patient_age == e_age
    assert p.attending_email == e_email


@pytest.mark.parametrize("hr_info, e_id, e_hr, e_status, e_timestamp", [
    ({"patient_id": "100", "heart_rate": 120,
      "status": "tachycardic",
      "timestamp": '2019-11-12 13:05:35.00'},
     100, [120], ["tachycardic"], ['2019-11-12 13:05:35.00']),
    ({"patient_id": "100", "heart_rate": 80,
      "status": "not tachycardic",
      "timestamp": '2019-11-12 13:06:35.00'},
     100, [120, 80], ["tachycardic", "not tachycardic"],
     ['2019-11-12 13:05:35.00', '2019-11-12 13:06:35.00'])
])
def test_add_hr_to_db(hr_info, e_id, e_hr, e_status, e_timestamp):
    """Test function add_hr_to_db

    Args:
        hr_info (dict): the posted patient heart rate information
        with the keys of "patient_id", "heart_rate", "status",
        and "timestamp".
        e_id (int): the expected patient id
        e_hr (int): the expected patient heart rate
        e_status (string): the expected patient heart rate status
        e_timestamp (string): the expected timestamp

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import add_hr_to_db, Patient
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")
    add_hr_to_db(hr_info)
    p = Patient.objects.raw({"_id": int(hr_info["patient_id"])}).first()
    assert p.patient_id == e_id
    assert p.heart_rate == e_hr
    assert p.status == e_status
    assert p.timestamp == e_timestamp


@pytest.mark.parametrize("indata, expected", [
    ({"patient_id": "100",
      "heart_rate_average_since": "2019-11-11 11:00:00.00"}, True),
    ({"patientid": "100",
      "heart_rate_average_since": "2020-11-11 11:00:00.00"}, False),
    ({"patient_id": "100",
      "heartrate_average_since": "2020-11-11 11:00:00.00"}, False)
])
def test_validate_avr_hr_keys(indata, expected):
    """Test function validate_avr_hr_keys

    Args:
        indata (dict): the posted information for interval average.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_avr_hr_keys
    result = validate_avr_hr_keys(indata)
    assert result == expected


@pytest.mark.parametrize("indata, expected", [
    ({"patient_id": "100",
      "heart_rate_average_since": "2019-11-11 11:00:00.00"},
     "2019-11-11 11:00:00.00"),
    ({"patient_id": "100",
      "heart_rate_average_since": "2020-11-11 11:00:00"}, False),
    ({"patient_id": "100",
      "heart_rate_average_since": 2019}, False)
])
def test_validate_time(indata, expected):
    """Test function validate_time

    Args:
        indata (dict): the posted information for interval average.
        expected (bool or string): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import validate_time
    result = validate_time(indata)
    assert result == expected


@pytest.mark.parametrize("p_id, e_hrs, e_timestamps",
                         [(100, [120, 80],
                          ['2019-11-12 13:05:35.00',
                           '2019-11-12 13:06:35.00'])])
def test_hr_and_t(p_id, e_hrs, e_timestamps):
    """Test function hr_and_t

    Args:
        p_id (int): the patient id.
        e_hrs (int): the expected heart rate
        e_timestamps (string): the expected timestamp

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import hr_and_t, Patient
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")
    hrs, timestamps = hr_and_t(p_id)
    p = Patient.objects.raw({"_id": p_id}).first()
    assert p.heart_rate == hrs
    assert p.timestamp == e_timestamps


@pytest.mark.parametrize("p_id, start_t_str, expected", [
    (100, "2019-11-11 11:00:00.00", 100),
    (100, "2020-11-11 11:00:00.00", False)
])
def test_ave_hr_since(p_id, start_t_str, expected):
    """Test function ave_hr_since

    Args:
        p_id (int): the patient id.
        start_t_str (string): the start time to compute the average.
        expected (bool or int): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from hr_server import ave_hr_since
    hr_ave = ave_hr_since(p_id, start_t_str)
    assert hr_ave == expected
