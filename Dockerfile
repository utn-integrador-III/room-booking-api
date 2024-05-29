FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD /usr/local/bin/gunicorn --reload --log-level 'debug' -t 3600 -b :$BOOKING_PORT run_server:App