FROM python:3.12.2-alpine

WORKDIR /source

COPY . .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 9360

CMD python3.12 main.py
