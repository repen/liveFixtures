#docker build -t check_count_fixtures:latest .
#docker run --name count_fixtures -d -v live_fixtures:/script/data check_count_fixtures:latest
FROM python:3.8

ENV BASE_DIR /script
ENV EXTERNAL_WORK true
ENV REMOTE_SERVER None

WORKDIR ${BASE_DIR}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY script ${BASE_DIR}

CMD python main.py