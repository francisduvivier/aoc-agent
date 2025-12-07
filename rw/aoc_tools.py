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
    path = Path(f"solutions/{year}/day{int(day):02d}")
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def fetch_problem_statement(year: int, day: int, session_cookie: str) -> str:
    """Fetch the problem page and return a cleaned plaintext of the statement.
    Attempts to extract the main <article class="day-desc"> block and preserve line breaks.
    Filters out sharing/sponsor/header artifacts.
    """
    url = f"{BASE}/{year}/day/{day}"
    cookies = {"session": session_cookie}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; aoc-agent/1.0)"}
    r = requests.get(url, cookies=cookies, headers=headers, timeout=15)
    r.raise_for_status()
    text = r.text
    # remove scripts
    text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
    # Try to extract all article.day-desc blocks (part 1 and part 2) which contain the problem descriptions
    matches = re.findall(r'<article[^>]*class="[^\"]*day-desc[^\"]*"[^>]*>([\s\S]*?)</article>', text, flags=re.I)
    if matches:
        text = "\n\n".join(matches)
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


def fetch_puzzle_status(year: int, day: int, session_cookie: str) -> dict:
    """Fetch the problem page and determine which parts are solved.
    Returns a dict: {'part1_solved': bool, 'part1_answer': str|None, 'part2_solved': bool, 'part2_answer': str|None}
    """
    url = f"{BASE}/{year}/day/{day}"
    cookies = {"session": session_cookie}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; aoc-agent/1.0)"}
    r = requests.get(url, cookies=cookies, headers=headers, timeout=15)
    r.raise_for_status()
    text = r.text

    status = {
        'part1_solved': False,
        'part1_answer': None,
        'part2_solved': False,
        'part2_answer': None
    }

    # Check for "Your puzzle answer was" blocks
    # Usually: <p>Your puzzle answer was <code>ANSWER</code>.</p>
    # If both are solved, there are two such blocks. The first one is part 1, second is part 2.
    # However, the page structure might be complex.
    # Let's look for the specific pattern.
    
    answers = re.findall(r"Your puzzle answer was <code>(.*?)</code>", text)
    
    if len(answers) >= 1:
        status['part1_solved'] = True
        status['part1_answer'] = answers[0]
    
    if len(answers) >= 2:
        status['part2_solved'] = True
        status['part2_answer'] = answers[1]
        
    return status


def download_input(year: int, day: int, session_cookie: str, out_dir: str) -> str:
    url = f"{BASE}/{year}/day/{day}/input"
    cookies = {"session": session_cookie}
    r = requests.get(url, cookies=cookies, timeout=15)
    r.raise_for_status()
    out_path = Path(out_dir) / "input.txt"
    out_path.write_text(r.text)
    return str(out_path)

# kwaipilot/kat-coder-pro:free
# tngtech/deepseek-r1t2-chimera:free
def generate_solver_with_openrouter(problem: str, input_sample: str, api_key: str, model: str = "tngtech/deepseek-r1t2-chimera:free", part: int = 1, previous_code: str = None, feedback: str = None) -> str:
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
        f"You are a python coding assistant. Produce a Python script that reads 'input.txt' from the current working directory and prints the part {part} answer. "
        "Do not include explanations, only return the python source code. Keep solution concise and robust."
    )
    user_msg = f"Problem statement:\n{problem}\n\nProvide a python script that reads 'input.txt' and prints the part {part} answer. Use only standard library. Include necessary parsing.\n" + \
               f"IMPORTANT: You MUST fill in the 'sample_input' and 'sample_answer' variables in the scaffold with data from the problem statement. " + \
               f"Uncomment the assertion line and ensure the test run passes. 'sample_answer' might be an integer or string." + ("\n\nInput sample:\n" + input_sample[:2000])
    
    if previous_code and feedback:
        user_msg += f"\n\nPrevious attempt failed:\n```python\n{previous_code}\n```\nFeedback: {feedback}\nPlease fix the code."
    payload = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user_msg}], "temperature": 0.5, "top_p": 0.9}
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    RESET = '\033[0m'
    logging.info(f"{YELLOW}OpenRouter REQUEST payload:{RESET}\n{payload}")
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            logging.warning(f"{CYAN}OpenRouter returned status {r.status_code}: {r.text[:1000]}{RESET}")
            return ""
        # parse json
        try:
            j = r.json()
        except Exception:
            logging.warning(f"{CYAN}OpenRouter returned non-json response: {r.text[:1000]}{RESET}")
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
        logging.info(f"{CYAN}OpenRouter RESPONSE:{RESET}\n{content}")
        return code
    except Exception as e:
        logging.warning(f"{CYAN}OpenRouter code generation failed: {e}{RESET}")
        return ""



def git_commit(paths: list[str], message: str) -> bool:
    """Stage the given paths and commit with the message."""
    if not paths:
        return False
    try:
        subprocess.run(["git", "add"] + paths, check=True, capture_output=True)
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"] + paths, capture_output=True, text=True)
        if not status.stdout.strip():
            logging.info("No changes to commit for %s", paths)
            return False
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        logging.info("Committed changes to %s with message: %s", paths, message)
        return True
    except subprocess.CalledProcessError as e:
        logging.warning("Git commit failed: %s", e)
        return False
