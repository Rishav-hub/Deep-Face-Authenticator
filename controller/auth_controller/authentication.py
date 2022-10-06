import os
import uuid
from pymongo.common import validate_type_registry
from starlette.responses import JSONResponse
from fastapi import HTTPException, status, APIRouter\
    , Request, Response
from pydantic import BaseModel
from typing import List, Optional
# from passlib.context import CryptContext
from datetime import datetime 
from datetime import timedelta
from jose import jwt, JWTError
from dotenv import dotenv_values

from face_auth.exception import AppException
from face_auth.entity.user import User
from face_auth.business_val.user_val import RegisterValidation, LoginValidation

# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Login(BaseModel):
    """_summary_
    """
    email_id: str
    password: str

class Register(BaseModel):
    """
    _summary_
    """
    Name: str
    username: str
    email_id: str
    ph_no: int
    password1: str
    password2: str


router = APIRouter(prefix="/auth", tags=["auth"], responses= {"401": {"description": "Not Authorized!!!"}})


# Calloging the logger for Database read and insert operations

async def get_current_user(request: Request):
    """_summary_

    Args:
        request (Request): _description_

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        if os.environ.get('SECRET_KEY') is None or os.environ.get('ALGORITHM') is None:
            enironment_variable= dotenv_values('.env')
            secret_key = enironment_variable['SECRET_KEY']
            algorithm = enironment_variable['ALGORITHM']
        else:
            secret_key = os.environ.get('SECRET_KEY')
            algorithm = os.environ.get('ALGORITHM')
        token=request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        uuid: str = payload.get("sub")
        username: str = payload.get("username")

        if uuid is None or username is None:
            return logout(request)
        return {"uuid": uuid, "username": username}
    except JWTError:
        raise HTTPException(status_code=404, detail="Detail Not Found")
    except Exception as e:
        msg = "Error while getting current user"
        response = JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": msg})
        return response

def create_access_token(uuid: str, username: str,\
                            expires_delta: Optional[timedelta] = None):
    try:
        
        if os.environ.get('SECRET_KEY') is None and os.environ.get('ALGORITHM') is None:
            enironment_variable= dotenv_values('.env')
            secrete_key = enironment_variable['SECRET_KEY']
            algorithm = enironment_variable['ALGORITHM']
        else:
            secrete_key = os.environ.get('SECRET_KEY')
            algorithm = os.environ.get('ALGORITHM')
        
        print(uuid, username)
        encode = {"sub": uuid, "username": username}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode.update({"exp": expire})
        # return jwt.encode(encode, Configuration().SECRET_KEY, algorithm=Configuration().ALGORITHM)
        return jwt.encode(encode,secrete_key, algorithm=algorithm)
    except Exception as e:
        raise e

@router.post("/token")
async def login_for_access_token(response: Response, login):
    try:
        userValidation = LoginValidation(login.email_id, login.password)
        user = userValidation.authenticateUserLogin()

        if not user:
            return False
        token_expires = timedelta(minutes=15)
        token = create_access_token(user['UUID'],user['username'],\
                                    expires_delta=token_expires)
        print(token)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return True, user['UUID']
    except Exception as e:
        msg = "Failed to set access token"
        response = JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": msg})
        return response

@router.get("/", response_class=JSONResponse)
async def authentication_page(request: Request):
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Authentication Page"})
    except Exception as e:
        raise e

@router.post("/", response_class=JSONResponse)
async def login(request: Request, login: Login):
    try:
        # response = RedirectResponse(url="/application/", status_code=status.HTTP_302_FOUND)
        msg = "Login Successful"
        response = JSONResponse(status_code=status.HTTP_200_OK, content={"message": msg})
        validate_user_cookie,user_uuid = await login_for_access_token(response= response, login=login)
        if not validate_user_cookie:
            msg = "Incorrect Username and password"
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "message": msg})
            # return RedirectResponse(url="/", status_code=status.HTTP_401_UNAUTHORIZED, headers={"msg": msg})
        # msg = "Login Successfull"
        # response = JSONResponse(status_code=status.HTTP_200_OK, content={"message": msg}, headers={"uuid": "abda"})
        response.headers["uuid"] = user_uuid
        return response

    except HTTPException:
        msg = "UnKnown Error"
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "message": msg})
        # return RedirectResponse(url="/", status_code=status.HTTP_401_UNAUTHORIZED, headers={"msg": msg})
    except Exception as e:
        print(e)
        msg = "User NOT Found"
        response = JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "message": msg})
        return response

@router.get("/register", response_class=JSONResponse)
async def authentication_page(request: Request):
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Registration Page"})
    except Exception as e:
        raise e
@router.post("/register", response_class=JSONResponse)
async def register_user(request: Request,register: Register):
    
    """Post request to register a user

    Args:
        request (Request): Request Object
        register (Register):    Name: str
                                username: str
                                email_id: str
                                ph_no: int
                                password1: str
                                password2: str

    Raises:
        e: If the user registration fails

    Returns:
        _type_: Will redirect to the embedding generation route and return the UUID of user
    """
    try:
        name = register.Name
        username = register.username
        password1 = register.password1
        password2 = register.password2
        email_id = register.email_id
        ph_no = register.ph_no

        # Add uuid to the session
        
        # print(request.session["uuid"])
        
        user = User(name, username, email_id, ph_no, password1, password2)
        request.session["uuid"] = user.uuid_

        # Validation of the user input data to check the format of the data
        userValidation = RegisterValidation(user)

        validate_regitration = userValidation.validateRegistration()
        if not validate_regitration["status"]:
            msg = validate_regitration['msg']
            response = JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "message": msg})
            return response
        
        # Save user if the validation is successful
        validation_status = userValidation.saveUser()

        msg = "Registration Successful...Please Login to continue"
        response = JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "message": validation_status['msg']},\
                                headers={"uuid": user.uuid_})
        return response
    except Exception as e:
        raise e

@router.get("/logout")
async def logout(request: Request):
    try:
        msg = "You have been logged out"
        # response =  RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND, headers={"msg": msg})
        response.delete_cookie(key="access_token")
        response = JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "message": msg})
        return response
    except Exception as e:
        raise e