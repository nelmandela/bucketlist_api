import unittest
import json
from tests.base import Base

class TestUserRegistration(Base):

    def test_register_user(self):
        payload = self.client.post('/auth/register',
                                    data=json.dumps({
                                        "name": "johndoe",
                                        "email": "john@doe.com",
                                        "password": "johndoe"
                                    }),
                                    headers=self.set_headers())
        print("Starting")
        print(payload)
        response = json.loads(payload.data.decode())
        print(response)

        self.assertEquals(response['message'] , 'signup successful')
        self.assertEquals(payload.status_code, 201)



if __name__ == "__main__":
    unittest.main()