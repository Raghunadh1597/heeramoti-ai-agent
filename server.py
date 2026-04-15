from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
import bot
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class IncomingMessage(BaseModel):
    text : str = Field(..., max_length=500)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # This intercepts the crash and sends a polite JSON box back to the website
    return JSONResponse(
        status_code=400,
        content={"response": "I apologize, Could you please shorten your message to 500 Characters?"}
    )

@app.post("/chat")
def get_incoming_msg(message: IncomingMessage):
    bot_answer = bot.get_ai_response("user_id", message.text)
    return {"response": bot_answer}
