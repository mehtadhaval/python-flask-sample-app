python-flask-sample-app
===================
A sample flask app which provides APIs for sending SMS.

The Stack
-------
 - Python 3.4
 - Flask
 - PostgreSQL
 - Redis
 - Flask-SQLAlchemy, Flask-RESTful, Flask-HTTPAuth, Flask-Redis

Installation
------------
**Prerequisites**

 1. PostgreSQL >= 9.0 - [https://www.postgresql.org/docs/current/static/tutorial-install.html](https://www.postgresql.org/docs/current/static/tutorial-install.html)
 2. Redis >= 2.8 - [https://redis.io/download#installation](https://redis.io/download#installation)
 3. Load datadump in PostgreSQL - `psql -U <username> <db_name> < testdatadump.txt`
 4. Python >= 3.4 - [https://www.python.org/downloads/](https://www.python.org/downloads/)

After all prerequisites are installed, follow these steps : 

 1. Clone this repo - `git clone https://github.com/mehtadhaval/python-flask-sample-app.git`
 2. Change into the directory - `cd python-flask-sample-app`
 3. Create virtualenv - `virtualenv venv --python=/usr/bin/python34`
 4. Activate virtualenv - `source venv/bin/activate`
 5. Install required python libs - `pip install -r requirements.pip`
 6. Update config according to local environment in `config_dev.py`
 7. Start the server - `python run.py`

Running Tests
-------------
This app is bundled with test cases. To run test cases, just execute 

    python tests.py

If all tests pass, it should print following output

    ---------------------------------------------------
    Ran 12 tests in 10.233s
    
    OK

