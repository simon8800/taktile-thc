# Deploy Code to Taktile Code Nodes via Taktile Decision History API

This solution uses GitHub Actions and Taktile Decision History API to automate the deployment of python code to Code Nodes in your Organization's flows. Code changes are pushed to Taktile when changes are pushed to your GitHub repository's `main` branch.

## Problem Statement

How do we automate code changes to Taktile flows when using GitHub as a repository?

## Solution Overview

- **GitHub Repostory:** Stores Python code (`Multiply.py`, `Summarize.py`) that needs to be deployed to Taktile Code Nodes.
- **GitHub Actions Workflow:** Automates the deployment process pased on `push` and `pull_request` events to the `main` branch.
- **Python Script:** Contains the logic to use Taktile API for validating Flow, Node, and patching the Code Node with specified files.

## Prerequisites

You can simply fork this repository and make your edits.

* You need a Taktile API key.
* You need the Flow ID and Node ID of the target node in your Taktile decision graph.

## Setup

1. Add the secret `TAKTILE_API_KEY: <YOUR_TAKTILE_API_KEY>` to your GitHub Actions. [(Using Secrets in GitHub Actions)](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
2. In the `deploy_nodes.yml` workflow, set the environment variables `TAKTILE_FLOW_ID`, `TAKTILE_NODE_ID`, and `SRC_CODE_PATH_FILE` to reflect your Flow ID, Node ID, and path to the source code.

## How it Works

1. **Trigger:** When code is pushed into the `main` branch of your GitHub repository, the `deploy_nodes.yml` workflow is automatically triggered.
2. **Checkout Code:** The workflow looks at the latest version of your code.
3. **Set up Python:** A Python environment is set up and installs the `requests` library for API requests.
4. **Deploy Jobs:** The secrets and environment variables are passed into the Python script to call Taktile APIs.
	- Deployment status is printed in the workflow logs.

## Support

Please refer to the following resources for more information:

- [Taktile API docs](https://docs.taktile.com/)
- [GitHub Actions](https://github.com/features/actions)