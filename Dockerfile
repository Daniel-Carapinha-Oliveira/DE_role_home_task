# pull official base image
FROM python:3.12.11-alpine

# set work directory
WORKDIR /home_task

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY ./requirements/* ./requirements/

RUN pip install --upgrade pip
RUN pip install -r ./requirements/base.txt

# copy boot .sh
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]