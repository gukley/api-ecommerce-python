FROM python:3.9

RUN groupadd --gid 1000 vscode && \
    useradd --uid 1000 --gid 1000 -m vscode

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
