FROM python:3.10

WORKDIR /app

COPY . .

COPY requirements_dev.txt requirements_dev.txt

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt



