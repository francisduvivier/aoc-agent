import time
import logging
import requests
import json
from pathlib import Path
from datetime import datetime, timedelta

BASE = "https://adventofcode.com"
ATTEMPT_FILE = Path(__file__).resolve().parent / ".submit_attempts.json"


def _load_attempts():
    if not ATTEMPT_FILE.exists():
        return {}
    try:
        return json.loads(ATTEMPT_FILE.read_text())
    except Exception:
        return {}


def _save_attempts(d):
    try:
        ATTEMPT_FILE.write_text(json.dumps(d))
    except Exception as e:
        logging.warning("Failed to write attempts file: %s", e)


def submit_solution(year: int, day: int, part: int, answer: str, session_cookie: str, max_attempts: int = 3) -> dict:
    """Submit an answer but enforce agent-side limits stored in .submit_attempts.json.
    Allows up to `max_attempts` with at least 60 seconds between tries. Records attempts and blocks further tries.
    """
    answer_str = str(answer).strip()
    if not answer_str:
        logging.warning("Empty answer provided; not submitting.")
        return {"success": False, "message": "Empty answer; not submitted", "status_code": None}

    key = f"{year}-{day}-{part}"
    attempts = _load_attempts()
    rec = attempts.get(key, {"count": 0, "last": None})
    now = datetime.utcnow()
    if rec.get("count", 0) >= max_attempts:
        logging.warning("Submission blocked: max attempts reached for %s", key)
        return {"success": False, "message": "Blocked: max attempts reached", "status_code": None}
    if rec.get("last"):
        try:
            last = datetime.fromisoformat(rec["last"].replace("Z", "+00:00"))
            if now - last < timedelta(seconds=60):
                logging.warning("Submission blocked: last attempt was less than 60s ago for %s", key)
                return {"success": False, "message": "Blocked: try later", "status_code": None}
        except Exception:
            pass

    url = f"{BASE}/{year}/day/{day}/answer"
    cookies = {"session": session_cookie}
    data = {"level": str(part), "answer": answer_str}

    # Record this attempt before firing to prevent concurrent repeat
    rec["count"] = rec.get("count", 0) + 1
    rec["last"] = now.isoformat() + "Z"
    attempts[key] = rec
    _save_attempts(attempts)

    logging.info("Submitting attempt %d for %s/%s part %s", rec["count"], year, day, part)
    try:
        r = requests.post(url, cookies=cookies, data=data, timeout=15)
    except Exception as e:
        logging.warning("Submission POST failed: %s", e)
        return {"success": False, "message": str(e), "status_code": None}

    logging.info("POST %s status=%s", url, r.status_code)
    body = r.text

    # Interpret response
    if "That's not the right answer" in body or "not the right answer" in body:
        logging.warning("Incorrect answer")
        # mark as blocked to prevent further tries
        rec["count"] = max_attempts
        rec["last"] = now.isoformat() + "Z"
        attempts[key] = rec
        _save_attempts(attempts)
        return {"success": False, "message": "Incorrect answer", "status_code": r.status_code}
    if "You gave an answer too recently" in body or "too recently" in body:
        logging.warning("Rate limited by AoC: too recently")
        return {"success": False, "message": "Rate limited", "status_code": r.status_code}
    if r.status_code == 200:
        if "That's the right answer" in body or "right answer" in body:
            logging.info("Correct answer")
            # clear attempts record on success
            if key in attempts:
                del attempts[key]
                _save_attempts(attempts)
            return {"success": True, "message": "Correct", "status_code": r.status_code}
        # Ambiguous 200 response
        snippet = body[:1000]
        logging.warning("Ambiguous 200 response from AoC; treating as failure. Snippet: %s", snippet)
        return {"success": False, "message": snippet, "status_code": r.status_code}

    logging.warning("Unexpected status %s", r.status_code)
    return {"success": False, "message": "Unexpected status", "status_code": r.status_code}
