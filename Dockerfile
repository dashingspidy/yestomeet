FROM python:3.6.3
ADD . /yestomeet
WORKDIR /yestomeet
RUN pip install -r requirements.txt
CMD ["gunicorn", "-k", "gevent", "-w", "1", "-t", "100", "run:app"]