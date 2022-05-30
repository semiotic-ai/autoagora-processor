# AutoAgora Processor

Processes raw `indexer-service` logs from a RabbitMQ queue, saves the results to a
PostgreSQL database.

The processing:

- Extracts details about query execution form the log lines: The subgraph deployment,
  timestamp, query, variables, execution time and fees paid.
- Normalizes the queries, separates the "query skeleton" from all values and variables.
- Saves the query skeleton (if never seen before), as well as a logs all the information
  about the query execution (including the variable values used).

Refer to [AutoAgora](https://gitlab.com/semiotic-ai/the-graph/autoagora) for more
details.
