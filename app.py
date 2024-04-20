from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
from routes import congruencial_mixto, congruencial_multiplicativo, cuadrados_medios

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(congruencial_mixto.router)
app.include_router(congruencial_multiplicativo.router)
app.include_router(cuadrados_medios.router)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, })



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app",host="0.0.0.0" , port=8000, reload=True)
