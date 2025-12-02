#!/usr/bin/env python3
"""AoC agent scaffold: fetch problem, download input, submit answer, and commit changes.
"""
import os
import sys
import time
import argparse
import logging
import subprocess
from datetime import datetime
from aoc_tools import fetch_problem_statement, download_input, submit_solution, create_day_dir, git_commit

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main():
    parser = argparse.ArgumentParser(description="AoC agent scaffold")
    parser.add_argument("--year", type=int, default=datetime.utcnow().year)
    parser.add_argument("--day", type=int, default=datetime.utcnow().day)
    args = parser.parse_args()

    year = args.year
    day = args.day

    session = os.environ.get("AOC_SESSION_COOKIE")
    if not session:
        logging.error("AOC_SESSION_COOKIE environment variable not set (value after session=).")
        sys.exit(1)

    workdir = create_day_dir(year, day)

    logging.info("Fetching problem statement HTML and cleaning to text")
    stmt = fetch_problem_statement(year, day, session)
    with open(os.path.join(workdir, "problem.txt"), "w") as f:
        f.write(stmt)

    logging.info("Downloading puzzle input")
    inp_path = download_input(year, day, session, workdir)
    logging.info("Input saved to %s", inp_path)

    sample_answer = None
    # Example: run a sample solver if provided
    # The agent scaffold should create a sample solver file structure for the user to edit.
    sample_py = os.path.join(workdir, "solution.py")
    if not os.path.exists(sample_py):
        with open(sample_py, "w") as f:
            f.write("""# Edit this file: implement solve_part1 and solve_part2


def read_input(path):
    with open(path) as fh:
        return [line.strip() for line in fh]


def solve_part1(lines):
    # replace with actual solution
    return ""


def solve_part2(lines):
    return ""


if __name__ == '__main__':
    lines = read_input('input.txt')
    print(solve_part1(lines))
    print(solve_part2(lines))
""")
        logging.info("Wrote sample solver %s", sample_py)

    # git commit the new files so agent actions are recorded
    git_commit(f"Add AoC day {year}-{day} scaffold")

    # Try to run the day's solution to obtain answers and submit part 1 if produced
    try:
        proc = subprocess.run(["python3", "solution.py"], cwd=workdir, capture_output=True, text=True, timeout=30)
        out = proc.stdout or ""
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        if lines:
            part1_answer = lines[0]
            logging.info("Found part1 answer from solution.py: %s", part1_answer)
            res = submit_solution(year, day, 1, part1_answer, session)
            logging.info("Submit result: %s", res)
            git_commit(f"Submit AoC {year}-{day} part1")
        else:
            logging.info("No output from solution.py; not submitting")
    except Exception as e:
        logging.warning("Running solution.py or submission failed: %s", e)

    logging.info("Scaffold ready in %s. Use submit_solution() from aoc_tools to submit answers manually if needed.", workdir)


if __name__ == "__main__":
    main()
