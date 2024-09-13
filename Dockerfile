FROM python:3.10

WORKDIR /backend

COPY . /backend

ENV PYTHONPATH=/backend
ENV PYTHONUNBUFFERED=1

# List the contents of the /backend directory for debugging
# RUN dir /s

RUN pip install --no-cache-dir --upgrade -r backend/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["fastapi", "dev", "/app/main.py"]