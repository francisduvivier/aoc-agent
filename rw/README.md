Advent of Code Agent

Quickstart

1. Prerequisites
- Docker (or Podman) with "docker compose" support.
- Place a .env file at the project root (rw/.env) containing at minimum:
  - AOC_SESSION_COOKIE=YOUR_SESSION_VALUE   # value after "session=" from your AoC cookie
  - AOC_OPENROUTER_API_KEY=...             # optional, required if you want automatic solver generation

2. Run the agent
From the rw directory run:

  docker compose up --build --force-recreate --abort-on-container-exit --remove-orphans

This will build the container, fetch the current year's/day's problem and input, and write files to YEAR/dayNN/ (e.g. 2025/day02/).

Files created
- YEAR/dayNN/problem.txt  (cleaned problem text, with paragraphs preserved as newlines)
- YEAR/dayNN/input.txt    (puzzle input, with proper newlines)
- YEAR/dayNN/solution.py  (scaffold or generated solver)

Auto-run and submit behavior
- After fetching, the agent will try to run YEAR/dayNN/solution.py. If the script prints any non-empty lines, the first non-empty line is treated as the part 1 answer.
- The submit tool validates that the answer is non-empty and parses as a number before sending it to Advent of Code. Submissions use exponential backoff on rate limits.
- If YEAR/dayNN/solution.py produces no output, the agent will attempt to generate a solver using OpenRouter (model: grok-4.1-fast) when AOC_OPENROUTER_API_KEY is set and the container has network/DNS access.

Manual submit example

  docker compose run --rm agent python -c "import os; from aoc_tools import submit_solution; print(submit_solution(2025,2,1,'YOUR_ANSWER',os.environ.get('AOC_SESSION_COOKIE')))"

Notes
- The agent attempts to commit changes (git) on the mounted host volume; if git is not available inside the container, commits will be skipped and a warning logged.
- For OpenRouter-based generation to work the container must have outbound network/DNS access and a valid AOC_OPENROUTER_API_KEY in .env.
- Problem text extraction strips header/share/sponsor artifacts and preserves paragraph/newline structure.

If you want the agent to only generate candidate code and wait for approval before submitting, modify agent.py accordingly.
