# Copyright 2022-, Semiotic AI, Inc.
# SPDX-License-Identifier: Apache-2.0

from typing import Set

import psycopg2
from more_itertools import flatten

from autoagora_processor.config import args


def get_indexed_subgraphs() -> Set[str]:
    conn = psycopg2.connect(
        dbname=args.graph_postgres_database,
        user=args.graph_postgres_username,
        password=args.graph_postgres_password,
        host=args.graph_postgres_host,
        port=args.graph_postgres_port,
    )
    cur = conn.cursor()

    cur.execute(
        """
        select
        d.deployment
        from subgraphs.subgraph_deployment as d,
        subgraphs.subgraph_deployment_assignment as a,
        subgraphs.subgraph_version as v,
        subgraphs.subgraph as g,
        ethereum_networks as n,
        deployment_schemas as s
        where g.id = v.subgraph
        and v.id in (g.pending_version, g.current_version)
        and a.id = s.id
        and s.id = d.id
        and v.deployment = d.deployment
        and n.name = s.network
        and not a.node_id = 'removed';
        """
    )

    return set(flatten(cur.fetchall()))
