# Rate Limiter

## Description
- My attempt to implement a core simple rate limiter for an API Gateway.
- The algorithm I use here is Token Bucket. The idea is that each IP has a limit tokens to access to the services in a selected window time

## Run local
```
poetry install
poetry run python3 main.py
```