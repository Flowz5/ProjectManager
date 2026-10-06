from fastapi import FastAPI

app = FastAPI(title='{name}')

@app.get('/')
def read_root():
    return {'message': 'API en ligne !'}