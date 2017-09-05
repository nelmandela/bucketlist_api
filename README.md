 # Bucketlist API
 
 [![Build Status](https://travis-ci.org/nelmandela/restful_api.svg?branch=master)](https://travis-ci.org/nelmandela/restful_api)

[![Coverage Status](https://coveralls.io/repos/github/nelmandela/bucketlist_api/badge.svg?branch=master)](https://coveralls.io/github/nelmandela/bucketlist_api?branch=master)

## What it does;

- This is a bucketlist api that enables users to register and login.After login it allows users to create,get,udpate and delete bucketlists and bucketlist items.

## Installation and Set Up:

- Clone the repo from GitHub:
    - git clone https://github.com/nelmandela/bucketlist_api.git

- Fetch from the develop branch:

  - git fetch origin develop

- Navigate to the root folder:

  - cd bucketlist-api
  
- Install the required packages:

  - pip install -r requirements.txt
  
- Initialize, migrate, and upgrade the database:

  - python manage.py db init
  - python manage.py db migrate
  - python manage.py db upgrade
  
## Launching the Program:

  - Run python run.py. You may use Postman for Google Chrome to test the API.

## API Endpoints:

| URL	| Method | Requires Token |
| --- | :--- | ---: |
| /api/v1/auth/register/ | POST | FALSE
| /api/v1/auth/login/ | POST | FALSE
| /api/v1/bucketlists/ | POST | TRUE
| /api/v1/bucketlists/{id}/	| GET | TRUE
| /api/v1/bucketlists/{id}/items/ | POST | TRUE
| /api/v1/bucketlists/{id}/items/<item_id>/	| PUT,DELETE | TRUE

  
## Testing:

  To run tests locally, run the following command: nosetests

## Built With...

  - Flask
  - Flask-RESTful
  - Flask-SQLAlchemy
