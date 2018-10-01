ARG PYTHON_VERSION=2.7
FROM python:${PYTHON_VERSION}
RUN useradd -r --no-user-group BottleUser && \
    echo BottleUser:iambottle | chpasswd
WORKDIR /app
RUN openssl req -new -x509 -days 365 -nodes -out cacert.pem -keyout privkey.pem -subj "/C=AA/ST=State/L=Location/O=IT/CN=bottle-ssl.com"
COPY Pipfil* /app/
RUN pip install pipenv && pipenv install --dev
COPY *.py ./
COPY index.html .

EXPOSE 443
CMD ["pipenv",  "run", "python", "main.py"]
