import subprocess
import sys
import shutil
import os
import argparse
import shlex

def run_pytest(pytest_extra_args=None):
    """
    Run pytest and put results into reports/allure_results.
    pytest_extra_args: list of extra args to forward to pytest (e.g. ['--use-local-driver', '--headless'])
    """
    cmd = [sys.executable, "-m", "pytest", "-q", "--alluredir=reports/allure_results"]
    if pytest_extra_args:
        # pytest_extra_args expected to be a list
        cmd = [sys.executable, "-m", "pytest"] + pytest_extra_args + ["-q", "--alluredir=reports/allure_results"]
    print("Running pytest:", " ".join(shlex.quote(p) for p in cmd))
    ret = subprocess.call(cmd)
    if ret != 0:
        print("pytest finished with non-zero exit code:", ret)
    return ret

def find_allure():
    return shutil.which("allure")

def generate_report(allure_path):
    os.makedirs("reports/allure_results", exist_ok=True)
    try:
        if allure_path:
            print("Generating allure report via:", allure_path)
            subprocess.check_call([allure_path, "generate", "reports/allure_results", "-o", "reports/allure-report", "--clean"])
        else:
            print("Generating allure report via shell fallback")
            subprocess.check_call("allure generate reports/allure_results -o reports/allure-report --clean", shell=True)
        print("Report successfully generated to reports/allure-report")
        return True
    except Exception as e:
        print("Allure generate failed:", e)
        return False

def open_report_with_allure(allure_path):
    try:
        if allure_path:
            subprocess.check_call([allure_path, "open", "reports/allure-report"])
        else:
            subprocess.check_call("allure open reports/allure-report", shell=True)
        return True
    except Exception as e:
        print("Failed to open report with Allure CLI:", e)
        # fallback: open index.html with default browser (if exists)
        index_path = os.path.abspath("reports/allure-report/index.html")
        if os.path.isfile(index_path):
            print("Opening generated report index.html in default browser...")
            try:
                if sys.platform.startswith("win"):
                    os.startfile(index_path)
                elif sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", index_path])
                else:
                    subprocess.Popen(["xdg-open", index_path])
                return True
            except Exception as e2:
                print("Fallback open failed:", e2)
        return False

def serve_report(allure_path, background=False, write_pid=True):
    """
    Start `allure serve reports/allure_results`.
    If background==False -> block until server exits (interactive).
    If background==True  -> start in background and return the PID (write PID to reports/allure.pid if write_pid True).
    """
    # Build command; prefer list when we have absolute allure_path
    if allure_path:
        cmd = [allure_path, "serve", "reports/allure_results"]
        use_shell = False
    else:
        cmd = "allure serve reports/allure_results"
        use_shell = True

    if background:
        stdout = subprocess.DEVNULL
        stderr = subprocess.DEVNULL
        if os.name == "nt":
            # Windows: create new console so child isn't tied to parent
            creationflags = subprocess.CREATE_NEW_CONSOLE
            p = subprocess.Popen(cmd, shell=use_shell, stdout=stdout, stderr=stderr, creationflags=creationflags)
        else:
            # Unix: detach using setsid
            p = subprocess.Popen(cmd, shell=use_shell, stdout=stdout, stderr=stderr, preexec_fn=os.setsid)

        pid = p.pid
        print(f"Allure serve started in background (PID {pid}).")
        if write_pid:
            try:
                os.makedirs("reports", exist_ok=True)
                with open("reports/allure.pid", "w") as f:
                    f.write(str(pid))
                print("Wrote PID to reports/allure.pid")
            except Exception as e:
                print("Failed to write PID file:", e)
        print("To stop: on Windows run 'taskkill /PID {pid} /F', on Unix 'kill {pid}'.")
        return pid
    else:
        try:
            p = subprocess.Popen(cmd, shell=use_shell)
            print("Allure serve started (blocking). Press Ctrl+C to stop.")
            p.wait()
            return p.returncode
        except KeyboardInterrupt:
            print("Stopping Allure serve (user interrupt).")
            try:
                p.terminate()
            except Exception:
                pass
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pytest and handle Allure reports (generate / open / serve)")
    parser.add_argument("--serve", action="store_true", help="Start 'allure serve' to view the allure-results (can be combined with --background).")
    parser.add_argument("--background", action="store_true", help="When used with --serve, start the server in background (non-blocking).")
    parser.add_argument("--open", action="store_true", help="After generating the report, open it with Allure (allure open).")
    parser.add_argument("--no-generate", action="store_true", help="Do not generate/serve Allure report; only run pytest.")
    parser.add_argument("--pytest-args", nargs=argparse.REMAINDER, help="Extra args to pass to pytest (place them after this flag)")
    args = parser.parse_args()

    # ensure results dir exists
    os.makedirs("reports/allure_results", exist_ok=True)

    # Run pytest first (unless user explicitly only wants to serve an existing folder)
    pytest_args = None
    if args.pytest_args:
        pytest_args = args.pytest_args
        if pytest_args and pytest_args[0] == "--":
            pytest_args = pytest_args[1:]
    run_pytest(pytest_args)

    if args.no_generate:
        print("Skipping Allure generate/serve (--no-generate specified).")
        sys.exit(0)

    allure_path = find_allure()
    if not allure_path:
        print("Warning: 'allure' not found by shutil.which; script will try shell fallback.")

    if args.serve:
        serve_report(allure_path, background=args.background, write_pid=True)
        sys.exit(0 if args.background else 0)

    # default: generate then maybe open
    ok = generate_report(allure_path)
    if ok and args.open:
        opened = open_report_with_allure(allure_path)
        if not opened:
            print("Failed to open report automatically. You can open reports/allure-report/index.html manually.")
    elif ok:
        print("Report generated. Use 'allure open reports/allure-report' to open, or run this script with --open or --serve.")