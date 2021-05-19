FROM python:3


RUN pip install pipenv

ENV BASCOBOT /opt/bascobot
ENV BASCOBOTTOKEN Nzk4NDM2Mjc2MzQ0NDU1MTk5.X_0_ug.deBrZIqOVNvDHQikqEOk-rmrMn8 

WORKDIR ${BASCOBOT}

# copy files into container
COPY . ${BASCOBOT}

# install dependencies
RUN pipenv install --system --deploy
RUN pipenv run python ./bot.py
