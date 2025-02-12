# adlc-kgs

[![Build status](https://img.shields.io/github/actions/workflow/status/atomobianco/adlc-kgs/main.yml?branch=main)](https://github.com/atomobianco/adlc-kgs/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/atomobianco/adlc-kgs)](https://img.shields.io/github/commit-activity/m/atomobianco/adlc-kgs)
[![License](https://img.shields.io/github/license/atomobianco/adlc-kgs)](https://img.shields.io/github/license/atomobianco/adlc-kgs)

Extracting RDF data from legal decisions.

## Context

This project belongs to a research program aimed at extracting structured data from legal decisions issued by the French Competition Authority ("Autorité de la concurrence"), presented in the following venue:

> "Information Extraction for the Analysis of the French Competition Authority's Decisions Using Machine Learning" by Arnold Vialfont and Tommaso Bianco. Econom'IA Workshop 2024.

Using an agent-based workflow, this program:

1. Loads a text and an ontology
2. Uses LLM to extract RDF data that follows the given ontology
3. Uses LLM to verify and edit the extracted RDF, also using programmatic verification
4. Writes the final RDF data to a file

## Getting started

First, install the environment:

```bash
poetry install
```

Then, create a `.env` file with API keys for LLM providers the code will use.

Finally, run the main script with:

```bash
poetry run python ./src/main.py
```

Note that we use dependencies only compatible with python 3.11, so that you may need to create and activate a dedicated environment to run these two commands.
