#!/bin/bash

# 1. Activate the project virtual environment
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null

# 2. Execute the test suite
pytest

# 3. Return exit code 0 if all tests passed, or 1 if something went wrong.
exit $?