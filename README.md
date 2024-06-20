# The Eco Games Web Application

## Business Need and Environment:
The Eco Games addresses the pressing issues of energy consumption and its environmental impacts. Fossil fuel dominance in energy generation contributes significantly to pollution, global warming, and habitat destruction. Energy security and economic stability are also concerns, necessitating sustainable energy solutions.

## Project Objectives:

Promote sustainable energy usage by encouraging users to shift consumption to off-peak hours.
Foster competition among UK locations through a points-based system and leaderboard.
Raise awareness with personalized energy-saving recommendations based on user behavior.

## Take a look at the short presentation below:
- https://www.youtube.com/watch?v=22YjIAaX3aU&si=OMLj4uk9JZgc61h4.

## How to run The Eco Games using Docker
------------------------------

Before you begin:
- Ensure the Docker Engine is running
- Stop any containers currently running on port 8000

To run The Eco Games in a Docker container:

1. In terminal, navigate to the location where the image is stored


2. Enter the following line into the terminal: 

docker load -i theecogames_final.tar 

You should see the message "Loaded image: theecogames:final2"


3. After seeing the message, enter the following line: 

docker run --publish 8000:8000 theecogames:final2


4. Go to localhost:8000 in a browser!
