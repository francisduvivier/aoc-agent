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
    """Fetch the problem page and return a cleaned plaintext of the statement.
    Attempts to extract the main <article class="day-desc"> block and preserve line breaks.
    Filters out sharing/sponsor/header artifacts.
    """
    url = f"{BASE}/{year}/day/{day}"
    cookies = {"session": session_cookie}
    r = requests.get(url, cookies=cookies, timeout=15)
    r.raise_for_status()
    text = r.text
    # remove scripts
    text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
    # Try to extract the first article.day-desc block which contains the problem description
    m = re.search(r'<article[^>]*class="[^"]*day-desc[^"]*"[^>]*>([\s\S]*?)</article>', text, flags=re.I)
    if m:
        text = m.group(1)
    # remove known unwanted tags/blocks
    text = re.sub(r"<current_datetime>[\s\S]*?</current_datetime>", "", text, flags=re.I)
    # replace block-level closing tags with newlines to preserve paragraphs
    text = re.sub(r"</(p|div|h[1-6]|li|pre)>", "\n", text, flags=re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    # remove share / social lines
    text = re.sub(r"You can also[\s\S]*?(?=<|$)", "", text, flags=re.I)
    # remove sponsors block if present
    text = re.sub(r"Our sponsors help make Advent of Code possible:[\s\S]*?(?=<|$)", "", text, flags=re.I)
    # strip all remaining tags
    clean = re.sub(r"<[^>]+>", "", text)
    # normalize line endings and collapse multiple blank lines
    clean = clean.replace('\r\n', '\n').replace('\r', '\n')
    clean = re.sub(r"\n[ \t]*\n+", "\n\n", clean)
    # Trim leading/trailing whitespace on each line
    clean = "\n".join([ln.rstrip() for ln in clean.splitlines()]).strip() + "\n"
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

    print("NOT POSTING")
    return
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


def generate_solver_with_openrouter(problem: str, input_sample: str, api_key: str, model: str = "x-ai/grok-4.1-fast:free") -> str:
    """Call OpenRouter's chat completions to generate a Python solver script.
    Returns the generated python code as a string (no surrounding ``` markers if possible).
    """
    base = "https://openrouter.ai/api/v1"
    url = base + "/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # optional extra headers from env to match OpenRouter client example
    referer = os.environ.get("AOC_OPENROUTER_REFERER")
    xtitle = os.environ.get("AOC_OPENROUTER_X_TITLE")
    if referer:
        headers["HTTP-Referer"] = referer
    if xtitle:
        headers["X-Title"] = xtitle

    system = (
        "You are a python coding assistant. Produce a Python script that reads 'input.txt' from the current working directory and prints the part 1 answer on the first line. "
        "Do not include explanations, only return the python source code. Keep solution concise and robust."
    )
    user_msg = f"Problem statement:\n{problem}\n\nProvide a python script that reads 'input.txt' and prints the part1 answer on the first line. Use only standard library. Include necessary parsing." + ("\n\nInput sample:\n" + input_sample[:2000])
    payload = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user_msg}], "temperature": 0}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            logging.warning("OpenRouter returned status %s: %s", r.status_code, r.text[:1000])
            return ""
        # parse json
        try:
            j = r.json()
        except Exception:
            logging.warning("OpenRouter returned non-json response: %s", r.text[:1000])
            return ""
        content = ""
        # OpenRouter responses: choices[0].message.content
        if isinstance(j, dict):
            choices = j.get("choices") or []
            if choices:
                # support both OpenAI and OpenRouter shapes
                msg = choices[0].get("message") or choices[0].get("delta") or choices[0]
                if isinstance(msg, dict):
                    content = msg.get("content") or msg.get("text") or ""
                else:
                    content = str(msg)
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
