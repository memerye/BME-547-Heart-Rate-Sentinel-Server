# test_hr_server.py
import pytest
from testfixtures import LogCapture
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
    from hr_server import validate_patient_email
    result = validate_patient_email(patient_info)
    assert result == expected


@pytest.mark.parametrize("patient_info, expected", [
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50}, 50),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "50"}, 50),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "nan"}, False),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "35.5"}, False),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "a50"}, False)
])
def test_validate_patient_age(patient_info, expected):
    from hr_server import validate_patient_age
    result = validate_patient_age(patient_info)
    assert result == expected


@pytest.mark.parametrize("patient_info", [
    ({"patient_id": "100",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": 50})
])
def test_add_new_patient_to_db(patient_info):
    from hr_server import add_new_patient_to_db, Patient
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")
    add_new_patient_to_db(patient_info)
    p = Patient.objects.raw({"_id": int(patient_info["patient_id"])}).first()
    assert p.patient_id == int(patient_info["patient_id"])
    assert p.attending_email == patient_info["attending_email"]
    assert p.patient_age == int(patient_info["patient_age"])


@pytest.mark.parametrize("patient_hr, expected", [
    ({"patient_id": "1",
      "heart_rate": 100}, True),
    ({"patientid": "1",
      "heart_rate": 100}, False),
    ({"patient_id": "1",
      "heart_rat": 100}, False)
])
def test_validate_hr_keys(patient_hr, expected):
    from hr_server import validate_hr_keys
    result = validate_hr_keys(patient_hr)
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
    from hr_server import validate_hr
    result = validate_hr(patient_hr)
    assert result == expected
