from django.core.management.base import BaseCommand 
from game.models import *

class Command(BaseCommand):

    def handle(self, *args, **options): 

        Activity.objects.all().delete()

        # Seed users

        user1 = User(username='user1', email='user1@surrey.ac.uk') 
        user1.set_password('MyPassword123')
        user1.save()
        challenger1=Challenger(user=user1, score=119, postcode="E1")
        challenger1.save()

        user2 = User(username='user2', email='user2@surrey.ac.uk') 
        user2.set_password('MyPassword123')
        user2.save()
        challenger2=Challenger(user=user2, score=219, postcode="N1")
        challenger2.save()

        user3 = User(username='user3', email='user3@surrey.ac.uk') 
        user2.set_password('MyPassword123')
        user3.save()
        challenger3=Challenger(user=user3, score=989, postcode="N8")
        challenger3.save()

        user4 = User(username='user4', email='user4@surrey.ac.uk') 
        user4.set_password('MyPassword123')
        user4.save()
        challenger4=Challenger(user=user4, score=1121, postcode="ST14")
        challenger4.save()

        user5 = User(username='user5', email='user5@surrey.ac.uk') 
        user5.set_password('MyPassword123')
        user5.save()
        challenger5=Challenger(user=user5, score=1239, postcode="NE12")
        challenger5.save()

        user6 = User(username='user6', email='user6@surrey.ac.uk') 
        user6.set_password('MyPassword123')
        user6.save()
        challenger6=Challenger(user=user6, score=459, postcode="CR3")
        challenger6.save()

        user7 = User(username='user7', email='user7@surrey.ac.uk') 
        user7.set_password('MyPassword123')
        user7.save()
        challenger7=Challenger(user=user7, score=735, postcode="SL6")
        challenger7.save()

        user8 = User(username='user8', email='user8@surrey.ac.uk') 
        user8.set_password('MyPassword123')
        user8.save()
        challenger8=Challenger(user=user8, score=202, postcode="OX4")
        challenger8.save()

        user9 = User(username='user9', email='user9@surrey.ac.uk') 
        user9.set_password('MyPassword123')
        user9.save()
        challenger9=Challenger(user=user9, score=862, postcode="PL11")
        challenger9.save()

        user10 = User(username='user10', email='user10@surrey.ac.uk') 
        user10.set_password('MyPassword123')
        user10.save()
        challenger10=Challenger(user=user1, score=163, postcode="TA8")
        challenger1.save()

        user11 = User(username='user11', email='user11@surrey.ac.uk') 
        user11.set_password('MyPassword123')
        user11.save()
        challenger11=Challenger(user=user11, score=493, postcode="TW4")
        challenger11.save()

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
        n = Activity(title="Used lids on pots and pans while cooking", points=10, cat=c1)
        n.save()
        n = Activity(title="Used a microwave or toaster oven instead of a regular oven", points=10, cat=c1)
        n.save()
        n = Activity(title="Composted food waste instead of throwing it away", points=10, cat=c1)
        n.save()        
        n = Activity(title="Used a reusable water bottle instead of disposable plastic bottles", points=10, cat=c1)
        n.save()
        n = Activity(title="Used a hybrid or electric vehicle", points=10, cat=c1)
        n.save()
        n = Activity(title="Used a ceiling fan to cool home instead of air conditioning", points=10, cat=c1)
        n.save()
        
        
        # Bathroom
        n = Activity(title="Took a shower", points=10, cat=c2, type=Activity.ActivityType.TIMEREQUIRED)
        n.save()        
        n = Activity(title="Used a low-flow showerhead", points=10, cat=c2, type=Activity.ActivityType.TIMENOTREQUIRED)
        n.save()
        n = Activity(title="Fixed leaky faucets and toilets promptly", points=10, cat=c2)
        n.save()
        n = Activity(title="Turned off the water when brushing teeth or shaving", points=10, cat=c2)
        n.save()
        n = Activity(title="Used a water-saving toilet", points=10, cat=c2)
        n.save()
        n = Activity(title="Used natural cleaning products instead of harsh chemicals", points=10, cat=c2)

        # Room
        n = Activity(title="Closed curtains and blinds to keep heat out in the summer and retain heat in the winter", points=10, cat=c3)
        n.save()
        n = Activity(title="Used LED light bulbs instead of incandescent bulbs", points=10, cat=c3)
        n.save()
        n = Activity(title="Turned off lights when leaving a room", points=10, cat=c3)
        n.save()
        n = Activity(title="Cleaned filters in heating and cooling systems", points=10, cat=c3)
        n.save()
        n = Activity(title="Sealed gaps and cracks in doors and windows to prevent air leaks", points=10, cat=c3)
        n.save()
        n = Activity(title="Used weather stripping around doors and windows", points=10, cat=c3)
        n.save()
        n = Activity(title="Used natural light instead of electric lighting during the day", points=10, cat=c3)
        n.save()

        # Electronics
        n = Activity(title="Unplugged electronics when not in use", points=10, cat=c4)
        n.save()
        n = Activity(title="Used a power strip to turn off electronics when not in use", points=10, cat=c4)
        n.save()
        n = Activity(title="Used the energy-saving mode on appliances like washing machines and dishwashers", points=10, cat=c4)
        n.save()
        n = Activity(title="Used rechargeable batteries", points=10, cat=c4)
        n.save()
        n = Activity(title="Used a laptop instead of a desktop computer", points=10, cat=c4)
        n.save()
        n = Activity(title="Used a fan instead of air conditioning on mild days", points=10, cat=c4)
        n.save()
        n = Activity(title="Used a power-saving mode on your computer or other devices", points=10, cat=c4)
        n.save()

        # Washing
        n = Activity(title="Air-dried clothes instead of using a dryer", points=10, cat=c5)
        n.save()
        n = Activity(title="Cleaned the lint filter in the dryer", points=10, cat=c5)
        n.save()

        # Heating
        n = Activity(title="Turned down the thermostat", points=10, cat=c6)
        n.save()


        self.stdout.write('done.')

        Riddles.objects.all().delete()

        # seed riddles

        r=Riddles(text="Welcome to the Eco Games! Every month you will see a new riddle. Here's one to get you started.. I touch your face, I'm in your words, I'm lack of space and beloved by birds")
        r.save()



        # Activities that require a time
        # Showering
        # Washing machine
        

        # Activities that require miles
        # Driving

        # Activities that require degrees
        # Turn down thermostat


# Daily activities (Little points)
        # Have a shower -> input duration
        # Use the microwave instead of oven
        # Hang washing instead of using tumble dryer
        # Wash clothes in cold water instead of hot
        # Turn the heating down -> input degrees
        # Turn TV's onto standby
        # Use full load dishwasher
        # Blocked draughts

        # Switch off standby

        # For meals: use a slow cooker: they use basically the same energy as a light bulb.


# Weekly activities



# One-off energy saving activities (Mega points)
        # Insulate the loft
        # Insulate boiler
        # Add solar panels
        # Change your gas hob to an electric hob
        # Install LED lights
        # Install a Qwokka instead of using a kettle
        # Bleed your radiator


# Reminders
        # Keep tap off whilst brushing teeth
        # Recycle bins
        # Turn off the lights
        # Avoid overfilling kettle
        # Avoid the tumble dryer hang your washing
        # For meals: Microwave a leftover meal instead of using the oven to cook something
        # Used glass/ceramic pans they retain heat better than metal
        # Dont heat empty rooms
        # Close curtains