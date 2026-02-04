# #----------Stage 1: builder -----

# FROM python:3.10-slim AS builder

# WORKDIR /build

# COPY requirements.txt .

# RUN apt-get update && apt-get install -y gcc libpq-dev \
#     && pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt  --target /install


# #---------------Stage 2: runtime-------


# FROM python:3.10-slim

# WORKDIR /app

# COPY --from=builder /install /usr/local/lib/python3.10/site-packages

# COPY . .

# ENV PYTHONPATH=/app:/usr/local/lib/python3.10/site-packages

# CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#---------------- Stage 1: Builder ----------------
FROM python:3.10-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc libpq-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

#---------------- Stage 2: Runtime ----------------
FROM python:3.10-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source code
COPY . .

ENV PYTHONPATH=/app

# CMD uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]