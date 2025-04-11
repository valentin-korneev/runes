import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()
app = FastAPI()


@app.get('/')
async def environ_keys() -> list[str]:
    return list(os.environ.keys())

@app.get('/{key}')
async def get_environ(key: str):
    key_file = f'{key}_FILE'
    if not key.endswith('_FILE') and key_file in os.environ:
        key = key_file

    value = os.getenv(key, None)

    if key.endswith('_FILE'):
        try:
            with open(value, 'r') as file:
                value = file.read()
        except FileNotFoundError:
            value = None

    return { key: value }