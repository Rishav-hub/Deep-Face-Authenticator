# from face_auth.entity.user import User
# from face_auth.business_val.user_val import UserValidation
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette import status
from starlette.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

from controller.auth_controller import authentication
from controller.app_controller import application

# def register_user():

#     user = User()
#     user.name = "John Doe"
#     user.email = "asdkla"
#     user.password = "asdkla"
#     user_validation = UserValidation(user)

#     if user_validation.save(user):

#         print("User is valid")
#         pass
#     else:
#         print("User is invalid")    

# if __name__ == "__main__":

#     register_user()

app = FastAPI()


@app.get("/")
def read_root():
    return RedirectResponse(url="/application", status_code=status.HTTP_302_FOUND)
app.include_router(authentication.router)
app.include_router(application.router)
app.add_middleware(SessionMiddleware, secret_key="!secret")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)