from django.test import TestCase
from game.models import *
from django.urls import reverse
from datetime import date
import requests
from decouple import config

# Create your tests here.
class GameTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User(username='annacarter', email='anna@surrey.ac.uk') 
        user1.set_password('ecogames')
        user1.save()
        user2 = User(username='testadminuser', email='testadminuser@surrey.ac.uk') 
        user2.set_password('MyPassword123')
        user2.save()
        user3 = User(username='testuser', email='testuser@surrey.ac.uk') 
        user2.set_password('MyPassword123')
        user3.save()
        r=Riddles(id=1,text="What animal can jump higher than a house?")
        r.save()

        challen=Challenger(user=user1, score=10, postcode="GU13")
        challen.save()

                # Seed Categories
        c1=Category(name="Kitchen")
        c1.save()
        c2=Category(name="Bathroom")
        c2.save()
        c3=Category(name="Rooms")
        c3.save()
        c4=Category(name="Electronics")
        c4.save()
        c5=Category(name="Washing")
        c5.save()
        c6=Category(name="Heating")
        c6.save()

        #seed activities
        # Kitchen
        n = Activity(title="Use lids on pots and pans while cooking", points=10, cat=c1)
        n.save()
        n = Activity(title="Use a microwave or toaster oven instead of a regular oven", points=10, cat=c1)
        n.save()
        n = Activity(title="Composte food waste instead of throwing it away", points=10, cat=c1)
        n.save()        
        n = Activity(title="Use a reusable water bottle instead of disposable plastic bottles", points=10, cat=c1)
        n.save()
        n = Activity(title="Use a hybrid or electric vehicle", points=10, cat=c1)
        n.save()
        n = Activity(title="Use a ceiling fan to cool home instead of air conditioning", points=10, cat=c1)
        n.save()
        
        
        # Bathroom
        n = Activity(title="Take a shorter shower", points=10, cat=c2, type=Activity.ActivityType.TIMEREQUIRED)
        n.save()        
        n = Activity(title="Use a low-flow showerhead", points=10, cat=c2, type=Activity.ActivityType.TIMENOTREQUIRED)
        n.save()
        n = Activity(title="Fix leaky faucets and toilets promptly", points=10, cat=c2)
        n.save()
        n = Activity(title="Turn off the water when brushing teeth or shaving", points=10, cat=c2)
        n.save()
        n = Activity(title="Use a water-saving toilet", points=10, cat=c2)
        n.save()
        n = Activity(title="Use natural cleaning products instead of harsh chemicals", points=10, cat=c2)

        # Room
        n = Activity(title="Close curtains and blinds to keep heat out in the summer and retain heat in the winter", points=10, cat=c3)
        n.save()
        n = Activity(title="Use LED light bulbs instead of incandescent bulbs", points=10, cat=c3)
        n.save()
        n = Activity(title="Turn off lights when leaving a room", points=10, cat=c3)
        n.save()
        n = Activity(title="Clean filters in heating and cooling systems", points=10, cat=c3)
        n.save()
        n = Activity(title="Seal gaps and cracks in doors and windows to prevent air leaks", points=10, cat=c3)
        n.save()
        n = Activity(title="Use weather stripping around doors and windows", points=10, cat=c3)
        n.save()
        n = Activity(title="Use natural light instead of electric lighting during the day", points=10, cat=c3)
        n.save()

        # Electronics
        n = Activity(title="Unplug electronics when not in use", points=10, cat=c4)
        n.save()
        n = Activity(title="Use a power strip to turn off electronics when not in use", points=10, cat=c4)
        n.save()
        n = Activity(title="Use the energy-saving mode on appliances like washing machines and dishwashers", points=10, cat=c4)
        n.save()
        n = Activity(title="Use rechargeable batteries", points=10, cat=c4)
        n.save()
        n = Activity(title="Use a laptop instead of a desktop computer", points=10, cat=c4)
        n.save()
        n = Activity(title="Use a fan instead of air conditioning on mild days", points=10, cat=c4)
        n.save()
        n = Activity(title="Use a power-saving mode on your computer or other devices", points=10, cat=c4)
        n.save()

        # Washing
        n = Activity(title="Air-dry clothes instead of using a dryer", points=10, cat=c5)
        n.save()
        n = Activity(title="Clean the lint filter in the dryer", points=10, cat=c5)
        n.save()
        n = Activity(title="Wash laundry in cold water", points=10, cat=c5)
        n.save()

        # Heating
        n = Activity(title="Turn down the thermostat", points=10, cat=c6)
        n.save()
        n = Activity(title="Replace inefficient boiler", points=10, cat=c6)
        n.save()
        n = Activity(title="Tackle draughty spots", points=10, cat=c6)
        n.save()
        n = Activity(title="Lower water temperature", points=10, cat=c6)
        n.save()
        n = Activity(title="Set boiler timer so hot water is not heated all day", points=10, cat=c6)
        n.save()

#----------- Login and Log out Views -----------#

## Test - Login user
    def test_login(self):
        login = self.client.login(username='annacarter', password='ecogames')
        data = {
            'username': 'annacarter',
            'password': 'ecogames',
        } 
        response=self.client.post(reverse('login'), data=data, follow=True)
        # Login successful
        self.assertTrue(login)
        # Correct view returned, user directed to page only visible if logged in
        self.assertContains(response, '<h1 class="display-5 fw-bold">Your Profile</h1>\n<h5>All about you!</h5>', status_code=200)

