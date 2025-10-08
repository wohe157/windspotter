Windspotter API
===============

This is the API for the Windspotter project. It is a FastAPI app that can be
hosted in AWS Lambda.

Configuration
-------------

Global configuration is handled via
[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).
Defaults are set in `app/core/config.py` and can be overridden using
environment variables or by adding a `.env` file in the root of this folder.

> Note: Some settings, like secrets, are mandatory.

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
