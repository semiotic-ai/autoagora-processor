[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![Semantic Versioning](https://img.shields.io/badge/semver-2.0.0-green)](https://semver.org/spec/v2.0.0.html)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# AutoAgora Processor

Processes raw `indexer-service` logs from a RabbitMQ queue, saves the results to a PostgreSQL database.

The processing:

- Extracts details about query execution form the log lines: The subgraph deployment, timestamp, query, variables,
execution time and fees paid.
- Normalizes the queries, separates the "query skeleton" from all values and variables.
- Saves the query skeleton (if never seen before), as well as a logs all the information
  about the query execution (including the variable values used).

Refer to [AutoAgora](https://github.com/semiotic-ai/autoagora) for more
details.

## Indexer's guide

### Build

Just build the container!

```sh
docker build -t autoagora-processor .
```

### Usage

Because it is a stateless service, and only consumes from a RabbitMQ queue and adds rows to a PostgreSQL database, the
Autoagora Processor can safely be dynamically scaled horizontally. Note however that it has been observed processing
upwards of 50 queries per second on a single CPU core.

Note that it also needs to connect to the `indexer-agent`'s management API to determine the indexer's current
allocations, and then pull their schemas using the `graph-node` query endpoint.

Configuration:

```txt
usage: autoagora-processor [-h] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] --rabbitmq-host
                           RABBITMQ_HOST [--rabbitmq-queue-name RABBITMQ_QUEUE_NAME]
                           [--rabbitmq-queue-limit RABBITMQ_QUEUE_LIMIT]
                           [--rabbitmq-exchange-name RABBITMQ_EXCHANGE_NAME]
                           [--rabbitmq-username RABBITMQ_USERNAME]
                           [--rabbitmq-password RABBITMQ_PASSWORD] --postgres-host POSTGRES_HOST
                           --postgres-database POSTGRES_DATABASE --postgres-username
                           POSTGRES_USERNAME --postgres-password POSTGRES_PASSWORD
                           [--postgres-port POSTGRES_PORT] --graph-node-query-endpoint
                           GRAPH_NODE_QUERY_ENDPOINT --indexer-agent-mgmt-endpoint
                           INDEXER_AGENT_MGMT_ENDPOINT

options:
  -h, --help            show this help message and exit
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        [env var: LOG_LEVEL] (default: WARNING)
  --rabbitmq-host RABBITMQ_HOST
                        Hostname of the RabbitMQ server used for queuing the GQL logs. [env var:
                        RABBITMQ_HOST] (default: None)
  --rabbitmq-queue-name RABBITMQ_QUEUE_NAME
                        Name of the RabbitMQ queue to pull query-node logs from. [env var:
                        RABBITMQ_QUEUE_NAME] (default: gql_logs_processor)
  --rabbitmq-queue-limit RABBITMQ_QUEUE_LIMIT
                        Size limit of the created RabbitMQ queue. It is discouraged to change that
                        value while the system is running, because it requires manual destruction
                        of the queue and a restart of the whole Auto Agora stack. [env var:
                        RABBITMQ_QUEUE_LIMIT] (default: 1000)
  --rabbitmq-exchange-name RABBITMQ_EXCHANGE_NAME
                        Name of the RabbitMQ exchange query-node logs are pushed to. [env var:
                        RABBITMQ_EXCHANGE_NAME] (default: gql_logs)
  --rabbitmq-username RABBITMQ_USERNAME
                        Username to use for the GQL logs RabbitMQ queue. [env var:
                        RABBITMQ_USERNAME] (default: guest)
  --rabbitmq-password RABBITMQ_PASSWORD
                        Password to use for the GQL logs RabbitMQ queue. [env var:
                        RABBITMQ_PASSWORD] (default: guest)
  --postgres-host POSTGRES_HOST
                        Host of the postgres instance storing the logs. [env var: POSTGRES_HOST]
                        (default: None)
  --postgres-database POSTGRES_DATABASE
                        Name of the logs database. [env var: POSTGRES_DATABASE] (default: None)
  --postgres-username POSTGRES_USERNAME
                        Username for the logs database. [env var: POSTGRES_USERNAME] (default:
                        None)
  --postgres-password POSTGRES_PASSWORD
                        Password for the logs database. [env var: POSTGRES_PASSWORD] (default:
                        None)
  --postgres-port POSTGRES_PORT
                        Port for the logs database. [env var: POSTGRES_PORT] (default: 5432)
  --graph-node-query-endpoint GRAPH_NODE_QUERY_ENDPOINT
                        URL of the indexer's graph-node GraphQL query endpoint. [env var:
                        GRAPH_NODE_QUERY_ENDPOINT] (default: None)
  --indexer-agent-mgmt-endpoint INDEXER_AGENT_MGMT_ENDPOINT
                        URL to the indexer-agent management GraphQL endpoint. [env var:
                        INDEXER_AGENT_MGMT_ENDPOINT] (default: None)
```
