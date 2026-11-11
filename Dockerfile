
FROM mcr.microsoft.com/playwright/python:v1.63.0-noble

WORKDIR /app

# Install Microsoft ODBC Driver 18 for SQL Server
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl ca-certificates unixodbc-dev && \
    curl -fsSL \
        https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb \
        -o /tmp/packages-microsoft-prod.deb && \
    dpkg -i /tmp/packages-microsoft-prod.deb && \
    rm /tmp/packages-microsoft-prod.deb && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "pytest", "-v", "--ai-analyze"]

