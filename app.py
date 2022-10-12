from fastapi import FastAPI,Response
from starlette.responses import RedirectResponse
from starlette import status
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

from controller.auth_controller import authentication
from controller.app_controller import application


app = FastAPI()


@app.get("/")
def read_root():
    return RedirectResponse(url="/application", status_code=status.HTTP_302_FOUND)

@app.get("/test")
def test_route():
    return Response("Testing CICD")

app.include_router(authentication.router)

app.include_router(application.router)

app.add_middleware(SessionMiddleware, secret_key="!secret")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
    
