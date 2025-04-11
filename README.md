# Runes

## Запуск
```bash
docker compose up -d
```

Для проверки можно воспользоваться URL:
1. `http://<host>:<port>/` - получение списка ключей
2. `http://<host>:<port>/<key>` - получение значения ключа

## Локальный запуск (установке + формирование .env)
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python dagaz.py <env>
```