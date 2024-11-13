# Hexagonal Python Project Template

#### Warning: This project is an experimental template created for learning purposes only.

<p align="center">
    <img src="https://github.com/baldimario/hexagonal-python/blob/develop/logo.png?raw=true" width="300px" height="300px" />
</p>

DDD and CQRS in Modern Python Environment
---
This project is a proof-of-concept template designed to demonstrate the application of Domain-Driven Design (DDD) and Command Query Responsibility Segregation (CQRS) principles in a modern Python environment. It is intended for educational purposes only and should not be used in production without thorough testing and validation.

## Usage

When using this project template, you should copy the template, keep what you need, and remove what you don't. This will allow you to tailor the project to your specific requirements and avoid unnecessary complexity.

## Features

- 🔄 Isolated endvironment:
    - ✅ Containerized
    - Environment Variable overriding
- ✅ Development and Production configuration:
    - ✅ environment variables and configurations
    - ✅ denepndencies management
- ✅ Poetry managed
    - ✅ Development and Production dependencies isolation
- 🔄 Design Patterns
    - ✅ Dependency Injection
    - ✅ CQRS
        - 🔄 with multiple brokers:
            - ✅ logical (local)
            - ✅ dependency injection
            - kafka
            - pulsar
            - rabbitmq
            - redis pub/sub
            - amazon sqs
            - mqtt
            - eventstore
        - Common commands and queries bundled helper services
            - S3
            - DynamoDB
            - ECS
            - AWS Lambda
            - OpenFaas
- ✅ Code Quality
    - ✅ Code Style: Pylint (Analysis), Black (Fix)
    - ✅ Type Checking: Pyright (Analysis)
- ✅ Testing
    - ✅ Unit Test Suite: PyTest
    - ✅ Funcitonal Test Suite: Behave
        - ✅ with Mocks, Steps, Local containers
- Configurable runtime entrypoint:
    - App/Worker
        - App: container running application code and sending commands
        - Worker: container listening events from specific broker
    - AWS Lambda
    - OpenFaas
    - Celery
- ✅ Docker Services Preset with Reverse Proxy:
    - ✅ Traefik
    - ✅ Mailcatcher
    - ✅ Redis
    - ✅ Redisinsight
    - ✅ RabbitMQ
    - ✅ Kafka
    - ✅ MySQL
    - ✅ Phpmyadmin
    - ✅ PostgreSQL
    - ✅ Pgadmin
    - ✅ Minio
    - ✅ Keycloak
    - ✅ Cassandra
    - ✅ Cassandra-web
    - ✅ Ollama
    - ✅ Open-WebUI
    - ✅ ElasticSearch
    - ✅ Kibana
    - ✅ Dejavu
    - ✅ Localstack

## Enable Services using docker compose profiles

In the `.env.make` that overrides `stack/docker/.env` file for the `COMPOSE_PROFILES` environment vairable, you can enable or disable services by adding or removing the service name from the `COMPOSE_PROFILES` variable.

The default profile is `default` and it is always enabled, it is used to enable the default services that are always required: `app`, `dnsmasq`, `traefik`.

For example: to enable RabbitMQ, add `rabbitmq` to the `COMPOSE_PROFILES` variable, like this:


```bash
COMPOSE_PROFILES=default,rabbitmq
```

A special profile is `all` that enables all services.


## Usage

### Install

```bash
make build
```

### Run

```bash
make run
```

or detached

```bash
make up
```

or enter the container

```bash
make shell
```

## Development

### Run code style checks, linting, type checking, unit tests and functional tests

```bash
make check
```

and to format code

```bash
make format
```

### Run tests

```bash
make unit
make functional
make coverage
```

### Linting, Type Checking and Formatting

```bash
make cs
make lint
make type-check
make format
```

---

## Coverage report example

