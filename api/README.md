Windspotter API
===============

This is the API for the Windspotter project. It is a FastAPI app that can be
hosted in AWS Lambda.

Development
-----------

[uv](https://docs.astral.sh/uv/) is used to manage this python project. To
install dependencies, run

```shell
uv sync
```

This will install all the dependencies, including dev-dependencies. You can then
run the app locally using [uvicorn](https://uvicorn.dev/):

```shell
uv run uvicorn app.main:app --reload --port 8000
```
