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
