# API BOT - README
## Description
API BOT is a RESTful API service built with FastAPI and Python. It provides an interface for interacting with a bot, allowing users to send prompts and receive responses. The bot also has the capability to pull models based on user input.  
Features
Message Input Model: A Pydantic model that defines the structure of the user's input, which is a prompt in the form of a string.  
CORS Middleware: The application is configured with Cross-Origin Resource Sharing (CORS) middleware to handle requests from different origins.  
Endpoints:  
GET /: A simple endpoint that returns a greeting message.
POST /message/: An endpoint that accepts a prompt from the user and returns a response from the bot.
POST /model/: An endpoint that pulls a model based on the user's input.
Setup and Installation
Clone the repository to your local machine.
Navigate to the project directory.
Install the required dependencies using pip:
pip install -r requirements.txt
Run the server:
python main.py
The server will start running at http://127.0.0.1:5001/.
Usage
Detailed API documentation is available at http://127.0.0.1:5001/docs.  
Contributing
We welcome contributions! Please see our contributing guidelines for more details.  
License
This project is licensed under the terms of the MIT license.