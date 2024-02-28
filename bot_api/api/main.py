from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bot import bot


class MessageInput(BaseModel):
    prompt: str


app = FastAPI()
origins = [
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# route to test the bot with a prompt with input message from the user pass in the generated response
@app.post("/message/")
def message(input_user: MessageInput):
    try:
        response = bot.generate_response(input_user.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/model/")
def model(input_user: MessageInput):
    try:
        response = bot.pull_model(input_user.prompt)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == '__main__':
    app.run(port=5001, debug=True)
