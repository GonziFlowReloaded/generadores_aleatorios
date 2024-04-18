from funcs.congruencial_multiplicativo import congruential_multiplicative
from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


router = APIRouter()

@router.post("/congruencial-multiplicativo", response_class=HTMLResponse)
def read_root(request: Request, seed: int = Form(...), quantity: int = Form(...)):
    random_numbers = congruential_multiplicative(seed, quant_digits=quantity)
    dict_numbers = {"random_numbers": random_numbers,
                    "array_index": range(0, quantity)
                    }
    return templates.TemplateResponse("table_gen.html", {"request": request, "seed": seed, "quantity": quantity, "method": "Congruencial Multiplicativo", "array_numbers": dict_numbers})