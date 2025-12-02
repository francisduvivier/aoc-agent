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
from aoc_tools import fetch_problem_statement, download_input, submit_solution, create_day_dir, git_commit, generate_solver_with_openrouter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main():
    parser = argparse.ArgumentParser(description="AoC agent scaffold")
    parser.add_argument("--year", type=int, default=datetime.utcnow().year)
    parser.add_argument("--day", type=int, default=datetime.utcnow().day)
    parser.add_argument("--fetch-only", action="store_true", help="Only fetch problem and input and create scaffold")
    parser.add_argument("--run-only", action="store_true", help="Only run existing scaffold/solution and attempt submission; do not fetch")
    parser.add_argument("--auto-submit", action="store_true", help="Automatically submit answers without prompting")
    args = parser.parse_args()

    year = args.year
    day = args.day

    # Allow explicit env override for compose systems that don't forward args reliably
    env_run_only = os.environ.get("AGENT_RUN_ONLY")
    env_fetch_only = os.environ.get("AGENT_FETCH_ONLY")
    if env_run_only and env_run_only.lower() in ("1", "true", "yes"):
        args.run_only = True
    if env_fetch_only and env_fetch_only.lower() in ("1", "true", "yes"):
        args.fetch_only = True

    # auto-submit can be enabled by flag or env
    auto_submit = args.auto_submit or (os.environ.get("AOC_AUTO_SUBMIT", "").lower() in ("1", "true", "yes"))

    session = os.environ.get("AOC_SESSION_COOKIE")
    if not session:
        logging.error("AOC_SESSION_COOKIE environment variable not set (value after session=).")
        sys.exit(1)

    workdir = create_day_dir(year, day)

    # validate flags
    if args.fetch_only and args.run_only:
        logging.error("Cannot use --fetch-only and --run-only together")
        sys.exit(1)

    do_fetch = not args.run_only
    do_run = not args.fetch_only

    def _should_submit_interactive(answer: str, part: int = 1) -> bool:
        if auto_submit:
            return True
        # non-interactive: skip unless auto_submit
        if not sys.stdin or not sys.stdin.isatty():
            logging.info("Non-interactive shell and auto-submit not enabled; skipping submission")
            return False
        try:
            resp = input(f"Submit part{part} answer '{answer}' for {year}-{day}? (y/N): ").strip().lower()
            return resp in ("y", "yes")
        except Exception as e:
            logging.warning("Failed to read confirmation: %s", e)
            return False

    if do_fetch:
        logging.info("Fetching problem statement HTML and cleaning to text")
        stmt = fetch_problem_statement(year, day, session)
        with open(os.path.join(workdir, "problem.txt"), "w") as f:
            f.write(stmt)

        logging.info("Downloading puzzle input")
        inp_path = download_input(year, day, session, workdir)
        logging.info("Input saved to %s", inp_path)

        # create scaffold if not exists
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

    if do_run:
        # ensure workdir has input and problem
        if not os.path.exists(os.path.join(workdir, "input.txt")):
            logging.error("input.txt not found in %s. Run with --fetch-only first.", workdir)
            sys.exit(1)
        if not os.path.exists(os.path.join(workdir, "problem.txt")):
            logging.error("problem.txt not found in %s. Run with --fetch-only first.", workdir)
            sys.exit(1)

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
                if len(lines) > 1:
                    part2_answer = lines[1]
                    logging.info("Found part2 answer from solution.py: %s", part2_answer)
                    res2 = submit_solution(year, day, 2, part2_answer, session)
                    logging.info("Submit result: %s", res2)
                    git_commit(f"Submit AoC {year}-{day} part2")
            else:
                logging.info("No output from solution.py; attempting to generate solver via OpenRouter")
                api_key = os.environ.get("AOC_OPENROUTER_API_KEY")
                if not api_key:
                    logging.warning("AOC_OPENROUTER_API_KEY not set; cannot generate solver")
                else:
                    try:
                        problem_txt = open(os.path.join(workdir, "problem.txt"), "r").read()
                        input_txt = open(os.path.join(workdir, "input.txt"), "r").read()
                        code = generate_solver_with_openrouter(problem_txt, input_txt, api_key)
                        if code:
                            with open(os.path.join(workdir, "solution.py"), "w") as sf:
                                sf.write(code)
                            logging.info("Wrote generated solver to %s", os.path.join(workdir, "solution.py"))
                            proc2 = subprocess.run(["python3", "solution.py"], cwd=workdir, capture_output=True, text=True, timeout=60)
                            out2 = proc2.stdout or ""
                            lines2 = [l.strip() for l in out2.splitlines() if l.strip()]
                            if lines2:
                                part1_answer = lines2[0]
                                logging.info("Found part1 answer from generated solver: %s", part1_answer)
                                if _should_submit_interactive(part1_answer, 1):
                                    res = submit_solution(year, day, 1, part1_answer, session)
                                    logging.info("Submit result: %s", res)
                                    git_commit(f"Submit AoC {year}-{day} part1 (generated)")
                                else:
                                    logging.info("Submission skipped for generated part1 answer: %s", part1_answer)
                                if len(lines2) > 1:
                                    part2_answer = lines2[1]
                                    logging.info("Found part2 answer from generated solver: %s", part2_answer)
                                    if _should_submit_interactive(part2_answer, 2):
                                        res2 = submit_solution(year, day, 2, part2_answer, session)
                                        logging.info("Submit result: %s", res2)
                                        git_commit(f"Submit AoC {year}-{day} part2 (generated)")
                                    else:
                                        logging.info("Submission skipped for generated part2 answer: %s", part2_answer)
                            else:
                                logging.info("Generated solver produced no output; not submitting")
                        else:
                            logging.info("No code generated by OpenRouter")
                    except Exception as e:
                        logging.warning("Error during generation or run: %s", e)
        except Exception as e:
            logging.warning("Running solution.py or submission failed: %s", e)

    logging.info("Scaffold ready in %s. Use submit_solution() from aoc_tools to submit answers manually if needed.", workdir)


if __name__ == "__main__":
    main()
