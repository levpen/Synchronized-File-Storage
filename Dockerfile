FROM python

WORKDIR /app

COPY /server /app

CMD python3 server.py

