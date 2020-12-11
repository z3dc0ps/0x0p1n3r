FROM python:3-alpine

WORKDIR /app

ADD . .

RUN python3 setup.py install

ENTRYPOINT ["python3", "takeover.py"]
CMD ["-v"]
