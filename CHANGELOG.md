# Changelog

## [1.0.0](https://github.com/semiotic-ai/autoagora-processor/compare/v0.4.1...v1.0.0) (2023-10-30)


### ⚠ BREAKING CHANGES

* autoagora-processor needs to communicate with the indexer-agent API (--indexer-agent-mgmt-endpoint) instead of graph-node's PG DB (--graph-postgres-... args are gone).

### Bug Fixes

* Only load schemas for allocated subgraphs ([2a24173](https://github.com/semiotic-ai/autoagora-processor/commit/2a24173696fd46934a686536f0dff82d90fdd626)), closes [#33](https://github.com/semiotic-ai/autoagora-processor/issues/33)

## [0.4.1](https://github.com/semiotic-ai/autoagora-processor/compare/v0.4.0...v0.4.1) (2023-10-11)


### Bug Fixes

* update dependencies ([058847f](https://github.com/semiotic-ai/autoagora-processor/commit/058847f271e5ef2cc1f4e8521d06259a805188a8))
