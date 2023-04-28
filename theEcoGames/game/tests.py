from django.test import TestCase
from game.models import *
from django.urls import reverse

# Create your tests here.
class GameTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User(username='annacarter', email='anna@surrey.ac.uk') 
        user1.set_password('MyPassword123')
        user1.save()
        user2 = User(username='testadminuser', email='testadminuser@surrey.ac.uk') 
        user2.set_password('MyPassword123')
        user2.save()
        user3 = User(username='testuser', email='testuser@surrey.ac.uk') 
        user2.set_password('MyPassword123')
        user3.save()

#----------- Login and Log out Views -----------#

## Test - Login user
    def test_login(self):
        login = self.client.login(username='annacarter', password='MyPassword123')
        data = {
            'username': 'annacarter',
            'password': 'MyPassword123',
        } 
        response=self.client.post(reverse('login'), data=data, follow=True)
        # Login successful
        self.assertTrue(login)
        # Correct view returned, user directed to page only visible if logged in
        self.assertContains(response, '<strong>Your Profile</strong>', status_code=200)

## Test - Log out
    def test_logout(self):
        self.client.login(username='annacarter', password='MyPassword123') 
        log_out = self.client.logout
        response=self.client.get(reverse('logout'), follow=True)
        # Logout successful
        print(response)
        self.assertTrue(log_out)
        # Correct view returned, user directed to homepage logged out
        self.assertContains(response, '<li class="nav-item"> <a class="nav-user" href="/accounts/login/">Login</a> </li>', status_code=200)

# Test - Attempt login with incorrect uername
    def test_incorrect_login_username(self):
        login=self.client.login(username='anacarter', password='MyPassword123') 
        data={
            'username': 'anacarter',
            'password': 'MPassword',
        }
        response=self.client.post(reverse('login'), data=data,follow=True)
        # Login failed
        self.assertFalse(login)
        # Correct view returned for incorrect password
        self.assertContains(response, "<li>Please enter a correct username and password. Note that both fields may be case-sensitive.</li>",status_code=200)

# Test - Attempt login with incorrect password
    def test_incorrect_login_password(self):
        login=self.client.login(username='annacarter', password='MPassword') 
        data={
            'username': 'annacarter',
            'password': 'MPassword',
        }
        response=self.client.post(reverse('login'), data=data,follow=True)
        # Login failed
        self.assertFalse(login)
        # Correct view returned for incorrect username
        self.assertContains(response, "<li>Please enter a correct username and password. Note that both fields may be case-sensitive.</li>",status_code=200)


#----------- Categories Views -----------#

