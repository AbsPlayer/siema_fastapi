The required environment variables:
(see `.envrc_example`)
```bash
# .envrc
export POSTGRES_USER=username
export POSTGRES_PASSWORD=password
export POSTGRES_DB=test_db

export DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
```

Project deploying:
1. make dir for project and go in it:
```bash
   mkdir project_dir_name
   cd project_dir_name/
```
2. make virtual environment for project and activate it:
```bash
   python3 -m venv .venv
   . .venv/bin/activate
```
3. install all required dependencies:
```bash
   pip install -r requirements.txt
```
---
Make migrations:
```bash
    alembic upgrade head
```
---
For filling database by fake data:

(if docker is used you must start docker and run command:
```bash
   docker exec -it siema_server /bin/sh
```
and then make next commands)
1. run FastAPI shell:
```bash
    python3 -m fastapi_shell --include app
```
2. and run commands:
```bash
   from app.utils import fill_fake_data
   fill_fake_data(<qty_categories>, <qty_products>, <qty_sales>)
```
where
`qty_categories` `qty_products` and `qty_sales` are corresponding quantities of rows for database.
These values are optional.
By default, qty_categories = 10, qty_products = 100, qty_sales = 1000


---
For running server go to app directory and run:
```bash
    uvicorn app.main:app --reload
```
---

For running test go to app directory and run:

(if docker is used you must start docker and run command:
```bash
   docker exec -it siema_server /bin/sh
```
and then make next commands)
```bash
    coverage run -m pytest
```
To see coverage report run:
```bash
    coverage report -m
```

```bash
# docker start
docker compose up

# docker stop
docker compose down
```