# Copyright 2022-, Semiotic AI, Inc.
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import Any

import configargparse


class _Args(configargparse.Namespace):
    def __getattribute__(self, name) -> Any:
        return object.__getattribute__(self, name)


# `args` will contain the global argument values after calling `init_config()`
args = _Args()


def init_config():
    """Parses the arguments from the global argument parser and sets logging config.

    To add arguments, simply add them to the global argument parser from any module, as
    long as the modules are imported before the invocation of that function.

    Argument values are added to the global `args` namespace object declared in this
    module.
    """
    argsparser = configargparse.get_argument_parser()
    #
    # General Arguments
    #
    argsparser.add_argument(
        "--log-level",
        env_var="LOG_LEVEL",
        type=str,
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        default="WARNING",
        required=False,
    )
    #
    # RabbitMQ
    #
    argsparser.add_argument(
        "--rabbitmq-host",
        env_var="RABBITMQ_HOST",
        required=True,
        help="Hostname of the RabbitMQ server used for queuing the GQL logs.",
    )
    argsparser.add_argument(
        "--rabbitmq-queue-name",
        env_var="RABBITMQ_QUEUE_NAME",
        default="gql_logs_processor",
        required=False,
        help="Name of the RabbitMQ queue to pull query-node logs from.",
    )
    argsparser.add_argument(
        "--rabbitmq-queue-limit",
        env_var="RABBITMQ_QUEUE_LIMIT",
        type=int,
        default=1000,
        required=False,
        help="Size limit of the created RabbitMQ queue. It is discouraged to change that "
        "value while the system is running, because it requires manual destruction of the "
        "queue and a restart of the whole Auto Agora stack.",
    )
    argsparser.add_argument(
        "--rabbitmq-exchange-name",
        env_var="RABBITMQ_EXCHANGE_NAME",
        default="gql_logs",
        required=False,
        help="Name of the RabbitMQ exchange query-node logs are pushed to.",
    )
    argsparser.add_argument(
        "--rabbitmq-username",
        env_var="RABBITMQ_USERNAME",
        type=str,
        default="guest",
        required=False,
        help="Username to use for the GQL logs RabbitMQ queue.",
    )
    argsparser.add_argument(
        "--rabbitmq-password",
        env_var="RABBITMQ_PASSWORD",
        type=str,
        default="guest",
        required=False,
        help="Password to use for the GQL logs RabbitMQ queue.",
    )
    #
    # Logs DB
    #
    argsparser.add_argument(
        "--postgres-host",
        env_var="POSTGRES_HOST",
        required=True,
        help="Host of the postgres instance storing the logs.",
    )
    argsparser.add_argument(
        "--postgres-database",
        env_var="POSTGRES_DATABASE",
        required=True,
        help="Name of the logs database.",
    )
    argsparser.add_argument(
        "--postgres-username",
        env_var="POSTGRES_USERNAME",
        required=True,
        help="Username for the logs database.",
    )
    argsparser.add_argument(
        "--postgres-password",
        env_var="POSTGRES_PASSWORD",
        required=True,
        help="Password for the logs database.",
    )
    argsparser.add_argument(
        "--postgres-port",
        env_var="POSTGRES_PORT",
        default=5432,
        required=False,
        help="Port for the logs database.",
    )
    #
    # Graph Node
    #
    argsparser.add_argument(
        "--graph-node-query-endpoint",
        env_var="GRAPH_NODE_QUERY_ENDPOINT",
        required=True,
        help="URL of the indexer's graph-node GraphQL query endpoint.",
    )
    #
    #
    #
    argsparser.add_argument(
        "--graph-postgres-host",
        env_var="GRAPH_POSTGRES_HOST",
        required=True,
        help="URL of the postgres instance use by the graph-nodes.",
    )
    argsparser.add_argument(
        "--graph-postgres-database",
        env_var="GRAPH_POSTGRES_DATABASE",
        required=True,
        help="Name of the graph-node database.",
    )
    argsparser.add_argument(
        "--graph-postgres-username",
        env_var="GRAPH_POSTGRES_USERNAME",
        required=True,
        help="Username for the graph-node databse.",
    )
    argsparser.add_argument(
        "--graph-postgres-password",
        env_var="GRAPH_POSTGRES_PASSWORD",
        required=True,
        help="Password for the graph-node database.",
    )
    argsparser.add_argument(
        "--graph-postgres-port",
        env_var="GRAPH_POSTGRES_PORT",
        default=5432,
        required=False,
        help="Port for the graph-node database.",
    )
    argsparser.parse_args(namespace=args)

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.root.setLevel(args.log_level)
