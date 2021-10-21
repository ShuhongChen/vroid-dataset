FROM python

ENV PYTHONBUFFERED=1

COPY . /app

# ADD ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt


# CMD ["python","serve.py"]