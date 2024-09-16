from fastapi import FastAPI, Request, Form, Path, Query, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from schemas import NewTour, SavedTour, TourPrice, DeletedTour
from storage import storage

app = FastAPI(
    debug=True,
    title='Tour Agency',
)

# Налаштування шаблонів та статичних файлів
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

# Головна сторінка з пропозиціями турів
@app.get('/', include_in_schema=False)
@app.post('/', include_in_schema=False)
def index(request: Request, q: str = Form(default='')):
    tours = storage.get_tours(limit=40, q=q)
    context = {
        'request': request,
        'page_title': 'All tours',
        'tours': tours
    }
    return templates.TemplateResponse('index.html', context=context)

# Детальна сторінка тура
@app.get('/{tour_id}', include_in_schema=False)
def tour_detail(request: Request, tour_id: int):
    tour = storage.get_tour(tour_id)
    context = {
        'request': request,
        'page_title': f'Tour {tour.title}',
        'tour': tour
    }
    return templates.TemplateResponse('details.html', context=context)

# CRUD API для турів
@app.post('/api/tour/', response_model=SavedTour, description='Create tour', status_code=status.HTTP_201_CREATED, tags=['API', 'Tour'])
def create_tour(new_tour: NewTour):
    return storage.create_tour(new_tour)

@app.get('/api/tour/', response_model=list[SavedTour], tags=['API', 'Tour'])
def get_tours(limit: int = Query(default=10, description='Limit of tours to display', gt=0), q: str = ''):
    return storage.get_tours(limit=limit, q=q)

@app.get('/api/tour/{tour_id}', response_model=SavedTour, tags=['API', 'Tour'])
def get_tour(tour_id: int = Path(ge=1, description='Tour ID')):
    return storage.get_tour(tour_id)

@app.patch('/api/tour/{tour_id}', response_model=SavedTour, tags=['API', 'Tour'])
def update_tour_price(tour_id: int, new_price: TourPrice):
    return storage.update_tour_price(tour_id, new_price.price)

@app.delete('/api/tour/{tour_id}', response_model=DeletedTour, tags=['API', 'Tour'])
def delete_tour(tour_id: int):
    storage.delete_tour(tour_id)
    return DeletedTour(id=tour_id)

@app.get('/navigation/', include_in_schema=False)
def navigation(request: Request):
    context = {
        'request': request,
        'page_title': 'How to find us',
    }
    return templates.TemplateResponse('navigation.html', context=context)
