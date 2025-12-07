# AoC Agent

An automated agent for solving Advent of Code puzzles using LLMs.

## Setup

1.  **Environment Variables**: Create a `.env` file in the root directory:
    ```bash
    AOC_SESSION_COOKIE=your_session_cookie
    AOC_OPENROUTER_API_KEY=your_openrouter_api_key
    ```

2.  **Docker**: Ensure Docker and Docker Compose are installed.

## Usage

Use the provided `go.sh` script to run the agent. This ensures it runs within the configured Docker environment.

### Basic Usage
Run the agent for the current day (UTC):
```bash
./go.sh
```

### Specific Date
Run for a specific year and day:
```bash
./go.sh --year 2023 --day 1
```

### Flags
-   `--fetch-only`: Only fetch the problem statement and input, and create the scaffold. Does not attempt to solve.
    ```bash
    ./go.sh --fetch-only
    ```
-   `--run-only`: Only run the existing solution/scaffold. Does not fetch input or problem statement. Useful for testing or retrying generation without hitting AoC servers.
    ```bash
    ./go.sh --run-only
    ```
-   `--auto-submit`: Automatically submit the answer if verification passes, without asking for confirmation.
    ```bash
    ./go.sh --auto-submit
    ```

## Development

-   **Scaffolds**: Templates for solutions are in `rw/templates/`.
-   **Agent Logic**: Main logic is in `rw/agent.py`.
-   **Tools**: Helper functions are in `rw/aoc_tools.py`.
