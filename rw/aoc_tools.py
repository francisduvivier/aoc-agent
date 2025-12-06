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


def download_input(year: int, day: int, session_cookie: str, out_dir: str) -> str:
    url = f"{BASE}/{year}/day/{day}/input"
    cookies = {"session": session_cookie}
    r = requests.get(url, cookies=cookies, timeout=15)
    r.raise_for_status()
    out_path = Path(out_dir) / "input.txt"
    out_path.write_text(r.text)
    return str(out_path)


def generate_solver_with_openrouter(problem: str, input_sample: str, api_key: str, model: str = "tngtech/deepseek-r1t2-chimera:free") -> str:
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
        "You are a python coding assistant. Produce a Python script that reads 'input.txt' from the current working directory and prints the part 1 answer on the first line and the part 2 answer on the second line. "
        "Do not include explanations, only return the python source code. Keep solution concise and robust."
    )
    user_msg = f"Problem statement:\n{problem}\n\nProvide a python script that reads 'input.txt' and prints the part1 answer on the first line and the part2 answer on the second line. Use only standard library. Include necessary parsing." + ("\n\nInput sample:\n" + input_sample[:2000])
    payload = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user_msg}], "temperature": 0}
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