```
Name                                            Stmts   Miss  Cover
-------------------------------------------------------------------
__init__.py                                         0      0   100%
features/environment.py                             2      0   100%
features/steps/di.py                               33      0   100%
features/steps/di_command_bus.py                   54      0   100%
features/steps/di_query_bus.py                     54      0   100%
src/__init__.py                                     1      0   100%
src/config.py                                      21      1    95%
src/core/__init__.py                                0      0   100%
src/core/cqrs/__init__.py                           0      0   100%
src/core/cqrs/bus.py                               10      0   100%
src/core/cqrs/command.py                            3      0   100%
src/core/cqrs/command_bus.py                       12      0   100%
src/core/cqrs/command_handler.py                    8      1    88%
src/core/cqrs/di_command_bus.py                    21      0   100%
src/core/cqrs/di_query_bus.py                      21      1    95%
src/core/cqrs/exceptions.py                        18      0   100%
src/core/cqrs/handler.py                            5      0   100%
src/core/cqrs/query.py                              2      0   100%
src/core/cqrs/query_bus.py                         13      0   100%
src/core/cqrs/query_handler.py                      7      0   100%
src/core/cqrs/simple_command_bus.py                17      0   100%
src/core/cqrs/types.py                              7      0   100%
src/core/di/__init__.py                             2      0   100%
src/core/di/container.py                           20      0   100%
src/core/di/exceptions.py                           1      0   100%
src/core/di/inject.py                              90     26    71%
src/example/__init__.py                             0      0   100%
src/example/domain/__init__.py                      0      0   100%
src/example/domain/command/example_command.py       6      0   100%
src/example/domain/command/example_handler.py      11      3    73%
src/example/domain/query/__init__.py                0      0   100%
src/example/domain/query/example_handler.py        10      1    90%
src/example/domain/query/example_query.py           6      0   100%
src/example/domain/query/example_response.py        5      0   100%
src/example/infrastructure/__init__.py              0      0   100%
src/example/infrastructure/cli/__init__.py          0      0   100%
src/example/infrastructure/cli/main.py             16      4    75%
tests/__init__.py                                   0      0   100%
tests/unit/__init__.py                              0      0   100%
tests/unit/test_container.py                       30      0   100%
tests/unit/test_di_command_bus.py                  37      0   100%
tests/unit/test_di_query_bus.py                    37      0   100%
tests/unit/test_dummy.py                            7      0   100%
tests/unit/test_simple_command_bus.py              31      0   100%
-------------------------------------------------------------------
TOTAL                                             618     37    94%
```

To generate coverage report in interactive html format, run:

```bash
make coverage-html
```

---

## Web Dashboards on reverse proxy

`lvh.me` is a special domain name that resolves to `127.0.0.1` (`localhost`) by default. This allows you to use it as a shortcut for local development, instead of `*.localhost`. All its subdomains also point to `127.0.0.1`, making it a convenient choice for local development environments.

All subdomains and main domain are configured in the `stack/docker/.env` file.
These are the default subdomains.

| Env var | Domain | Description |
|---|---|---|
| DOMAIN | lvh.me | Main domain |
| REVERSE_PROXY_SUBDOMAIN | reverse-proxy.lvh.me | Points to Traefik web ui |
| STORAGE_SUBDOMAIN | storage-admin.lvh.me | Points to minio admin panel |
| STORAGE_API_SUBDOMAIN | storage-api.lvh.me | Points to minio APIs |
| RABBITMQ_SUBDOMAIN | rabbitmq-management.lvh.me | RabbitMQ management interface |
| PHPMYADMIN_SUBDOMAIN | phpmyadmin.lvh.me | phpMyAdmin panel |
| PGADMIN_SUBDOMAIN | pgadmin.lvh.me | pgadmin panel |
| MAIL_SUBDOMAIN | mail.lvh.me | mailcatcher interface |
| REDISINSIGHT_SUBDOMAIN | redis-insight.lvh.me | redis management interface |
| CASSANDRA_WEB_SUBDOMAIN | cassandra-web.lvh.me | cassandra management interface |
| LOCAL_SUBDOMAIN | local.lvh.me | local domain to manage development 4th level domains |
| LLM_SUBDOMAIN | llm.lvh.me | ollama api |
| OPEN_WEBUI_SUBDOMAIN | ai.lvh.me | web panel for llm managgement |
| ELASTICSEARCH_SUBDOMAIN | search.lvh.me | elasticsearch |
| DEJAVU_SUBDOMAIN | dejavu.lvh.me | elasticsearch management interface |
| KIBANA_SUBDOMAIN | kibana.lvh.me | kibana admin panel for bi |
| KAFKA_UI_SUBDOMAIN | kafka-ui.lvh.me | kafka management interface |
| LOCALSTACK_GATEWAY_SUBDOMAIN| localstack.lvh.me | localstack gateway |
