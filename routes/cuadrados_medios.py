from funcs.cuadrados_medios import middle_square
from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


router = APIRouter()

@router.post("/cuadrados-medios", response_class=HTMLResponse)
def read_root(request: Request, seed: int = Form(...), quantity: int = Form(...)):
    random_numbers = middle_square(seed, quant_digits=quantity)
    dict_numbers = {"random_numbers": random_numbers,
                    "array_index": range(0, quantity)
                    }
    return templates.TemplateResponse("table_gen.html", {"request": request, "seed": seed, "quantity": quantity, "method": "Cuadrados Medios", "array_numbers": dict_numbers})