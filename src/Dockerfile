FROM python:3.13-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy your app
COPY src .

CMD ["python", "pipeline.py"]
