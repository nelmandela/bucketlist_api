import unittest
import json
from tests.base import Base
from app import db

class TestBucketlist(Base):
    def test_bucketlist_creation(self):
        """Test bucketlist POST request"""
        response = self.client.post('/bucketlists', 
                                    data=json.dumps({"bucketlist": "work"}), 
                                    headers=self.set_headers())
        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"], "bucketlist created")
        self.assertEquals(response.status_code, 201)

    def test_gets_all_bucketlists(self):
        self.client.post('/bucketlists',
                         data=json.dumps({"bucketlist": "work"}),
                         headers=self.set_headers())
        response = self.client.get('/bucketlists',
                                   headers=self.set_headers())
        payload = json.loads(response.data.decode())
        self.assertEquals(len(payload["bucketlists"]), 1)
        self.assertEquals(response.status_code, 200)
  
    def test_post_method_is_protected(self):
            # make a request with no token set
            response = self.client.post('/bucketlists', 
                                        data=json.dumps({"bucketlist": "work"}), 
                                        content_type="application/json")
            payload = json.loads(response.data.decode())
            self.assertEquals(payload["message"],
                            "You are not logged in")
            self.assertEquals(response.status_code, 401)



if __name__ == "__main__":
    unittest.main()