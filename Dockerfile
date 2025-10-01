FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# pre-download model into cache
RUN mkdir -p /opt/render/.cache/huggingface
RUN TRANSFORMERS_CACHE=/opt/render/.cache/huggingface python -c "from transformers import pipeline; pipeline('text-to-audio','facebook/musicgen-small')"

COPY . .

CMD ["gunicorn", "app:app", "--timeout", "120", "--bind", "0.0.0.0:$PORT"]
