from funcs.congruencial_mixto import congruential_mixed
from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


router = APIRouter()

@router.post("/congruencial-mixto", response_class=HTMLResponse)
def read_root(request: Request, seed: int = Form(...), quantity: int = Form(...)):
    random_numbers = congruential_mixed(seed, quant_digits=quantity)
    dict_numbers = {"random_numbers": random_numbers,
                    "array_index": range(0, quantity)
                    }
    return templates.TemplateResponse("table_gen.html", {"request": request, "seed": seed, "quantity": quantity, "method": "Congruencial Mixto", "array_numbers": dict_numbers})