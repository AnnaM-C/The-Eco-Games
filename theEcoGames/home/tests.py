from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class HomePageTest(TestCase):
    def setUp(self):
        return
    
    def test_homepage(self):
        response = self.client.get('home')
        self.assertEqual(response.status_code, 200)
        

class ContactPageTest(TestCase):
    def test_contact(self):
        url = reverse('contact')
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@any.com',
            'message': 'Testing message'
            }
        response = self.client.post(url, data=form_data)
    
    
