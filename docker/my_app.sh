#!/bin/bash

alembic upgrade head

CMD uvicorn my_app.api:app --host 0.0.0.0 --port 8000
