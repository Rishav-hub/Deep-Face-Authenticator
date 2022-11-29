import os
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi import HTTPException, status, APIRouter, Request, Response
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from datetime import timedelta
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from face_auth.entity.user import User
from face_auth.business_val.user_val import RegisterValidation, LoginValidation
from face_auth.constant.auth_constant import SECRET_KEY, ALGORITHM


templates = Jinja2Templates(directory= os.path.join(os.getcwd(), "templates"))

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.email_id: Optional[str] = None
        self.password: Optional[str] = None
    
    async def create_oauth_form(self):
        form = await self.request.form()
        self.email_id = form.get("email")
        self.password = form.get("password")

class RegisterForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.name: Optional[str] = None
        self.username: Optional[str] = None
        self.email_id: Optional[str] = None
        self.ph_no: Optional[int] = None
        self.password1: Optional[str] = None
        self.password2: Optional[str] = None
        
    async def create_oauth_form(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.username = form.get("username")
        self.email_id = form.get("email")
        self.ph_no = form.get("ph_no")
        self.password1 = form.get("password1")
        self.password2 = form.get("password2")


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={"401": {"description": "Not Authorized!!!"}},
)


# Calloging the logger for Database read and insert operations


async def get_current_user(request: Request):
    """This function is used to get the current user

    Args:
        request (Request): Request from the route

    Returns:
        dict: Returns the username and uuid of the user
    """
    try:
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        token = request.cookies.get("access_token")
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
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return response


def create_access_token(
    uuid: str, username: str, expires_delta: Optional[timedelta] = None
) -> str:
    """This function is used to create the access token

    Args:
        uuid (str): uuid of the user
        username (str): username of the user

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """

    try:
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        encode = {"sub": uuid, "username": username}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode.update({"exp": expire})
        # return jwt.encode(encode, Configuration().SECRET_KEY, algorithm=Configuration().ALGORITHM)
        return jwt.encode(encode, secret_key, algorithm=algorithm)
    except Exception as e:
        raise e


@router.post("/token")
async def login_for_access_token(response: Response, login) -> dict:
    """_summary_

    Args:
        response (Response): _description_
        login (_type_): _description_

    Returns:
        dict: _description_
    """

    try:
        userValidation = LoginValidation(login['email_id'], login['password'])
        user: Optional[str] = userValidation.authenticateUserLogin()
        if not user:
            return {"status": False, "uuid": None, "response": response}
        token_expires = timedelta(minutes=15)
        token = create_access_token(
            user["UUID"], user["username"], expires_delta=token_expires
        )
        response.set_cookie(key="access_token", value=token, httponly=True)
        return {"status": True, "uuid": user["UUID"], "response": response}
    except Exception as e:
        msg = "Failed to set access token"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return {"status": False, "uuid": None, "response": response}


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    """_summary_

    Args:
        request (Request): _description_

    Raises:
        e: Exception

    Returns:
        Response: _description_
    """
    try:
        return templates.TemplateResponse("login.html", 
        context={"request":request,"msg":"login_page","status_code":status.HTTP_200_OK})
    except Exception as e:
        raise e


@router.post("/", response_class=HTMLResponse)
async def login(request: Request):
    """_summary_

    Args:
        request (Request): _description_
        login (Login): _description_

    Returns:
        _type_: _description_
    """
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        login = {
            "email_id": form.email_id,
            "password": form.password
        }

        msg = "Login Successful"
        response = RedirectResponse(url="/application/", status_code=status.HTTP_302_FOUND)

        token_response = await login_for_access_token(response=response, login=login)

        if not token_response["status"]:
            msg = "Incorrect Username and password"
            return templates.TemplateResponse("login.html", 
            context={"request": request, "msg": msg,"status_code":status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_401_UNAUTHORIZED,
            )
       
        response.headers["uuid"] = token_response["uuid"]

        return response

    except HTTPException:
        msg = "UnKnown Error"
        return templates.TemplateResponse("login.html",
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"request":request ,"status": False, "message": msg},
        )
    except Exception as e:
        msg = "User NOT Found"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": msg},
        )
        return response


@router.get("/register", response_class=HTMLResponse)
async def authentication_page(request: Request):
    """_summary_

    Args:
        request (Request): _description_

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """
    try:
        return templates.TemplateResponse("login.html",
            status_code=status.HTTP_200_OK, 
            context={"request": request,"message": "Registration Page"}
        )
    except Exception as e:
        raise e


@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request):

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
        register = RegisterForm(request)
        await register.create_oauth_form()

        name = register.name
        username = register.username
        password1 = register.password1
        password2 = register.password2
        email_id = register.email_id
        ph_no = register.ph_no

        # Add uuid to the session
        user = User(name, username, email_id, ph_no, password1, password2)
        request.session["uuid"] = user.uuid_

        # Validation of the user input data to check the format of the data
        userValidation = RegisterValidation(user)

        validate_regitration = userValidation.validateRegistration()

        if not validate_regitration["status"]:
            msg = validate_regitration["msg"]
            response = templates.TemplateResponse("login.html",
            status_code=status.HTTP_401_UNAUTHORIZED,
            context={"request": request,"msg":msg,"status_code":status.HTTP_404_NOT_FOUND}
            )
            return response

        # Save user if the validation is successful
        validation_status = userValidation.saveUser()

        msg = "Registration Successful...Please Login to continue"
        response = RedirectResponse(url="/application/register_embedding",
         status_code=status.HTTP_302_FOUND,
         headers={"uuid": user.uuid_})
        return response
        
        
    except Exception as e:
        response = templates.TemplateResponse("error.html",
                status_code=status.HTTP_404_NOT_FOUND,
                context={"request": request,"status": False},
            )
        return response


@router.get("/logout")
async def logout(request: Request):
    """_summary_

    Args:
        request (Request): _description_

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """
    try:
        msg = "You have been logged out"
        # response =  RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND, headers={"msg": msg})
        response =  templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        response.delete_cookie(key="access_token")
        return response
    except Exception as e:
        raise e
