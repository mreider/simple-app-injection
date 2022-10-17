FROM python:3.7-alpine3.16 AS parent
WORKDIR /app
RUN pip3 install pipenv
COPY Pipfile /app/
COPY Pipfile.lock /app/
RUN pipenv install --deploy --system
COPY src /app
ENTRYPOINT ["gunicorn"]
CMD ["app:app"]