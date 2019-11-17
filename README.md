# Heart Rate Sentinel Server
[![Build Status](https://travis-ci.com/bme547-fall2019/ecg-analysis-memerye.svg?token=7FEBMaBYsSUBFsqKGuGE&branch=master)](https://travis-ci.com/bme547-fall2019/hr-sentinel-server-memerye)


## Background
[Tachycardia](https://en.wikipedia.org/wiki/Tachycardia), also called tachyarrhythmia, is a heart rate that exceeds the normal resting rate. When the heart beats excessively or rapidly, the heart pumps less efficiently and provides less blood flow to the rest of the body, including the heart itself. The increased heart rate also leads to increased work and oxygen demand by the heart, which can lead to rate related ischemia.
Relative tachycardia involves a greater increase in rate than would be expected in a given illness state.

This project builds a simple centralized heart rate sentinel 
server, which can receive GET and POST requests from mock 
patient heart rate monitors that contain patient heart rate information over time. 
If a patient exhibits a tachycardic heart rate and is detected by the heart rate monitor, an email would be sent out at that time to warn the physician of the situation. The tachycardic calculation is based on age, assuming 
all patients will be one year old or older). The notification e-mail is sent using the free [Sendgrid API](https://sendgrid.com/).


## Environment
python 3


## Server Specifications
Your Flask web service implement the following API routes:
* `POST /api/new_patient` that takes a JSON as follows:
  ```
  {
      "patient_id": "1", # usually this would be the patient MRN
      "attending_email": "dr_user_id@yourdomain.com", 
      "patient_age": 50, # in years
  }
  ```
  The `patient_id` and `patient_age` should be numeric whether it is an integer or a string containing an integer.
  - valid for 5 or "5"
  - not valid for 5.5, "5.5", "5a", etc.
  
  This route is called to register a new patient with your server.  This would
  occur when a heart rate monitor is checked out and attached 
  to a particular patient.  This will allow you to initialize a patient in
  the server and be able to accept future heart rate measurements for this 
  patient.  It will always be called before any heart rate data for the patient
  is sent. If the posted patient id already exists in the database, then the 
  information of "attending_email" and the "patient_age" would be updated while
  other information will be erased.
   
* `POST /api/heart_rate` that takes a JSON as follows:
  ```
  {
      "patient_id": "1", # usually this would be the patient MRN
      "heart_rate": 100
  }
  ```
  The `patient_id` and `heart_rate` should be numeric whether it is an integer or a string containing an integer.
  - valid for 5 or "5"
  - not valid for 5.5, "5.5", "5a", etc.

  This route stores the sent heart rate measurement in the record for the specified patient.  The [current date/time stamp](https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python) 
  of when the POST was received should also be stored with the heart rate
  measurement with the format of `"year-month-day hour:mimute:second.microsecond"`. Based on age and heart rate, we can calculate if it is tachycardic listed below, assuming all patients will be one year old or older.
  - 1–2 years: Tachycardia >151 bpm
  - 3–4 years: Tachycardia >137 bpm
  - 5–7 years: Tachycardia >133 bpm
  - 8–11 years: Tachycardia >130 bpm
  - 12–15 years: Tachycardia >119 bpm
  - 15 years or older – adult: Tachycardia >100 bpm
  
  If the posted heart rate is tachycardic for the specified 
  patient and patient age, an e-mail would be sent to the attending physician. 
  This e-mail includes the patient_id, the tachycardic heart rate, and 
  the date/time stamp of that heart rate. The sample format of the e-mail is provided below.
  ```
  Patient ID: 7
  time: 2019-11-16 16:47:35.387322
  heart rate: 160
  Exhibits tachycardic!
  ```
  
* `GET /api/status/<patient_id>`  
  This route returns a JSON containing the latest heart rate, as an integer, for the
  specified patient, whether this patient is 
  currently tachycardic based on this most recently posted heart rate, and 
  the date/time stamp of this most recent heart rate.  The return JSON looks like:
  ```
  {
      "heart_rate": 100,
      "status":  "tachycardic" | "not tachycardic",
      "timestamp": "2018-03-09 11:00:36.372339"  
  }
  ```
   Note that the `status` key contains either the string `"tachycardic"` or
   `"not tachycardic"`.  The key `timestamp` contains a `datetime` string with the format of `"year-month-day hour:mimute:second.microsecond"`.
 
* `GET /api/heart_rate/<patient_id>`  
  This route returns a list of all the previous 
  heart rate measurements for that patient, as a list of integers.

* `GET /api/heart_rate/average/<patient_id>`  
  This route returns the patient's 
  average heart rate, as an integer, of all measurements that have stored for 
  this patient.
 
* `POST /api/heart_rate/interval_average` that takes a JSON as follows: 
  ```
  {
      "patient_id": "1",
      "heart_rate_average_since": "2018-03-09 11:00:36.372339"
  }
  ```
  The `patient_id` should be numeric whether it is an integer or a string containing an integer.
  - valid for 5 or "5"
  - not valid for 5.5, "5.5", "5a", etc.
  
  The h`eart_rate_average_since` is a datetime string in the format of `"year-month-day hour:mimute:second.microsecond"`.
  This route returns the average, as an integer, of all the heart rates that have been
  posted for the specified patient since the given date/time.  Note that
  the given time stamp could be any time, and not necessarily the time of a 
  previous heart rate.


## Functional Specifications
* Logging  
The server writes to a log file when the following events occur:
  1. A new patient is registered.  The log entry includes the patient ID.
    ```
    INFO:root:* ID 5 has been registered in server
    ```
  2. A heart rate is posted that is tachycardic.  The log entry includes the 
    patient ID, the heart rate, and the attending physician e-mail.
    ```
    WARNING:root:* Sent the email to liangyuxu121@gmail.com.
                   Patient ID: 5
                   Heart rate: 120
    ```

* Status code  
  All of the above routes return an appropriate status code including the reason.  
  For example:
  1. All of the above routes do input data validation, making sure that
  the appropriate keys in JSON inputs exist, and that the data types are
  correct. If the input is incorrect, the error status code of `400` as a bad
  request would be returned.
  2. The routes would return the error status codes of `400` as a bad request if a 
  request asks for a patient that does not exist.

* Mongo Database  
  All of the patient data would be saved in [MongoDB](https://www.mongodb.com/). The patient id is the primary key for each patient, which means that the id is unique in the database.
  ```
  _id: 5
  attending_email: "liangyuxu121@gmail.com"
  patient_age: 50
  heart_rate: Array
    0: 100
    1: 120
    2: 80
  status: Array
    0: "not tachycardic"
    1: "tachycardic"
    2: "not tachycardic"
  timestamp: Array
    0: "2019-11-16 15:27:16.692557"
    1: "2019-11-16 15:27:16.826264"
    2: "2019-11-16 15:27:17.548851"
  ```

* Virtual machine
  - Hostname: vcm-11671.vm.duke.edu
  - port: 5000  
  - The URL for running server is `http://vcm-11671.vm.duke.edu:5000`


## How to use
1. Choose "clone with https" in your repository to your local computer.
2. Open your `Git Bash` and input `git clone` adding with the URL.
3. Create virtual environment by command `python -m venv <venv name>`.
4. Install the required code environment in the `requitements.txt` with the following command: `pip install -r requirements.txt`. Afterwards, be sure to start the service of Sendgrid by command `source ./sendgrid.env`.
5. Ensure the existence of the files named `hr_server.py`, `send_email.py` and `test_hr_server.py`. Another python file is `hr_client.py`, which is used for testing the function of server by making up some patient data.
6. Run the command `pytest -v` in your bash window. It will automatically test the function in `hr_server.py`. If all pass, we are expected to see the following output (just part of it).
    ```
    
    ```
    * You can also change the testing arguments and expected results in the `test_ecg.py` and re-run the pytest command.
7. Run the command `python hr_server.py` in your bash window to start the server. The log for running `hr_server.py` would be created at the current file path.
8. Run the command `python hr_client.py` in your bash window to start the requests from a client. You can also change the data within the functions of `test_<route>` to create your mocked patient data.
9. If you want to create the sphinx documentation, you should run following commands to generate HTML documentation. 
    ```
    cd docs
    sphinx-build -M html . _build
    ```
    * This will create `docs/_build/html` with the default webpage being `index.html`. Or the result of webpage that I ran is in the same path in the repository.

## Reference
+ https://en.wikipedia.org/wiki/Tachycardia
+ https://github.com/dward2/BME547/blob/master/Assignments/heart_rate_sentinel_server_assignment.md
+ https://github.com/dward2/BME547/tree/master/Resources/WebServices
+ https://github.com/dward2/BME547/blob/master/Resources/Databases
