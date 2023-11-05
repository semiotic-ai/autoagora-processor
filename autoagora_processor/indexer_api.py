# Copyright 2023-, Semiotic AI, Inc.
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import Mapping, Optional, Set

import backoff
from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from requests import RequestException

from autoagora_processor.config import args


@backoff.on_exception(backoff.expo, RequestException, max_time=30, logger=logging.root)
def query_indexer_agent(query: str, variables: Optional[Mapping] = None):
    client = Client(
        transport=RequestsHTTPTransport(args.indexer_agent_mgmt_endpoint),
        fetch_schema_from_transport=False,
    )
    result = client.execute(gql(query), variable_values=variables)  # type: ignore
    return result


def get_network_allocated_subgraphs(network: str) -> Set[str]:
    """Get the indexer's subgraph allocations for the given Graph network."""

    result = query_indexer_agent(
        """
        query ($protocolNetwork: String!) {
            indexerAllocations (protocolNetwork: $protocolNetwork) {
                subgraphDeployment
            }
        }
        """,
        variables={
            "protocolNetwork": network,
        },
    )

    return set(e["subgraphDeployment"] for e in result["indexerAllocations"])


def get_allocated_subgraphs() -> Set[str]:
    """
    Get the indexer's subgraph allocations for all Graph networks.

    Will try for both mainnet and arbitrum-one networks. If one of them fails, it
    will ignore it (happens if the indexer-agent is in single network mode).
    If both fail, it will raise the exception.
    """

    networks = ("mainnet", "arbitrum-one")
    results = []

    for network in networks:
        try:
            results += [get_network_allocated_subgraphs(network)]
        except TransportQueryError:
            logging.info(
                f"Failed to get indexer allocations for network '{network}'. Ignoring."
            )
            results += [None]

    if all(r is None for r in results):
        raise RuntimeError(
            f"Failed to query indexer allocations for all Graph networks: {networks}."
        )

    # Replace None's with empty set
    results = [r if r is not None else set() for r in results]

    return set.union(*results)
