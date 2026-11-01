FROM python:3.11-slim
WORKDIR /app
ENV HF_HOME=/app/hf_cache
COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python ingest.py && chmod -R 777 /app
EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]