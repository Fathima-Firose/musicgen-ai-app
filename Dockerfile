FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Pre-download MusicGen model
RUN python -c "from transformers import pipeline; pipeline('text-to-audio','facebook/musicgen-small')"

COPY . .

CMD ["gunicorn", "app:app", "--timeout", "120", "--bind", "0.0.0.0:10000"]
