# adlc-kgs

[![Build status](https://img.shields.io/github/actions/workflow/status/atomobianco/adlc-kgs/main.yml?branch=main)](https://github.com/atomobianco/adlc-kgs/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/atomobianco/adlc-kgs)](https://img.shields.io/github/commit-activity/m/atomobianco/adlc-kgs)
[![License](https://img.shields.io/github/license/atomobianco/adlc-kgs)](https://img.shields.io/github/license/atomobianco/adlc-kgs)

Extracting RDF data from legal decisions.

## Context

This project is a proof of concept for extracting RDF data from legal decisions issued by the French competition authority, "Autorité de la concurrence".

Leveraging an agentic flow, it:

1. loads a text and an ontology;
2. asks LLM to extract RDF data that follows the given ontology;
3. asks LLM to verify and edit the extracted RDF, also using programmatic verification;
4. writes the final RDF data to a file.

## Getting started

First, install the environment

```bash
poetry install
```

Finally, run the main script with

```bash
poetry run python ./src/main.py
```
