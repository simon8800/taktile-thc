# Deploy Code to Taktile Code Nodes via Taktile Decision History API

This solution uses GitHub Actions and Taktile Decision History API to automate the deployment of python code to Code Nodes in your Organization's flows.

Code changes are pushed to Taktile when changes are pushed to your GitHub repository's `main` branch.

## Prerequisites

* You need a Taktile API key
* You need the Flow ID and Node ID of the target node in your Taktile decision graph.

## Usage

### Setup

1. Add the secret `TAKTILE_API_KEY: <YOUR_TAKTILE_API_KEY>` to your GitHub Actions. [(Using Secrets in GitHub Actions)](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
2. In the `deploy_nodes.yml` workflow, adjust `TAKTILE_FLOW_ID`, `TAKTILE_NODE_ID`, and `SRC_CODE_PATH_FILE` to reflect your Flow ID, Node ID, and path to the source code.