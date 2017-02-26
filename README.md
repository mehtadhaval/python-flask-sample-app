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

 1. Create virtualenv - `virtualenv venv --python=/usr/bin/python34`
 2. Activate virtualenv - `source venv/bin/activate`
 2. Install required python libs - `pip install -r requirements.pip`
 3. Update config according to local environment in `config_dev.py`
 4. Start the server - `python run.py`

Running Tests
-------------
This app is bundled with test cases. To run test cases, just execute 

    python tests.py

If all test pass, it should print following output

    ---------------------------------------------------
    Ran 12 tests in 10.233s
    OK

