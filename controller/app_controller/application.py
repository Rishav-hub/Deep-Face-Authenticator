import os,io,base64
from typing import List, Optional

from fastapi import APIRouter, File, Request
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from controller.auth_controller.authentication import get_current_user
from face_auth.business_val.user_embedding_val import (
    UserLoginEmbeddingValidation,
    UserRegisterEmbeddingValidation,
)

router = APIRouter(
    prefix="/application",
    tags=["application"],
    responses={"401": {"description": "Not Authorized!!!"}},
)
templates = Jinja2Templates(directory= os.path.join(os.getcwd(), "templates"))

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class ImageForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.image1: Optional[str] = None
        self.image2: Optional[str] = None
        self.image3: Optional[str] = None
        self.image4: Optional[str] = None
        self.image5: Optional[str] = None
        self.image6: Optional[str] = None
        self.image7: Optional[str] = None
        self.image8: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.image1 = form.get("image1")
        self.image2 = form.get("image2")
        self.image3 = form.get("image3")
        self.image4 = form.get("image4")
        self.image5 = form.get("image5")
        self.image6 = form.get("image6")
        self.image7 = form.get("image7")
        self.image8 = form.get("image8")


@router.get("/", response_class=HTMLResponse)
async def application(request: Request):
    try:
        
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
        return templates.TemplateResponse("login_embedding.html", context={"request": request,"status_code":status.HTTP_200_OK,"msg":"Logged in Successfully","user":user['username']})

    except Exception as e:
        msg = "Error in Login Embedding in Database"
        response = templates.TemplateResponse("error.html",
                status_code=status.HTTP_404_NOT_FOUND,
                context={"request": request,"status": False, "msg": msg},
            )
        return response 

@router.post("/")
async def loginEmbedding(
    request: Request
):
    """This function is used to get the embedding of the user while login

    Args:
        request (Request): _description_
        files (List[UploadFile], optional): _description_. Defaults to \File(description="Multiple files as UploadFile").

    Returns:
        response: If user is authenticated then it returns the response
    """

    try:
        
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

        user_embedding_validation = UserLoginEmbeddingValidation(user["uuid"])

        form = ImageForm(request)
        await form.create_oauth_form()
        files = []
        base64_images = [form.image1,form.image2,form.image3,form.image4,form.image5,form.image6,form.image7,form.image8]
        for image in base64_images:
            strip_metadata = image[image.find(",")+1:]
            decode_base64 = base64.b64decode(strip_metadata)
            image_bytes = io.BytesIO(decode_base64)
            bytes_value = image_bytes.getvalue()
            files.append(bytes_value)

        # Compare embedding
        user_simmilariy_status = user_embedding_validation.compareEmbedding(files)

        if user_simmilariy_status:
            msg = "User is authenticated"
            response = templates.TemplateResponse("login_embedding.html",
                status_code=status.HTTP_200_OK,
                context={"request": request,"status_code":status.HTTP_200_OK, "msg": msg,"user":user['username']},
            )
            return response
            
        else:
            msg = "User is NOT authenticated"
            response = templates.TemplateResponse("unauthorized.html",
                status_code=status.HTTP_404_NOT_FOUND,
                context={"status": False, 'status_code':status.HTTP_404_NOT_FOUND,"msg": msg},
            )
            return response
    except Exception as e:
        msg = "Error in Login Embedding in Database"
        response = templates.TemplateResponse("unauthorized.html",
                status_code=status.HTTP_404_NOT_FOUND,
                context={"request": request,"status": False, "msg": msg},
            )
        return response

@router.get("/register_embedding", response_class=HTMLResponse)
async def application(request: Request):
    try:        
        uuid = request.session.get("uuid")
        if uuid is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
        return templates.TemplateResponse("register_embedding.html", context={"request": request,"status_code":status.HTTP_200_OK,"msg":"Logged in Successfully" })
    except Exception as e:
        msg = "Error in Login Embedding in Database"
        response = templates.TemplateResponse("error.html",
                status_code=status.HTTP_404_NOT_FOUND,
                context={"request": request,"status": False, "msg": msg},
            )
        return response

@router.post("/register_embedding")
async def registerEmbedding(
    request: Request
):
    """This function is used to get the embedding of the user while register

    Args:
        request (Request): _description_
        files (List[UploadFile], optional): _description_. Defaults to \File(description="Multiple files as UploadFile").

    Returns:
        Response: If user is registered then it returns the response
    """
    try:
        uuid = request.session.get("uuid")
        if uuid is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
        
        form = ImageForm(request)
        await form.create_oauth_form()
        files = []
        base64_images = [form.image1,form.image2,form.image3,form.image4,form.image5,form.image6,form.image7,form.image8]
        for image in base64_images:
            strip_metadata = image[image.find(",")+1:]
            decode_base64 = base64.b64decode(strip_metadata)
            image_bytes = io.BytesIO(decode_base64)
            bytes_value = image_bytes.getvalue()
            files.append(bytes_value)
    
        # Get the UUID from the session
        user_embedding_validation = UserRegisterEmbeddingValidation(uuid)

        # Save the embeddings
        user_embedding_validation.saveEmbedding(files)

        msg = "Embedding Stored Successfully in Database"

        response = templates.TemplateResponse("login.html",
                status_code=status.HTTP_200_OK,
                context={"request": request,"status": False, "msg": msg},
            )
        return response

    except Exception as e:
        msg = "Error in Storing Embedding in Database"
        response = templates.TemplateResponse("error.html",
                status_code=status.HTTP_404_NOT_FOUND,
                context={"request": request,"status": False, "msg": msg},
            )
        return response