## Test - Log out
    def test_logout(self):
        self.client.login(username='annacarter', password='ecogames') 
        log_out = self.client.logout
        response=self.client.get(reverse('logout'), follow=True)
        # Logout successful
        self.assertTrue(log_out)
        # Correct view returned, user directed to homepage logged out
        self.assertContains(response, '<li><a class="dropdown-item" href="/accounts/login/">Login</a></li>', status_code=200)

# Test - Attempt login with incorrect uername
    def test_incorrect_login_username(self):
        login=self.client.login(username='anacarter', password='ecogames') 
        data={
            'username': 'anacarter',
            'password': 'ecogames',
        }
        response=self.client.post(reverse('login'), data=data,follow=True)
        # Login failed
        self.assertFalse(login)
        # Correct view returned for incorrect password
        self.assertContains(response, "<li>Please enter a correct username and password. Note that both fields may be case-sensitive.</li>",status_code=200)

# Test - Attempt login with incorrect password
    def test_incorrect_login_password(self):
        login=self.client.login(username='annacarter', password='ecgames') 
        data={
            'username': 'annacarter',
            'password': 'ecgames',
        }
        response=self.client.post(reverse('login'), data=data,follow=True)
        # Login failed
        self.assertFalse(login)
        # Correct view returned for incorrect username
        self.assertContains(response, "<li>Please enter a correct username and password. Note that both fields may be case-sensitive.</li>",status_code=200)


#----------- Test Logging Activities -----------#

    def test_ajax_log_activity_time(self):
        login=self.client.login(username='annacarter', password='ecogames') 
        # Create an instance of the Django test client
        client = self.client

        challen=Challenger.objects.get(pk=1)
        u_cart=UserCart(challenger=challen)
        u_cart.save()
        timeRecorded="19:08"
        act=Activity.objects.get(pk=1)
        act_id=getattr(act,'id')
        lineItem=LineItem(timeRecorded=timeRecorded, dateRecorded=date.today(), activity=act, cart=u_cart)
        print(lineItem)
        # event publish set to false
        data = {
            'time': timeRecorded,
            'duration':0,
            'activityId':act_id
        }
        response = self.client.post(reverse('gameapp:add_time'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        self.assertContains(response, '<h5 name="1" class="line-item card-title">Use lids on pots', status_code=200)


    def test_ajax_submit_activity(self):
        login=self.client.login(username='annacarter', password='ecogames') 
        # Create an instance of the Django test client
        client = self.client

        challen=Challenger.objects.get(pk=1)
        u_cart=UserCart(challenger=challen)
        u_cart.save()
        timeRecorded="19:08"
        act=Activity.objects.get(pk=1)
        act_id=getattr(act,'id')
        lineItem=LineItem(timeRecorded=timeRecorded, dateRecorded=date.today(), activity=act, cart=u_cart)
        lineItem.save()
        listitems=lineItem
        # event publish set to false
        data = {
            'list_items[]': '1'
        }
        response = self.client.post(reverse('gameapp:record_points'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        data =response.json()
        self.assertEquals(data['message'], "Elements received and processed successfully.")

    #----------- Carbon Intensity API -----------#

    # def test_carbon_intensity(self, requests_mock):
    #     headers = {
    #         'Accept': 'application/json'
    #     }
    #     postcode = "GU13"
    #     formatted_from_datetime = "2023-05-18T19:08Z"
    #     formatted_to_datetime = "2023-05-18T19:38Z"
                    
    #     requests_mock.get(
    #         f'https://api.carbonintensity.org.uk/regional/intensity/{formatted_from_datetime}/{formatted_to_datetime}/postcode/{postcode}',
    #         json={'data': 'Mocked response data'},
    #         headers=headers
    #     )

    #     response = requests.get(
    #         f'https://api.carbonintensity.org.uk/regional/intensity/{formatted_from_datetime}/{formatted_to_datetime}/postcode/{postcode}',
    #         params={},
    #         headers=headers
    #     )

    #     assert 'index:' == response.json()['data']

    # #----------- Weather API -----------#

    # def test_weather_api(self, requests_mock):
    #     headers = {
    #         'Accept': 'application/json'
    #     }
    #     location = "GU13"
    #     WEATHER_KEY=config('WEATHER_KEY')            
    #     requests_mock.get(f"https://api.openweathermap.org/data/2.5/weather?zip={location},{'GB'}&appid={WEATHER_KEY}&units=metric")

    #     response = requests.get(
    #         f"https://api.openweathermap.org/data/2.5/weather?zip={location},{'GB'}&appid={WEATHER_KEY}&units=metric",
    #         params={},
    #         headers=headers
    #     )

    #     assert 'temperature:' == response.json()['data']

    # #----------- Datawrapper API -----------#

    # def test_datawrapper(self, requests_mock):

    #     DATA_KEY = config('DATA_KEY') # Get API key

    #     url = f"https://api.datawrapper.de/v3/charts"

    #     data = {
    #         "title": "The Eco Games", 
    #         "type": "d3-maps-choropleth"
    #             }
        
    #     headers = {
    #         "Authorization": f"Bearer {DATA_KEY}",
    #         "accept": "*/*",
    #         "content-type": "application/json"
    #     }          
    #     requests_mock.post(url, json=data, headers=headers)

    #     response = requests.post(url, json=data, headers=headers)

    #     assert 'publicId:' == response.json()['publicId']