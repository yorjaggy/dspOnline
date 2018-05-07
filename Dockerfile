FROM python:slim

COPY ./app/requirements.txt /tmp/app/requirements.txt
RUN pip install --no-cache-dir -r /tmp/app/requirements.txt

CMD [ "python", "./app/app.py" ]
