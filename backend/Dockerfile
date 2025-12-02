# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# copy files
COPY ./app /app/app
COPY requirements.txt /app/requirements.txt

# install dependencies
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# expose port
ENV PORT=8000
EXPOSE 8000

# run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
