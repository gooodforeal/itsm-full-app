from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory='client_site/templates')


@router.get('/client/create')
async def get_students_html(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})

