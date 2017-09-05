import unittest
import json
from tests.base import Base


class TestBuckelistItems(Base):
    def test_create_bucketlist_item(self):
        """Test bucketlist item POST request"""
        self.client.post('/buckelists',data=json.dumps({"bucketlist_item": "fears"}),headers=self.set_headers())
        response = self.client.post('bucketlists/1/items', data=json.dumps({"bucketlist_item": "conquer fear for spiders"}), headers=self.set_headers())
        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"], "bucketlist item created")
        self.assertEquals(response.status_code, 201)

    def test_gets_all_bucketlist_items(self):
        self.client.post('/bucketlists/1/items',
                         data=json.dumps({"bucketlist_item": "sky diving"}),
                         headers=self.set_headers())
        response = self.client.get('/bucketlists/1/items',
                                   headers=self.set_headers())
        payload = json.loads(response.data.decode())
        self.assertEquals(len(payload["bucketlist_items"]), 1)
        self.assertEquals(response.status_code, 200)


    # def test_get_unavailable_bucketlist_item(self):
    #     """Test unavailable GET request"""
    #     self.client.post('/bucketlist/1/items',data=json.dumps(self.item), headers=self.set_header())
    #     rv = self.client.get('/bucketlist/1/items',headers=self.set_header())
    #     self.assertEqual(json.loads(rv.data.decode()), {'message': 'Bucketlist item not found'})
    #     self.assertEqual(rv.status_code, 404)
    #     self.assertTrue(rv['message'] == 'bucketlist item not found')

    # def test_update_bucketlist_item(self):
    #     """Test bucketlist PUT request"""
    #     rv = self.client().post('/bucketlists/<id>/items',data={'bucketlist_item_id': 'travel'})
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.client().put('/bucketlists/1/items',data={"bucketlist_item_id": "explore"})
    #     self.assertEqual(rv.status_code, 200)
    #     results = self.client().get('/bucketlists/1/items')
    #     self.assertIn('explore', str(rv.data))
    #     self.assertTrue(rv['message'] == 'bucketlist item updated')

    # def test_delete_bucketlist_item(self):
    #     """Test bucketlist DELETE request"""
    #     rv = self.client().post('/bucketlists/<id>/items',data={'bucketlist_item_id': 'visit cayman islands'})
    #     self.assertEqual(rv.status_code, 201)
    #     response = self.client().delete('/bucketlists/<id>/items')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response['message'] == 'bucketlist item deleted')

    # response = self.client().get('/bucketlists/<id>/items')
    # self.assertEqual(response.status_code, 404)
    # self.assertTrue(response['message'] == 'bucketlist item not found')


if __name__ == "__main__":
    unittest.main()