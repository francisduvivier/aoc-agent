# Antigravity Agent Instructions

## Operational Rules

1.  **Execution Environment**:
    - Always use `./go.sh` to run the agent. This wraps `docker compose run --rm agent`.
    - Do not run `python agent.py` directly unless debugging outside the container context.

2.  **Timezone**:
    - Advent of Code unlocks at midnight EST (UTC-5). Ensure all date/time calculations use this timezone.

3.  **Network & API Usage**:
    - **Pricing Check**: Before calling OpenRouter, check that the model's pricing is below $0.0001 per 1M tokens.
    - **Token Logging**: Log `prompt_tokens`, `completion_tokens`, and `total_tokens` for every API response.
    - **Rate Limiting**: Implement exponential backoff for 429 errors. In interactive mode, ask for user confirmation before retrying.

4.  **Solution Management & Caching**:
    - **Output Format**: Solutions must print results using explicit markers:
        ```text
        ---- Sample Solution Part X: [result] ----
        ---- Final Solution Part X: [result] ----
        ```
    - **Caching**: Upon a successful submission (accepted answer), write the answer to `accepted_part{part}.txt` in the day's directory and commit it.
    - **Status Checking**:
        - **Primary Source**: Check for `accepted_part{1,2}.txt`. If present, consider the part solved.
        - **Secondary Source**: Use `fetch_puzzle_status` (AoC API) if local files are missing.
        - **Forbidden**: Do **NOT** parse `problem.txt` to determine solved status.
    - **Skip Fetching**: If local files indicate the current part is solved, skip fetching the problem statement and input to save network requests.

5.  **Git Integration**:
    - Commit the solutions directory after fetching input.
    - Commit the solution file and accepted answer file after a successful solve.

6.  **Problem Text**:
    - When fetching the problem statement, ensure "Your puzzle answer was..." lines are included in the text (if available) to keep `problem.txt` complete, even though we don't parse it for status.
