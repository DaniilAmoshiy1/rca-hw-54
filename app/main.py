import asyncio
from random import randint

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()
app.mount(
    '/static',
    StaticFiles(directory='static'),
    name='static'
)

templates = Jinja2Templates(directory='templates')


PRODUCT_LIST: list[str] = [
    'Yogurt in the "Bonus" market',
    'MSI GeForce RTX 4090 in "DNS"',
    'Headphones Razer Blackshark V2 X on "Ozon"',
    'Shampoo with aloe on "AliExpress"',
    'Кукумбер(огурец) в "YerevanCity"',
    'Гитара YAMAHA F310 Natural на "Авито"',
    'Крыса пароды "Рекс" в зоомагазине "KAKADU"',
    'Футболка "GUCCI" на Вайлдбериз'
]


async def fake_edit_prices():
    while True:
        await asyncio.sleep(1)
        index: int = randint(0, len(PRODUCT_LIST) - 1)
        product: str = PRODUCT_LIST[index]
        new_price: int = randint(10, 100000)
        yield f"Data: {product} - New price: ${new_price}\n\n"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/events")
async def _get_events(request: Request):
    referer = request.headers.get("referer")
    if referer and referer.endswith("/"):
        return StreamingResponse(fake_edit_prices(), media_type="text/event-stream")
    else:
        return templates.TemplateResponse("access_denied.html", {"request": request})
