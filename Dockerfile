FROM python:3.12.2-alpine

WORKDIR /source

COPY . .

# Install necessary dependencies
RUN apk update && apk add --no-cache \
    libffi-dev \
    postgresql-dev \
    musl-dev

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 9360

CMD python3.12 main.py
