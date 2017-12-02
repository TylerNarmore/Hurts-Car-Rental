FROM python:latest
LABEL maintainer = "Josh Possel"

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]