from bot import bot
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Define the model for the input message
class MessageInput(BaseModel):
    prompt: str


# Initialize the FastAPI application
app = FastAPI()

# Define the list of origins for CORS
origins = [
    "http://localhost:8000",
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the root route
@app.get("/")
def read_root():
    """
    This function returns a simple greeting message.

    Returns:
        dict: A dictionary with a greeting message.
    """
    return {"Hello": "World"}


# Define the route to test the bot with a prompt


@app.post("/message/")
def message(input_user: MessageInput):
    """
    This function generates a response from the bot based on the user's input.

    Args:
        input_user (MessageInput): The user's input.

    Returns:
        dict: A dictionary with the bot's response.

    Raises:
        HTTPException: If there is an error generating the response.
    """
    try:
        response = bot.generate_response(input_user.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Define the route to pull a model
@app.post("/model/")
def model(input_user: MessageInput):
    """
    This function pulls a model based on the user's input.

    Args:
        input_user (MessageInput): The user's input.

    Returns:
        Any: The response from the bot.

    Raises:
        HTTPException: If there is an error pulling the model.
    """
    try:
        response = bot.pull_model(input_user.prompt)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Main function
if __name__ == "__main__":
    """
    This is the main function that runs the FastAPI application.
    """
    app.run(port=5001, debug=True)
