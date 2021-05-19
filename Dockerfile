FROM python:3.8

RUN pip install pipenv

ENV BASCOBOT_DIR /opt/bascobot

WORKDIR ${BASCOBOT_DIR}

# copy files into container
COPY . ${BASCOBOT}
COPY Pipfile Pipfile.lock ${BASCOBOT_DIR}/

# install dependencies
RUN pipenv install --system --deploy

# run program
CMD ["python", "./bot.py", "&"]
