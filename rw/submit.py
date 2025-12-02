import time
import logging
import requests

BASE = "https://adventofcode.com"

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
