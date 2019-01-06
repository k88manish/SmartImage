# To install python packages. Please run

pip install -r requirements.txt

## Run Server

Move to Video-Analyser folder by following command

cd Video-Analyser

# For Linux and Mac:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

# For Windows cmd, use set instead of export:

set FLASK_APP=flaskr
set FLASK_ENV=development
flask run

## Upload video

Go to url on which server is running on http://localhost:5000/upload
