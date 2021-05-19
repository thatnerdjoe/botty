FROM python:3.8

# install pipenv
RUN pip install pipenv

# set working directory
ENV BASCOBOTDIR /opt/bascobot
WORKDIR ${BASCOBOTDIR}

# copy dependency lists into container
COPY Pipfile Pipfile.lock requirements.txt ${BASCOBOTDIR}/

# install dependencies and do not use a shell (--system)
# fail if any dependencies do not match the hash in Pipfile.lock (--deploy)
RUN pipenv install --system --deploy

# copy all files into container
COPY . .

# set environment variables 
ARG token=0
ENV BASCOBOTTOKEN=$token

# run program
CMD ["python", "./bot.py"]
