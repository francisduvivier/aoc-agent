#!/usr/bin/env python3
"""AoC agent scaffold: fetch problem, download input, submit answer, and commit changes.
"""
import os
import sys
import time
import argparse
import logging
import subprocess
import re
from datetime import datetime, timezone, timedelta
from aoc_tools import fetch_problem_statement, download_input, create_day_dir, generate_solver_with_openrouter, git_commit, fetch_puzzle_status, check_accepted_files
from submit import submit_solution

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main():
    parser = argparse.ArgumentParser(description="AoC agent scaffold")
    # AoC unlocks at midnight EST (UTC-5)
    est = timezone(timedelta(hours=-5))
    parser.add_argument("--year", type=int, default=datetime.now(est).year)
    parser.add_argument("--day", type=int, default=datetime.now(est).day)
    parser.add_argument("--fetch-only", action="store_true", help="Only fetch problem and input and create scaffold")
    parser.add_argument("--run-only", action="store_true", help="Only run existing scaffold/solution and attempt submission; do not fetch")
    parser.add_argument("--auto-submit", action="store_true", help="Automatically submit answers without prompting")
    parser.add_argument("--model", type=str, default="kwaipilot/kat-coder-pro:free", help="Model to use for solving")

    args = parser.parse_args()

    year = args.year
    day = args.day
    model = args.model

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
        # Check if problem.txt already exists and has Part 2 answer
        accepted_status = check_accepted_files(workdir)
        
        if accepted_status and accepted_status['part2_solved']:
            logging.info("Local files indicate Part 2 is solved. Skipping fetch.")
        else:
            logging.info("Fetching problem statement HTML and cleaning to text")
            stmt = fetch_problem_statement(year, day, session)
            with open(os.path.join(workdir, "problem.txt"), "w") as f:
                f.write(stmt)

        logging.info("Downloading puzzle input")
        inp_path = download_input(year, day, session, workdir)
        logging.info("Input saved to %s", inp_path)
        git_commit([workdir], f"Fetch input for {year} day {day}")

        # create scaffold if not exists
        # We now use separate files for part 1 and part 2
        sol1 = os.path.join(workdir, "solution_part1.py")
        sol2 = os.path.join(workdir, "solution_part2.py")
        
        # Load templates
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        with open(os.path.join(template_dir, "scaffold_part1.py")) as f:
            scaffold1 = f.read()
        with open(os.path.join(template_dir, "scaffold_part2.py")) as f:
            scaffold2 = f.read()
        
        if not os.path.exists(sol1):
            with open(sol1, "w") as f:
                f.write(scaffold1)
            logging.info("Wrote sample solver %s", sol1)

        if not os.path.exists(sol2):
            with open(sol2, "w") as f:
                f.write(scaffold2)
            logging.info("Wrote sample solver %s", sol2)


    if do_run:
        # ensure workdir has input and problem
        if not os.path.exists(os.path.join(workdir, "input.txt")):
            logging.error("input.txt not found in %s. Run with --fetch-only first.", workdir)
            sys.exit(1)
        
        # Check puzzle status
        # Check puzzle status
        # status = parse_problem_file(os.path.join(workdir, "problem.txt")) # Removed as unreliable
        status = None
        accepted_status = check_accepted_files(workdir)
        
        if accepted_status:
            logging.info("Using local accepted files: %s", accepted_status)
            if status:
                # Merge status, preferring accepted files for solved status
                if accepted_status['part1_solved']:
                    status['part1_solved'] = True
                    status['part1_answer'] = accepted_status['part1_answer']
                if accepted_status['part2_solved']:
                    status['part2_solved'] = True
                    status['part2_answer'] = accepted_status['part2_answer']
            else:
                status = accepted_status
        
        if status and status['part2_solved']: # If part2_solved, then part1 must also be solved.
            logging.info("Using local status from accepted files: %s", status)
        else:
            status = fetch_puzzle_status(year, day, session)
            logging.info("Puzzle status from AoC: %s", status)

        api_key = os.environ.get("AOC_OPENROUTER_API_KEY")
        
        # --- PART 1 ---
        if not status['part1_solved']:
            logging.info("Part 1 not solved. Attempting to solve...")
            sol1 = os.path.join(workdir, "solution_part1.py")
            
            max_retries = 10
            feedback = None
            previous_code = None
            
            for attempt in range(1, max_retries + 1):
                logging.info("Part 1 Attempt %d/%d", attempt, max_retries)
                output = None
                
                
                # Reset to scaffold on fresh start
                if attempt == 1 and not feedback:
                    # Load template again to be sure
                    template_dir = os.path.join(os.path.dirname(__file__), "templates")
                    with open(os.path.join(template_dir, "scaffold_part1.py")) as f:
                        scaffold1 = f.read()
                    
                    with open(sol1, "w") as f:
                        f.write(scaffold1)
                    logging.info("Reset solution_part1.py to scaffold.")
                    previous_code = scaffold1
                    feedback = "Starting fresh. Please implement the solution starting from this scaffold. Fill in sample_input and sample_answer. The script MUST print the test result first, then the real result."

                # Try to run existing solution first if no feedback yet (skipped if we just reset)
                if attempt == 1 and os.path.exists(sol1) and not feedback and False: # Disabled because we always reset on attempt 1 now
                    try:
                        proc = subprocess.run(["python3", "solution_part1.py"], cwd=workdir, capture_output=True, text=True, timeout=30)
                        if proc.returncode == 0 and proc.stdout.strip():
                            # Parse output with regex
                            sample_match = re.search(r"---- Sample Solution Part 1: (.+?) ----", proc.stdout)
                            final_match = re.search(r"---- Final Solution Part 1: (.+?) ----", proc.stdout)
                            
                            if sample_match and final_match:
                                test_res = sample_match.group(1).strip()
                                real_res = final_match.group(1).strip()
                                if test_res != real_res and test_res != "0" and real_res != "0":
                                    output = real_res
                                    logging.info("Output from existing solution_part1.py: Test=%s, Real=%s", test_res, real_res)
                                else:
                                    feedback = f"Existing solution output invalid: Test='{test_res}', Real='{real_res}'. Must be distinct and non-zero."
                            else:
                                feedback = "Existing solution produced insufficient output (missing format markers)."
                        else:
                            # Existing solution failed or no output
                            if proc.returncode != 0:
                                feedback = f"Existing solution failed with error:\n{proc.stderr}"
                            else:
                                feedback = "Existing solution produced no output."
                            previous_code = open(sol1).read()
                    except Exception as e:
                        logging.warning("Failed to run existing solution_part1.py: %s", e)
                        feedback = f"Failed to run existing solution: {e}"

                # Generate if needed (if no output from existing, or if we have feedback from previous attempt)
                if not output and api_key:
                    logging.info("Generating solution for Part 1...")
                    problem_txt = open(os.path.join(workdir, "problem.txt"), "r").read()
                    input_txt = open(os.path.join(workdir, "input.txt"), "r").read()
                    
                    code = generate_solver_with_openrouter(problem_txt, input_txt, api_key, part=1, previous_code=previous_code, feedback=feedback)
                    
                    if code:
                        with open(sol1, "w") as f:
                            f.write(code)
                        git_commit([sol1], f"Agent generated solution_part1 for {year} day {day} (attempt {attempt})")
                        
                        try:
                            proc = subprocess.run(["python3", "solution_part1.py"], cwd=workdir, capture_output=True, text=True, timeout=60)
                            if proc.returncode == 0 and proc.stdout.strip():

                                # Parse output with regex
                                sample_match = re.search(r"---- Sample Solution Part 1: (.+?) ----", proc.stdout)
                                final_match = re.search(r"---- Final Solution Part 1: (.+?) ----", proc.stdout)
                                
                                if sample_match and final_match:
                                    test_res = sample_match.group(1).strip()
                                    real_res = final_match.group(1).strip()
                                    if test_res != real_res and test_res != "0" and real_res != "0":
                                        output = real_res
                                        logging.info("Output from generated solution_part1.py: Test=%s, Real=%s", test_res, real_res)
                                    else:
                                        feedback = f"Generated solution output invalid: Test='{test_res}', Real='{real_res}'. Must be distinct and non-zero."
                                        previous_code = code
                                        logging.warning("Verification failed: %s", feedback)
                                else:
                                    feedback = "Generated solution produced insufficient output (missing format markers)."
                                    previous_code = code
                                    logging.warning("Verification failed: %s", feedback)
                            else:
                                if proc.returncode != 0:
                                    feedback = f"Runtime error:\n{proc.stderr}"
                                else:
                                    feedback = "Script produced no output."
                                previous_code = code
                                logging.warning("Generation failed: %s", feedback)
                        except Exception as e:
                            logging.warning("Failed to run generated solution_part1.py: %s", e)
                            feedback = f"Execution failed: {e}"
                            previous_code = code
                    else:
                        logging.warning("No code generated.")
                        # If generation fails, maybe break or continue? Continue allows retry if transient.
                
                if output:
                    if _should_submit_interactive(output, 1):
                        res = submit_solution(year, day, 1, output, session)
                        logging.info("Submit result: %s", res)
                        if isinstance(res, dict) and res.get("success"):
                            logging.info("Part 1 solved successfully!")
                            # Cache the accepted solution
                            accepted_file = os.path.join(workdir, f"accepted_part1.txt")
                            with open(accepted_file, "w") as f:
                                f.write(str(output))
                            logging.info("Cached accepted solution to %s", accepted_file)
                            git_commit([workdir], f"Solved Part 1 for {year} Day {day}")
                            
                            status['part1_solved'] = True
                            status['part1_answer'] = str(output)
                            break
                        else:
                            logging.info("Part 1 submission failed.")
                            msg = res.get("message", "Unknown error")
                            feedback = f"Submitted answer '{output}' was incorrect. Message: {msg}"
                            if os.path.exists(sol1):
                                previous_code = open(sol1).read()
                    else:
                        logging.info("Submission skipped by user.")
                        break
                
                if attempt == max_retries:
                    logging.error("Part 1 failed after %d attempts.", max_retries)
        else:
            logging.info("Part 1 already solved.")

        # --- PART 2 ---
        # Only proceed to Part 2 if Part 1 is solved
        if status['part1_solved']:
            if not status['part2_solved']:
                logging.info("Part 2 not solved. Attempting to solve...")
                sol2 = os.path.join(workdir, "solution_part2.py")
                
                # Check local status again just in case
                accepted_status = check_accepted_files(workdir)
                
                if accepted_status and accepted_status['part2_solved']:
                    logging.info("Local files indicate Part 2 is solved. Skipping fetch.")
                else:
                    stmt = fetch_problem_statement(year, day, session)
                    with open(os.path.join(workdir, "problem.txt"), "w") as f:
                        f.write(stmt)
                
                max_retries = 20
                feedback = None
                previous_code = None
                
                for attempt in range(1, max_retries + 1):
                    logging.info("Part 2 Attempt %d/%d", attempt, max_retries)
                    output = None
                    
                    
                    # Reset to scaffold on fresh start
                    if attempt == 1 and not feedback:
                        # Load template again to be sure
                        template_dir = os.path.join(os.path.dirname(__file__), "templates")
                        with open(os.path.join(template_dir, "scaffold_part2.py")) as f:
                            scaffold2 = f.read()
                        
                        with open(sol2, "w") as f:
                            f.write(scaffold2)
                        logging.info("Reset solution_part2.py to scaffold.")
                        previous_code = scaffold2
                        feedback = "Starting fresh. Please implement the solution starting from this scaffold. Fill in sample_input and sample_answer. The script MUST print the results in the format: ---- Sample Solution Part 2: [result] ---- and ---- Final Solution Part 2: [result] ----"

                    if attempt == 1 and os.path.exists(sol2) and not feedback and False: # Disabled because we always reset on attempt 1 now
                        try:
                            proc = subprocess.run(["python3", "solution_part2.py"], cwd=workdir, capture_output=True, text=True, timeout=30)
                            if proc.returncode == 0 and proc.stdout.strip():
                                # Parse output with regex
                                sample_match = re.search(r"---- Sample Solution Part 2: (.+?) ----", proc.stdout)
                                final_match = re.search(r"---- Final Solution Part 2: (.+?) ----", proc.stdout)
                                
                                if sample_match and final_match:
                                    test_res = sample_match.group(1).strip()
                                    real_res = final_match.group(1).strip()
                                    if test_res != real_res and test_res != "0" and real_res != "0":
                                        output = real_res
                                        logging.info("Output from existing solution_part2.py: Test=%s, Real=%s", test_res, real_res)
                                    else:
                                        feedback = f"Existing solution output invalid: Test='{test_res}', Real='{real_res}'. Must be distinct and non-zero."
                                else:
                                    feedback = "Existing solution produced insufficient output (missing format markers)."
                            else:
                                if proc.returncode != 0:
                                    feedback = f"Existing solution failed with error:\n{proc.stderr}"
                                else:
                                    feedback = "Existing solution produced no output."
                                previous_code = open(sol2).read()
                        except Exception as e:
                            logging.warning("Failed to run existing solution_part2.py: %s", e)
                            feedback = f"Failed to run existing solution: {e}"

                    if not output and api_key:
                        logging.info("Generating solution for Part 2...")
                        problem_txt = open(os.path.join(workdir, "problem.txt"), "r").read()
                        input_txt = open(os.path.join(workdir, "input.txt"), "r").read()
                        code = generate_solver_with_openrouter(problem_txt, input_txt, api_key, part=2, previous_code=previous_code, feedback=feedback, model=model)
                        if code:
                            with open(sol2, "w") as f:
                                f.write(code)
                            git_commit([sol2], f"Agent generated solution_part2 for {year} day {day} (attempt {attempt})")
                            try:
                                proc = subprocess.run(["python3", "solution_part2.py"], cwd=workdir, capture_output=True, text=True, timeout=60)
                                if proc.returncode == 0 and proc.stdout.strip():

                                    # Parse output with regex
                                    sample_match = re.search(r"---- Sample Solution Part 2: (.+?) ----", proc.stdout)
                                    final_match = re.search(r"---- Final Solution Part 2: (.+?) ----", proc.stdout)
                                    
                                    if sample_match and final_match:
                                        test_res = sample_match.group(1).strip()
                                        real_res = final_match.group(1).strip()
                                        if test_res != real_res and test_res != "0" and real_res != "0":
                                            output = real_res
                                            logging.info("Output from generated solution_part2.py: Test=%s, Real=%s", test_res, real_res)
                                        else:
                                            feedback = f"Generated solution output invalid: Test='{test_res}', Real='{real_res}'. Must be distinct and non-zero."
                                            previous_code = code
                                            logging.warning("Verification failed: %s", feedback)
                                    else:
                                        feedback = "Generated solution produced insufficient output (missing format markers)."
                                        previous_code = code
                                        logging.warning("Verification failed: %s", feedback)
                                else:
                                    if proc.returncode != 0:
                                        feedback = f"Runtime error:\n{proc.stderr}"
                                    else:
                                        feedback = "Script produced no output."
                                    previous_code = code
                                    logging.warning("Generation failed: %s", feedback)
                            except Exception as e:
                                logging.warning("Failed to run generated solution_part2.py: %s", e)
                                feedback = f"Execution failed: {e}"
                                previous_code = code

                    if output:
                        if _should_submit_interactive(output, 2):
                            res = submit_solution(year, day, 2, output, session)
                            logging.info("Submit result: %s", res)
                            if isinstance(res, dict) and res.get("success"):
                                logging.info("Part 2 solved successfully!")
                                # Cache the accepted solution
                                accepted_file = os.path.join(workdir, f"accepted_part2.txt")
                                with open(accepted_file, "w") as f:
                                    f.write(str(output))
                                logging.info("Cached accepted solution to %s", accepted_file)
                                git_commit([workdir], f"Solved Part 2 for {year} Day {day}")
                                
                                status['part2_solved'] = True
                                status['part2_answer'] = str(output)
                                break
                            else:
                                logging.info("Part 2 submission failed.")
                                msg = res.get("message", "Unknown error")
                                feedback = f"Submitted answer '{output}' was incorrect. Message: {msg}"
                                if os.path.exists(sol2):
                                    previous_code = open(sol2).read()
                        else:
                            logging.info("Submission skipped by user.")
                            break
                    
                    if attempt == max_retries:
                        logging.error("Part 2 failed after %d attempts.", max_retries)
            
            else:
                # Part 2 is solved. Verification mode.
                logging.info("Part 2 already solved. Entering VERIFICATION MODE.")
                known_answer = status['part2_answer']
                logging.info("Known Part 2 Answer: %s", known_answer)
                
                if not known_answer:
                    logging.warning("Could not extract known answer from page. Skipping verification.")
                elif not api_key:
                    logging.warning("No API key. Skipping verification.")
                else:
                    max_attempts = 20
                    feedback = None
                    previous_code = None
                    
                    for attempt in range(1, max_attempts + 1):
                        logging.info("Verification Attempt %d/%d", attempt, max_attempts)
                        
                        problem_txt = open(os.path.join(workdir, "problem.txt"), "r").read()
                        input_txt = open(os.path.join(workdir, "input.txt"), "r").read()
                        
                        code = generate_solver_with_openrouter(problem_txt, input_txt, api_key, part=2, previous_code=previous_code, feedback=feedback, model=model)
                        
                        if code:
                            sol2_verify = os.path.join(workdir, "solution_part2_verify.py")
                            with open(sol2_verify, "w") as f:
                                f.write(code)
                            
                            try:
                                proc = subprocess.run(["python3", "solution_part2_verify.py"], cwd=workdir, capture_output=True, text=True, timeout=60)
                                if proc.returncode == 0 and proc.stdout.strip():
                                
                                    # Parse output with regex
                                    sample_match = re.search(r"---- Sample Solution Part 2: (.+?) ----", proc.stdout)
                                    final_match = re.search(r"---- Final Solution Part 2: (.+?) ----", proc.stdout)
                                    
                                    if sample_match and final_match:
                                        output = final_match.group(1).strip()
                                        logging.info("Generated Answer: %s", output)
                                        
                                        if output == known_answer:
                                            logging.info("VERIFICATION SUCCESS: Generated answer matches known answer.")
                                            os.rename(sol2_verify, os.path.join(workdir, "solution_part2.py"))
                                            git_commit([os.path.join(workdir, "solution_part2.py")], f"Agent verified solution_part2 for {year} day {day}")
                                            break
                                        else:
                                            logging.warning("VERIFICATION FAILED: Generated answer '%s' != Known answer '%s'", output, known_answer)
                                            feedback = f"Generated answer '{output}' is incorrect. Expected '{known_answer}'."
                                            previous_code = code
                                    else:
                                        logging.warning("Verification script produced insufficient output (missing format markers). Output:\n%s", proc.stdout)
                                        feedback = "Verification script produced insufficient output (missing format markers)."
                                        previous_code = code
                                else:
                                    logging.warning("Verification script failed or produced no output.")
                                    if proc.returncode != 0:
                                        feedback = f"Runtime error:\n{proc.stderr}"
                                    else:
                                        feedback = "Script produced no output."
                                    previous_code = code
                            except Exception as e:
                                logging.warning("Error running verification script: %s", e)
                                feedback = f"Execution failed: {e}"
                                previous_code = code
                        else:
                            logging.warning("Failed to generate verification code.")
                        
                        if attempt == max_attempts:
                            logging.error("Verification failed after %d attempts.", max_attempts)

    logging.info("Scaffold ready in %s. Use submit_solution() from aoc_tools to submit answers manually if needed.", workdir)


if __name__ == "__main__":
    main()
