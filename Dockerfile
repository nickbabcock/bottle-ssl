ARG PYTHON_VERSION=2.7
FROM python:${PYTHON_VERSION}
RUN useradd -r --no-user-group BottleUser && \
    echo BottleUser:iambottle | chpasswd
WORKDIR /app
RUN bash -c "openssl req -x509 -nodes -keyout privkey.pem -new -out cacert.pem -subj /CN=localhost -reqexts SAN -extensions SAN -config <(cat /usr/lib/ssl/openssl.cnf <(printf '[SAN]\nsubjectAltName=DNS:localhost')) -sha256 -days 3650"
COPY poetry.lock /app/.
COPY pyproject.toml /app/.
RUN pip install poetry && poetry install
COPY *.py ./
COPY index.html .

EXPOSE 443
CMD ["poetry", "run", "python", "main.py"]
