from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes.user import user #para poder usar las rutas de user
from mangum import Mangum #si nos la llevaremos a AWS Lambda

#app = FastAPI()
app = FastAPI(
    title="FastAPI demo API",
    description="CRUD con FastAPI, Python 3.12",
    version="0.0.1",
    openapi_tags=[{
        "name": "Users",
        "description": "Users routes"
    }]
)

@app.get("", include_in_schema=False)  # Handle empty path
async def root_empty():
    return RedirectResponse(url="/docs")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(user)

handler = Mangum(app) #si usaremos AWS Lambda