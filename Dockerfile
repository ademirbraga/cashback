FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN mkdir /tmp/cashback/
RUN echo 'teste' > /tmp/cashback/debug.log
RUN cat /tmp/cashback/debug.log
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/