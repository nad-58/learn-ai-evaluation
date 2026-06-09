# Changelog

All notable changes to this repository will be documented here.

The format follows a simple Keep a Changelog style and uses semantic versioning principles.

## [Unreleased]

### Planned

- Expand benchmark coverage with more public-safe synthetic examples
- Add optional integration examples for external evaluation platforms
- Add cross-version trend visualisation

## [1.1.0] - 2026-06-09

### Added

- Automated benchmark runner for the synthetic advanced AI benchmark
- Per-track aggregation for LLM, VLM, RAG, agentic AI, and system-level evaluation
- Equal-weight overall benchmark score
- CSV-based benchmark baseline and regression thresholds
- Absolute minimum-score checks and maximum allowed-drop checks
- JSON, CSV, and Markdown benchmark reports
- CI regression gate that fails when an acceptance threshold is breached
- GitHub Actions artifact upload for generated benchmark reports
- Unit tests for benchmark loading, aggregation, rule parsing, and pass/fail behaviour

### Changed

- Updated package version to 1.1.0
- Extended the validation workflow to run benchmark regression checks
- Added benchmark reports and regression thresholds to repository navigation

## [1.0.0] - 2026-06-09

### Added

- Complete seven-phase AI evaluation learning framework
- Classical ML, dataset, computer vision, technical medical AI, fairness, robustness, monitoring, and lifecycle evaluation
- Advanced evaluation for LLMs, VLMs, RAG systems, agentic AI, and combined systems
- Systematic LLM evaluation playbook covering code-based, human-based, and model-based evaluation
- Evaluator agreement, order-adjusted win rate, rubric scoring, and proxy-metric warning utilities
- Expanded VLM capability, hallucination, abstention, and rubric evaluation
- Synthetic public-safe benchmark covering prompt comparison, evaluator agreement, order effects, VLM hallucination, RAG retrieval, agent traces, and system-level evaluation
- Consolidated sample evaluation results
- Automated test suite and example validation runner
- GitHub Actions validation workflow
- Package build metadata and first stable package version

### Changed

- Improved README navigation and advanced evaluation documentation
- Updated package version to 1.0.0
- Added release-oriented validation of source compilation, tests, examples, and package metadata

## [0.1.0] - 2026-06-08

### Added

- Classical ML evaluation
- Dataset quality evaluation
- Computer vision evaluation
- Technical medical AI evaluation
- Group performance and robustness evaluation
- Monitoring and lifecycle evaluation
- Foundational LLM and VLM evaluation
- Reusable Python utilities, tutorials, templates, examples, and tests
