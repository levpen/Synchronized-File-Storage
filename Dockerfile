FROM python
RUN mkdir app
COPY ./server app
ENV PYTHONUNBUFFERED=1
CMD ["python3", "app/server.py"]