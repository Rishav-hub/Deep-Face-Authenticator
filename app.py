import os
import uvicorn
from fastapi import FastAPI, Response
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from controller.app_controller import application
from controller.auth_controller import authentication

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")

templates = Jinja2Templates(directory= os.path.join(os.getcwd(), "templates"))


@app.get("/")
def read_root():
    try:
        return RedirectResponse(url="/application", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        return templates.TemplateResponse("error.html", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/test")
def test_route():
    return Response("Testing CI-CD")


app.include_router(authentication.router)

app.include_router(application.router)

app.add_middleware(SessionMiddleware, secret_key="!secret")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
