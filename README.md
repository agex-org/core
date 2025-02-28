# Agex

## install dev dependencies

```shell
   pip install -r requirements-dev.txt
 ```

 ```shell
   pre-commit install
 ```

## Feeds
Feed Educator
```shell
   python3 -m app.agents.educator.feed
 ```

Feed Auditor
```shell
   python3 -m app.agents.auditor.feed
 ```

## Run project

```shell
   docker compose up [--build]
 ```

## Optional tools
Install [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension to be able to send requests in the `requests.http` file.
