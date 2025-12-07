#!/bin/bash
# Wrapper to run the agent via docker compose
docker compose run --rm agent "$@"
