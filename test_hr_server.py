# test_hr_server.py
import pytest
from testfixtures import LogCapture
from pymodm import connect
from datetime import datetime


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
      "patient_age": "50.5"}, 50.5),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "nan"}, False),
    ({"patient_id": "1",
      "attending_email": "dr_user_id@yourdomain.com",
      "patient_age": "a50"}, False)
])
def test_validate_patient_age(patient_info, expected):
    from hr_server import validate_patient_age
    result = validate_patient_age(patient_info)
    assert result == expected


@pytest.mark.parametrize("p_info, e_id, e_email, e_age", [
    ({"patient_id": "100",
      "attending_email": "100@yourdomain.com",
      "patient_age": 50}, 100, "100@yourdomain.com", 50)])
def test_add_new_patient_to_db(p_info, e_id, e_email, e_age):
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


@pytest.mark.parametrize("p_id, e_age", [(100, 50)])
def test_get_age(p_id, e_age):
    from hr_server import get_age, Patient
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")
    get_age(p_id)
    p = Patient.objects.raw({"_id": p_id}).first()
    assert p.patient_age == e_age


@pytest.mark.parametrize("hr_info, e_id, e_hr, e_status", [
    ({"patient_id": "100", "heart_rate": 120, "status": "tachycardic"},
     100, [120], ["tachycardic"]),
    ({"patient_id": "100", "heart_rate": 80, "status": "not tachycardic"},
     100, [120, 80], ["tachycardic", "not tachycardic"])
])
def test_add_hr_to_db(hr_info, e_id, e_hr, e_status):
    from hr_server import add_hr_to_db, Patient
    connect("mongodb+srv://python-code:xly760022@bme547-plgi0."
            "mongodb.net/test?retryWrites=true&w=majority")
    add_hr_to_db(hr_info)
    p = Patient.objects.raw({"_id": int(hr_info["patient_id"])}).first()
    assert p.patient_id == e_id
    assert p.heart_rate == e_hr
    assert p.status == e_status


@pytest.mark.parametrize("age, hr, expected", [
    (1/365, 150, "not tachycardic"),
    (1/365, 160, "tachycardic"),
    (4/365, 160, "not tachycardic"),
    (4/365, 170, "tachycardic"),
    (10/365, 180, "not tachycardic"),
    (10/365, 190, "tachycardic"),
    (50/365, 170, "not tachycardic"),
    (50/365, 180, "tachycardic"),
    (100/365, 180, "not tachycardic"),
    (100/365, 190, "tachycardic"),
    (200/365, 160, "not tachycardic"),
    (200/365, 170, "tachycardic"),
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
def test_validate_hr(age, hr, expected):
    from hr_server import is_tachycardia
    result = is_tachycardia(age, hr)
    assert result == expected
