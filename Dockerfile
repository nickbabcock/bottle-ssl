ARG PYTHON_VERSION=2.7
FROM python:${PYTHON_VERSION}
RUN useradd -r --no-user-group BottleUser && \
    echo BottleUser:iambottle | chpasswd
WORKDIR /app
RUN bash -c "openssl req -x509 -nodes -keyout privkey.pem -new -out cacert.pem -subj /CN=localhost -reqexts SAN -extensions SAN -config <(cat /usr/lib/ssl/openssl.cnf <(printf '[SAN]\nsubjectAltName=DNS:localhost')) -sha256 -days 3650"
COPY Pipfil* /app/
RUN pip install pipenv && pipenv install --dev
COPY *.py ./
COPY index.html .

EXPOSE 443
CMD ["pipenv",  "run", "python", "main.py"]
