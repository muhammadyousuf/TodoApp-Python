import unittest
import os
import sys, json
from todo import app

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
    # def test_add(self):
    #     response = self.app.post('/todoapp/api/v1.0/yousuf',
    #                     data=json.dumps(dict(saves='tasks')),
    #                    content_type='application/json')
    #     self.assertEqual(response.status_code,200 )
   
    def test_todoList(self):
        response = self.app.get('/todoapp/api/v1.0/yousuf/todoList')
        self.assertEqual(response.status_code,200 )

if __name__ == "__main__":
    unittest.main() 
