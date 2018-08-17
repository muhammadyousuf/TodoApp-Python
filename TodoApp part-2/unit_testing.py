import unittest
import os
import sys, json
from app import app

class TodoData(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
 
        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass
    
    def test_todo_api(self):
        response = self.app.get('/todoapp/api/v1.0/yousuf')
        self.assertEqual(response.status_code,200 )
    
    def test_delete(self):
        response = self.app.delete('/todoapp/api/v1.0/yousuf/3')
        self.assertEqual(response.status_code,200)
    # def test_edit(self):
    #     response = self.app.put('/todoapp/api/v1.0/yousuf/5')
    #     self.assertEqual(response.status_code,200 )
    def test_todoList(self):
        response = self.app.get('/todoapp/api/v1.0/yousuf/3')
        self.assertEqual(response.status_code,200 )

if __name__ == "__main__":
    unittest.main() 
