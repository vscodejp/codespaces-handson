FROM node:16.19-bullseye as node-build-env
WORKDIR /workspace
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY tsconfig.json
COPY frontend/ .
RUN mkdir -p /workspace/public/js/
RUN npx tsc

FROM python:3.10-bullseye
WORKDIR /app
RUN pip install poetry==1.1.13
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install

COPY api ./api
COPY --from=node-build-env public ./public

CMD ["poetry", "run", "python", "api/app.py"]
