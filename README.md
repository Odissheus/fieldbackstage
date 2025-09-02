# React Field Insights — bootstrap

## Setup
1) Copia `.env.example` in `.env` e compila i valori.
2) Crea e attiva venv, poi:
   ```bash
   cd server
   pip install -r requirements.txt
   # Migrazioni DB (sviluppo SQLite di default in alembic.ini)
   alembic upgrade head
   uvicorn main:app --reload
   ```

3. Apri `http://localhost:8000/docs` (Swagger UI generato da OpenAPI in runtime).

## Genera SDK dai file OpenAPI

* Web TS:

  ```bash
  ./scripts/gen_client_web.sh
  ```
* Flutter/Dart:

  ```bash
  ./scripts/gen_client_flutter.sh
  ```

## Job settimanale (dev)

```bash
python -m server.jobs.weekly_report_job
```

## Dove lavorare

* API: `server/routers/*` (aderiscono a `docs/openapi.yaml`)
* Report: template in `templates/report/*`
* Q&A LLM: `server/routers/qa.py` + indicizzazione in `weekly_report_job.py`
* Migrazioni DB: `server/alembic/*` — comandi: `alembic revision --autogenerate -m "msg"`, `alembic upgrade head`

