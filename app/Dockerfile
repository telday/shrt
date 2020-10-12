FROM python:3.8.3-alpine


ENV APP_HOME=/usr/src/app/
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh $APP_HOME
run mkdir $APP_HOME/staticfiles

COPY . .

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
