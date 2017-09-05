import os
import unittest
import json
from app import create_app, db

class Base(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.user = json.dumps({
            "name": "nel",
            "email": "test@test.com",
            "password": "password"
        })

        print("creating")
        db.create_all()

    def set_headers(self):
        """ Set headers for Authorization and Content Type. """
        self.client.post("/auth/register",
                         data=self.user,
                         content_type='application/json')

        response = self.client.post("/auth/login",
                                   data=self.user,
                                   content_type='application/json')
        print(response)
        payload = json.loads(response.data.decode())

        # get the token from the reponse body
        self.token = payload['access_token']

        return dict({
                'access-token': self.token,
                'Content-Type': 'application/json',
               })

    def tearDown(self):
        db.drop_all()
        os.remove('test.db')
            