# CONTRIBUTING

## Dockerfile

```
FROM  python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
```

## How to run the Docker file locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```

## How to run the Docker file on render

> After adding to requirements the `gunicorn`

We change the flask command to `CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]`
