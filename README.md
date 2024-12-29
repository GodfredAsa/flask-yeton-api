# flask-yeton-api
### TECHNOLOGIES USES
Python
- Flask
- SQLite for Data Storage
- bcrypt
- JWT for security ensurance.
### CHALLENGES FACED
One major faced during the development of the service is the updating of a phone number. This is the case where I ensured that the number to be updated exists and the replacement number should be someone else's number. This is to ensure that unique of all numbers stored in the system.
WHAT AM PROUD OF
I am proud of being able to implement the updating of a number and also writing tests to cover this functionality.

### INSTALLATION GUIDE
Clone the project git clone _project url_
cd into the project root directory
create a virtual environment using python -m venv <virtual_name> where <virtual_name> is your env name eg. If ussd-env is your venv name, then copy, paste and run python3 -m venv ussd-env
Activate virtual environment `source <virtual_name>/bin/activate`. But you used ussd-env as your env then use this `source <virtual_name>/bin/activate` in your terminal far left of the console will appear as (ussd-env) which means env is activated where the word in the parenthesis is your environment name
Installing dependencies from the requirements.txt. Copy, paste and run this `pip install -r requirements.txt`
Running the server python app.py or python3 app.py depending on which version of python installed or if have multiple python versions on your computer, you should see  Running on http://127.0.0.1:5003 Press CTRL+C  to quit
Congratulations you have started server. If you have issues and need assistance contact me asap on LinkedIn
`docker build -t yeton-api .`
`docker run -p 88:5001 --name yetona-api-container yeton-api`
