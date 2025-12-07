# Things to improve

## Simple improvements

### Use Chat History Context
**Current:** The system constructs a new prompt for every retry, concatenating the problem, input, previous code, and feedback into a single user message.
**Plan:**
- Refactor `generate_solver_with_openrouter` to accept and maintain a list of `messages` (Conversation History).
- Instead of appending previous attempts to a single prompt, append a sequence of `{"role": "assistant", "content": code}` and `{"role": "user", "content": error_log}` to the message history.
- Ensure the context window does not overflow; implement a sliding window or summary strategy if the history exceeds token limits (though unlikely for single-file solutions).

### Robust Rate Limit Handling
**Current:** Returns failure or relies on simplistic user input on HTTP 429.
**Plan:**
- Implement a dedicated `BackoffStrategy` class in `aoc_tools.py`.
- If HTTP 429 is received, automatically engage exponential backoff (e.g., `sleep(base * 2^retries)`).
- Move the user interaction check outside the retry loop. If the user authorizes "auto-retry", the agent should persist in the backoff loop until success or a hard timeout (e.g., 10 minutes) without re-prompting.

### Persist and Block Previous Wrong Answers
**Current:** `submit.py` prevents rapid re-submission, but `agent.py` doesn't check validity before generation or execution.
**Plan:**
- Create a `solutions/{year}/day{day}/history.json` file.
- Structure: `{"part1": {"wrong_answers": [100, 200], "attempts": []}}`.
- Inside the main loop, after parsing the solution output:
    1. Check if the result is in `wrong_answers`.
    2. If yes, generate immediate negative feedback to the LLM ("You already calculated X, which is wrong. Try a different approach.") without executing the submission logic.
    3. If submission returns "That's not the right answer", append to `wrong_answers`.

### Automated Experimentation Framework
**Current:** No mechanism to compare model performance or parameter tuning.
**Plan:**
- Create `benchmark.py`.
- Define a configuration schema (JSON/YAML) to specify: `models`, `temperature_range`, `problem_set` (years/days).
- Implement a harness that runs `agent.py` logic in a loop, capturing:
    - Pass/Fail rate.
    - Number of retries to solve.
    - Cost (tokens used).
- output results to a CSV/Pandas dataframe for analysis.

### Controlled Code Variation
**Current:** Random temperature/top_p.
**Plan:**
- Decouple variation from random float generation.
- Implement `PromptStrategy` pattern.
- Inject variation via system prompts (e.g., "Act as a functional programmer", "Use iterative DFS", "Use recursion with memoization").
- Allow the agent to rotate through these strategies if the default approach fails repeatedly, ensuring semantic variation rather than just token probability variation.

### Static Analysis for Syntax Errors
**Current:** Relies on `subprocess` execution to catch `SyntaxError`, which consumes runtime overhead and looks like a logic error.
**Plan:**
- Import `ast` module.
- Before writing to file or executing, run `ast.parse(code_string)`.
- If `SyntaxError` is raised:
    - Catch it immediately in Python.
    - Create a specific log entry "Syntax Error Detected".
    - Feed the traceback back to the LLM immediately without attempting `subprocess.run`.

### Code Refactoring and Abstraction
**Current:** Monolithic `main()` function in `agent.py` with code duplication for Part 1, Part 2, and Verification.
**Plan:**
- Extract a `Solver` class.
- Method: `solve(part: int, mode: str) -> result`.
- Centralize logic for:
    - Fetching status.
    - Loop (Generate -> Execute -> Parse -> Submit).
    - Feedback loop management.
- Move regex parsing logic into a dedicated `OutputParser` static class to standardize how sample and final results are extracted.

### Mock AoC Server
**Current:** Integration tests require hitting live `adventofcode.com`.
**Plan:**
- Create a `MockAoCServer` class using `requests-mock` or `pytest-mock`.
- Intercept GET requests to `/{year}/day/{day}` and return static HTML files (stored in `tests/fixtures`).
- Intercept POST requests to `/answer` and return canned JSON responses for "Correct", "Too High", "Too Low".
- Allows testing the `agent.py` flow (parsing, file creation, status updates) without network calls.

### Mock LLM Interface
**Current:** Requires live OpenRouter API key and consumes credits.
**Plan:**
- Abstract `generate_solver_with_openrouter` behind an `LLMProvider` interface.
- Implement `MockLLMProvider`.
- Behavior: Returns pre-defined code snippets based on the input prompt (e.g., always returns `print("---- Final result Part 1: 42 ----")`).
- Use this to test the "Scaffold Verification" and "Output Parsing" logic deterministically.

## Hard improvements

### Parallel Multi-Agent Solving
**Current:** Serial execution.
**Plan:**
- Refactor `agent.py` to use `concurrent.futures.ThreadPoolExecutor`.
- Instantiate multiple `SolverAgent` workers (e.g., 3 workers).
- Each worker needs:
    - Unique scratchpad file (e.g., `solution_p1_worker_0.py`).
    - Distinct parameters (Worker A: High Temp, Worker B: Low Temp, Worker C: Python Expert Prompt).
- Implement a `SharedState` object (Thread-safe) to handle:
    - "First Solved" signal (cancellation token).
    - Submission lock (only one agent submits at a time).
- When one agent parses a valid result:
    1. Acquire lock.
    2. Submit.
    3. If correct, signal `Event` to cancel other threads.
    4. If incorrect, add to global blocklist and release lock.