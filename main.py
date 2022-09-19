
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# `app` instance 
app = FastAPI()

# `template` instance 
template = Jinja2Templates(directory='templates')

@app.get('/',response_class=HTMLResponse)
def root(request:Request):
    return template.TemplateResponse('index.html',{'request':request})

