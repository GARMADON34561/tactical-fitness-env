FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY server/requirements.txt /app/server/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic openenv-core openai

# Copy the entire project
COPY . /app

# Expose port
EXPOSE 8000

# Run the FastAPI app (adjust path to your app)
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]