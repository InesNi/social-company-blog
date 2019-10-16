# social-company-blog

## Tech Stack
- Python 
- Flask
- Bootstrap
- Flask-Sqlalchemy
- Gunicorn


### How to run

1. Create new virtual environment by running `python3 -m venv env`;
2. Activate virtual environment by running `source env/bin/activate`;
3. Install all requirements by running `pip3 install -r requirements.txt`;
4. Run with `flask run` or `gunicorn wsgi:app` while in main directory 