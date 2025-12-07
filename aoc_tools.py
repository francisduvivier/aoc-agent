"""Helper utilities for Advent of Code agent: fetching problem, input, and submitting answers.
"""
import os
import time
import logging
import re
import requests
import subprocess
import sys
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


def check_accepted_files(workdir: str) -> dict | None:
    """Check for accepted_part{1,2}.txt files in the work directory.
    Returns a status dict if any accepted files are found, else None.
    """
    p1_file = os.path.join(workdir, "accepted_part1.txt")
    p2_file = os.path.join(workdir, "accepted_part2.txt")
    
    status = {
        'part1_solved': False,
        'part1_answer': None,
        'part2_solved': False,
        'part2_answer': None
    }
    
    found_any = False
    
    if os.path.exists(p1_file):
        try:
            status['part1_answer'] = open(p1_file).read().strip()
            status['part1_solved'] = True
            found_any = True
        except Exception:
            pass
            
    if os.path.exists(p2_file):
        try:
            status['part2_answer'] = open(p2_file).read().strip()
            status['part2_solved'] = True
            found_any = True
        except Exception:
            pass
            
    return status if found_any else None


    return status if found_any else None


def download_input(year: int, day: int, session_cookie: str, out_dir: str) -> str:
    url = f"{BASE}/{year}/day/{day}/input"
    cookies = {"session": session_cookie}
    r = requests.get(url, cookies=cookies, timeout=15)
    r.raise_for_status()
    out_path = Path(out_dir) / "input.txt"
    out_path.write_text(r.text)
    return str(out_path)


def check_pricing(model: str) -> bool:
    return True # TODO: decide what to do with this
    """Check if the model's pricing is within the limit (0.0001 per 1M tokens)."""
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        r.raise_for_status()
        data = r.json()
        for m in data.get("data", []):
            if m.get("id") == model:
                pricing = m.get("pricing", {})
                prompt = float(pricing.get("prompt", 0)) * 1_000_000
                completion = float(pricing.get("completion", 0)) * 1_000_000
                
                # Limit: 0.0001 per 1M tokens
                limit = 0.0001
                if prompt > limit or completion > limit:
                    logging.warning(f"Model {model} pricing too high: Prompt=${prompt:.6f}/1M, Completion=${completion:.6f}/1M. Limit=${limit}/1M.")
                    return False
                return True
        logging.warning(f"Model {model} not found in pricing list. Proceeding with caution.")
        return True
    except Exception as e:
        logging.warning(f"Failed to check pricing: {e}. Proceeding.")
        return True


# kwaipilot/kat-coder-pro:free
# tngtech/deepseek-r1t2-chimera:free
# deepseek/deepseek-chat-v3.1
def generate_solver_with_openrouter(problem: str, input_sample: str, api_key: str, model: str = "kwaipilot/kat-coder-pro:free", part: int = 1, previous_code: str = None, feedback: str = None) -> str:
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
                f"IMPORTANT: You are encouraged to include reasoning and debug output in your solution in case of errors.\n" + \
                f"IMPORTANT: You MUST fill in the 'samples' list with (sample_input, expected_result) tuples extracted from the problem statement.\n" + \
                f"IMPORTANT: The script MUST iterate over the 'samples' list, assert each sample result, and print each sample solution using the format '---- Sample {{idx}} Solution Part {part}: {{sample_res}} ----'.\n" + ("\n\nInput sample[:100]...[-100:]" + input_sample[:100]+"..."+input_sample[-max(0,min(100, len(input_sample)-1000)):])
    
    if previous_code and feedback:
        user_msg += f"\n\nPrevious attempt failed:\n```python\n{previous_code}\n```\nFeedback: {feedback}\nPlease fix the code."
    payload = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user_msg}], "temperature": 0.01, "top_p": 0.01}
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    RESET = '\033[0m'
    logging.info(f"{YELLOW}OpenRouter REQUEST payload:{RESET}\n{payload}")
    
    if not check_pricing(model):
        logging.error("Pricing check failed. Request skipped.")
        return ""

    max_retries = 3
    retry_delay = 5
    user_approved_retry = False

    for attempt in range(max_retries + 1):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            if r.status_code == 429:
                logging.warning(f"{CYAN}OpenRouter Rate Limit (429).{RESET}")
                if not user_approved_retry:
                    # Ask user if they want to wait/retry
                    # If auto-submit is on, maybe we assume yes? But user said "ask user interaction"
                    # We'll use input() if interactive
                    if sys.stdin and sys.stdin.isatty():
                        try:
                            resp = input("Rate limited. Continue and retry? (y/N): ").strip().lower()
                            if resp in ("y", "yes"):
                                user_approved_retry = True
                            else:
                                logging.error("User cancelled retry.")
                                return ""
                        except Exception:
                            logging.warning("Failed to read input. Aborting.")
                            return ""
                    else:
                         # Non-interactive: log and fail, or maybe wait?
                         # User said "if user interaction was requested and approved, it should never be rate limited"
                         # which implies we should handle it. But without interaction, we can't ask.
                         # Let's just log and fail for now if non-interactive.
                         logging.error("Rate limited in non-interactive mode. Aborting.")
                         return ""
                
                # If we are here, user approved (or we are retrying)
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2 # Exponential backoff
                continue

            try:
                r.raise_for_status()
            except requests.HTTPError:
                logging.warning(f"{CYAN}OpenRouter returned status {r.status_code}: {r.text}{RESET}")
                return ""
            break # Success
        except Exception as e:
             logging.warning(f"{CYAN}Request failed: {e}{RESET}")
             return ""
    else:
        logging.error("Max retries exceeded.")
        return ""

    # parse json
    try:
        j = r.json()
    except Exception:
        logging.warning(f"{CYAN}OpenRouter returned non-json response: {r.text}{RESET}")
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
    
    usage = j.get("usage", {})
    if usage:
        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
        total_tokens = usage.get("total_tokens")
        logging.info(f"Token Usage: Prompt={prompt_tokens}, Completion={completion_tokens}, Total={total_tokens}")

    logging.info(f"{CYAN}OpenRouter RESPONSE:{RESET}\n{content}")
    return code



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
