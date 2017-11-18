FROM python:latest
LABEL maintainer = "Josh Possel"

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "run.py"]
