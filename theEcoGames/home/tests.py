from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class HomePageTest(TestCase):
    def setUp(Self):
        return
    
    def test_homepage(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        
def test_contact(self):
    response = self.client.get(reverse('contact'))
    self.assertEqual(response.status_code, 200)
    
    self.assertContains(response, 'This is my header')
    self.assertContains(response, 'This is My Contact Page')
    self.assertContains(response, 'This is my footer')