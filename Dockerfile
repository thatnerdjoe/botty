FROM python:3.8


RUN pip install pipenv

ENV BASCOBOT /opt/bascobot
ENV BASCOBOTTOKEN Nzk4NDM2Mjc2MzQ0NDU1MTk5.X_0_ug.nql6nhLy7TeFSh7DNjqCvU1rtyg

WORKDIR ${BASCOBOT}

# copy files into container
COPY . ${BASCOBOT}

# install dependencies
RUN pipenv install --system --deploy

# run program
CMD ["python", "./bot.py", "&"]
