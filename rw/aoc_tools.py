"""Helper utilities for Advent of Code agent: fetching problem, input, and submitting answers.
"""
import os
import time
import logging
import re
import requests
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO)

BASE = "https://adventofcode.com"


def create_day_dir(year: int, day: int) -> str:
    path = Path(f"{year}/day{int(day):02d}")
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def fetch_problem_statement(year: int, day: int, session_cookie: str) -> str:
    """Fetch the problem page and return a crude plaintext of the statement."""
    url = f"{BASE}/{year}/day/{day}"
    cookies = {"session": session_cookie}
    r = requests.get(url, cookies=cookies, timeout=15)
    r.raise_for_status()
    text = r.text
    # Strip HTML tags simply
    clean = re.sub(r"<script[\s\S]*?</script>", "", text)
    clean = re.sub(r"<[^>]+>", "", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def download_input(year: int, day: int, session_cookie: str, out_dir: str) -> str:
    url = f"{BASE}/{year}/day/{day}/input"
    cookies = {"session": session_cookie}
    r = requests.get(url, cookies=cookies, timeout=15)
    r.raise_for_status()
    out_path = Path(out_dir) / "input.txt"
    out_path.write_text(r.text)
    return str(out_path)


def submit_solution(year: int, day: int, part: int, answer: str, session_cookie: str, max_attempts: int = 5) -> dict:
    """Submit an answer with exponential backoff. Logs request and response.
    Verifies answer is non-empty and numeric before submitting.
    Returns dict with keys: success(bool), message(str), status_code(int)
    """
    answer_str = str(answer).strip()
    if not answer_str:
        logging.warning("Empty answer provided; not submitting.")
        return {"success": False, "message": "Empty answer; not submitted", "status_code": None}
    # Ensure the answer parses as a number
    try:
        _ = int(answer_str)
    except ValueError:
        try:
            _ = float(answer_str)
        except ValueError:
            logging.warning("Answer does not parse as a number; not submitting.")
            return {"success": False, "message": "Answer not numeric; not submitted", "status_code": None}

    url = f"{BASE}/{year}/day/{day}/answer"
    cookies = {"session": session_cookie}
    data = {"level": str(part), "answer": answer_str}

    attempt = 0
    wait = 1
    while attempt < max_attempts:
        attempt += 1
        logging.info("Submitting attempt %d for %s/%s part %s", attempt, year, day, part)
        r = requests.post(url, cookies=cookies, data=data, timeout=15)
        # Log request/response (avoid printing full session cookie)
        logging.info("POST %s status=%s", url, r.status_code)
        body = r.text
        # check common AoC messages
        if "That's not the right answer" in body or "not the right answer" in body:
            message = "Incorrect answer"
            logging.warning(message)
            return {"success": False, "message": message, "status_code": r.status_code}
        if "You gave an answer too recently" in body or "too recently" in body:
            message = "Rate limited, backing off"
            logging.warning(message)
            time.sleep(wait)
            wait *= 2
            continue
        if r.status_code == 200:
            # Could be correct or other; attempt to detect success
            if "That's the right answer" in body or "right answer" in body:
                logging.info("Correct answer")
                return {"success": True, "message": "Correct", "status_code": r.status_code}
            # otherwise return raw body snippet
            snippet = body[:200]
            logging.info("Response: %s", snippet)
            return {"success": True, "message": snippet, "status_code": r.status_code}
        # on other status codes back off
        logging.warning("Unexpected status %s, backing off", r.status_code)
        time.sleep(wait)
        wait *= 2
    return {"success": False, "message": "Max attempts reached", "status_code": None}


def generate_solver_with_openrouter(problem: str, input_sample: str, api_key: str, model: str = "grok-4.1-fast") -> str:
    """Call OpenRouter's chat completions to generate a Python solver script.
    Returns the generated python code as a string (no surrounding ``` markers if possible).
    """
    url = "https://api.openrouter.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    system = (
        "You are a python coding assistant. Produce a Python script that reads 'input.txt' from the current working directory and prints the part 1 answer on the first line. "
        "Do not include explanations, only return the python source code. Keep solution concise and robust."
    )
    user_msg = f"Problem statement:\n{problem}\n\nProvide a python script that reads 'input.txt' and prints the part1 answer on the first line. Use only standard library. Include necessary parsing." + ("\n\nInput sample:\n" + input_sample[:2000])
    payload = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user_msg}], "temperature": 0}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        j = r.json()
        content = ""
        # OpenRouter responses: choices[0].message.content
        if isinstance(j, dict):
            choices = j.get("choices") or []
            if choices:
                content = choices[0].get("message", {}).get("content", "")
        # extract code block if present
        m = re.search(r"```(?:python)?\n([\s\S]*?)```", content)
        code = m.group(1) if m else content
        return code
    except Exception as e:
        logging.warning("OpenRouter code generation failed: %s", e)
        return ""


def git_commit(message: str):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        logging.info("Committed changes: %s", message)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.warning("Git not available or commit failed (git may be missing in container or nothing to commit)")
