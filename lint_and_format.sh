#!/bin/bash

# Exit in case of error
# set -e

echo "Running Flake8 for linting..."
flake8 .

echo "Running Black for code formatting..."
black .

echo "Linting and formatting complete!"