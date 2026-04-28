from fastapi import routing,HTTPException,Depends,Header,Form
from .schemas.db_models import User
from .schemas.database import db_dependency
from .schemas.pydant import TokenPydant
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_,and_
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from .schemas.settings import SETTINGS
from .schemas.mail import send_mail_message
from pathlib import Path

AUTHroute = routing.APIRouter(
    prefix="/auth",
    tags=["auth"]
)

MAIL_TEMPLATES_DIR = Path(__file__).resolve().parent/"templates"/"mail" 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
cryptoContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_regiser_token(user_id:int):
    to_encode = {
        "user_id":user_id,
        "exp":datetime.utcnow() + timedelta(minutes = SETTINGS.REGISTER_TOKEN_EXPIRES_MINUTES)
    }

    register_token = jwt.encode(to_encode,SETTINGS.SECRET_KEY,SETTINGS.ALGORITHM)

    return register_token

async def send_account_verify_mail(user_mail:str,register_token:str):
    template_body = {
        "verification_link":f"{SETTINGS.APP_URL}/auth/authenticate_user?token={register_token}"
    }
    try:
        await send_mail_message([user_mail],
                                "Verify your account",
                                template_body,
                                "register")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    
async def decode_register_token(token:str):
    try:
        payload = jwt.decode(token,SETTINGS.SECRET_KEY,SETTINGS.ALGORITHM)
        
        return payload["user_id"]
    except JWTError:
        raise HTTPException(401,"Register Token could not be verified")

# @AUTHroute.post("/testing_mail")
# async def send_test_mail(email:str):
#     await send_account_verify_mail(email,"x")
#     return {"success"}

@AUTHroute.post("/register")
async def register(db:db_dependency,email:str = Form(...),credentials:OAuth2PasswordRequestForm = Depends()):
    if db.query(User.id).filter(or_(User.username == credentials.username,User.email == email)).first() or "@" in credentials.username:
        raise HTTPException(409,"user already exists")
    
    #user_data:UserPydant = UserPydant(username=user_data.username,password=user_data.password)
    credentials.password = cryptoContext.hash(credentials.password)
    new_user = User(username = credentials.username,
                    password = credentials.password,
                    email = email)

    db.add(new_user)
    db.commit()

    register_token = generate_regiser_token(new_user.id)
    await send_account_verify_mail(email,register_token)

    return {"detail":"e-mail sent successfully","expires_in":SETTINGS.REGISTER_TOKEN_EXPIRES_MINUTES}

@AUTHroute.get("/authenticate_user")
async def authenticate_user_via_mail(token:str,db:db_dependency):
    user_id = await decode_register_token(token)

    user = (db.query(User)
            .filter(and_(
                User.id == user_id,
                User.account_activated == False))
                .first())
    
    user.account_activated = True
    db.commit()
    db.refresh(user)

    return {"detail":"user account successfully activated"}

@AUTHroute.put("/change_email")
async def update_mail(newMail:str,db:db_dependency,token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SETTINGS.SECRET_KEY,SETTINGS.ALGORITHM)
        user_id:int = payload["id"]
        username:str = payload["sub"]

        if user_id is None or username is None:
            raise HTTPException(401,"cold not validate token")
    
    except JWTError:
        raise HTTPException(401, "cold not validate token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email == newMail
        db.commit()
        db.refresh(user)

    return {"detail":"email address updated successfully"}

@AUTHroute.get("/send_verification_mail")
async def send_verification_mail(db:db_dependency,token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SETTINGS.SECRET_KEY,SETTINGS.ALGORITHM)
        user_id:int = payload["id"]
        username:str = payload["sub"]

        if user_id is None or username is None:
            raise HTTPException(401,"cold not validate token")
    
    except JWTError:
        raise HTTPException(401, "cold not validate token")
    
    userMail = (db.query(User.email)
                .filter(
                    User.id == user_id,
                    User.account_activated == False).first())
    
    if not userMail:
        raise HTTPException(404,"Could not find user with those credentials that have unactive acount")

    register_token = register_token
    await send_account_verify_mail(userMail,register_token)

    return {"detial":"mail sent successfully"}

async def generate_access_token(username:str,user_id:int):
    to_encode = {
        "sub":username,
        "id":user_id,
        "exp":datetime.utcnow() + timedelta(minutes = SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    access_token = jwt.encode(to_encode,SETTINGS.SECRET_KEY,SETTINGS.ALGORITHM)

    return access_token

async def generate_refresh_token(username:str,id:int):
    to_encode = {
        "sub":username,
        "id":id,
        "scope":"refresh",
        "exp":datetime.utcnow() + timedelta(days = SETTINGS.REFRESH_TOKEN_EXPIRES_DAYS) 
    }

    refresh_token = jwt.encode(to_encode,SETTINGS.SECRET_KEY)

    return refresh_token

async def authenticate_user_credentials(password:str,db:Session,username:str):
    user = db.query(User).filter(
            or_(User.username == username,
                User.email == username)
        ).first()
    
    if not user:
        raise HTTPException(404,"User do not exist")
    if not cryptoContext.verify(password,user.password):
        raise HTTPException(401,"Credential incorrect")
    if not user.account_activated:
        raise HTTPException(401,"You need to first activate your account")
    
    username = user.username
    
    return user.id,username

@AUTHroute.post("/login", response_model=TokenPydant)
async def login(db:db_dependency,credentials:OAuth2PasswordRequestForm = Depends()):
    user_id,username = await authenticate_user_credentials(credentials.password,db,credentials.username)
    access_token = await generate_access_token(username,user_id)
    refresh_token = await generate_refresh_token(username,user_id)

    return TokenPydant(
        accessToken = access_token,
        refreshToken = refresh_token,
        tokenType = "barear"
    )    

@AUTHroute.post("/acces_token_refresh")
async def refresh_access_token(refresh_token:str = Header(..., alias="X-Refresh-Token")):
    try:
        payload = jwt.decode(refresh_token,SETTINGS.SECRET_KEY)
        user_id:int = payload["id"]
        username:str = payload["sub"]
        scope:str = payload["scope"]

        if user_id is None or username is None or scope != "refresh":
            raise HTTPException(401,"could not validate refresh token")
        
        access_token = await generate_access_token(username,user_id)

        return TokenPydant(
            accessToken= access_token,
            refreshToken= "",
            tokenType = "barear"
        )
    except JWTError:
        raise HTTPException(401,"could not validate refresh token")

async def decode_acces_token1(db:db_dependency,token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SETTINGS.SECRET_KEY,SETTINGS.ALGORITHM)
        user_id:int = payload["id"]
        username:str = payload["sub"]

        if user_id is None or username is None:
            raise HTTPException(401,"cold not validate token")
        
        isUserAccountActivated = db.query(
            db.query(User.id)
            .filter(and_(User.id == user_id,
                         User.account_activated == True))
            .exists()
        )

        if not isUserAccountActivated:
            raise HTTPException(400,"Account is not verified")
        
        return {"id":user_id,"username":username}
    
    except JWTError:
        raise HTTPException(401, "cold not validate token")
    
decode_acces_token = Annotated[dict,Depends(decode_acces_token1)]

@AUTHroute.get("/token_auth")
async def decode_token_endpoint(user_data:decode_acces_token,db:db_dependency):
    user_id = user_data["id"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404,"user could not be found")
    return {"detail":"ok"}