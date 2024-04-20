from funcs.congruencial_mixto_decimal import congruential_mixto_decimal_interval
from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


router = APIRouter()

@router.post("/random-decimal", response_class=HTMLResponse)
def read_root(request: Request, seed: int = Form(...), quantity: int = Form(...), interval: str = Form(...)):
    try:
        interval = list(map(float, interval.split(",")))
        random_numbers = congruential_mixto_decimal_interval(seed, quant_digits=quantity, intervalo=interval)
        dict_numbers = {"random_numbers": random_numbers,
                        "array_index": range(0, quantity)
                        }
        return templates.TemplateResponse("table_gen.html", {"request": request, "seed": seed, "quantity": quantity, "method": "Congruencial Mixto Decimal", "array_numbers": dict_numbers, "interval": interval})
    except:
        #Redireccionar a index con mensaje de error
        return templates.TemplateResponse("index.html", {"request": request, "error": "Intervalo inválido, por favor ingrese dos números separados por coma."})