FROM python:3.10-buster

# We don't want to run our application as root if it is not strictly necessary, even in a container.
# Create a user and a group called 'app' to run the processes.
# A system user is sufficient and we do not need a home.
RUN adduser --system --group --no-create-home app

COPY . /app

WORKDIR /app

RUN pip install -r requirements-dev.txt

# Hand everything over to the 'app' user
RUN chown -R app:app /app

USER app

CMD ["flask", "run", "--host=0.0.0.0"]
