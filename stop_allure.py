#!/usr/bin/env python3
"""
Stop Allure 'serve' background process started by run.py --serve --background.

Usage:
  python stop_allure.py              # Read reports/allure.pid and try to stop that PID (recommended)
  python stop_allure.py --pid-file path/to/file.pid
  python stop_allure.py --find      # Try to find running 'allure' processes (pgrep / wmic) and prompt to stop
  python stop_allure.py --force     # Kill without interactive confirmation (use with care)

This script:
- If a PID file exists (default reports/allure.pid) it will try a graceful terminate, wait, then force-kill if necessary.
- If no PID file or --find is used, it will try to discover Allure processes and optionally stop them.
- Works on Windows and Unix-like systems, using taskkill when necessary on Windows.
"""
from __future__ import annotations
import os
import sys
import time
import argparse
import subprocess
import signal

DEFAULT_PID_FILE = os.path.join("reports", "allure.pid")
WAIT_SECONDS_BEFORE_FORCE = 5


def read_pid_file(pid_file: str) -> int | None:
    if not os.path.isfile(pid_file):
        return None
    try:
        with open(pid_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return None
        return int(content)
    except Exception as e:
        print(f"Failed to read PID file '{pid_file}': {e}")
        return None


def is_pid_running(pid: int) -> bool:
    try:
        # On Unix and Windows, os.kill(pid, 0) will raise if process does not exist.
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # Process exists but we have no permission to signal it
        return True
    except OSError:
        return False
    else:
        return True


def terminate_pid(pid: int) -> bool:
    """Try graceful terminate then force kill if necessary. Returns True if process ended."""
    if not is_pid_running(pid):
        print(f"PID {pid} is not running.")
        return True

    try:
        print(f"Sending SIGTERM to PID {pid}...")
        os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(f"Failed to send SIGTERM to {pid}: {e}")

    # Wait for a short period for the process to exit
    for i in range(WAIT_SECONDS_BEFORE_FORCE):
        if not is_pid_running(pid):
            print(f"PID {pid} exited after SIGTERM.")
            return True
        time.sleep(1)

    print(f"PID {pid} still running after {WAIT_SECONDS_BEFORE_FORCE} seconds; trying force kill...")

    try:
        if os.name == "nt":
            # Use taskkill for Windows to ensure child processes are killed as well
            subprocess.check_call(["taskkill", "/PID", str(pid), "/F", "/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.kill(pid, signal.SIGKILL)
    except Exception as e:
        print(f"Force kill failed for PID {pid}: {e}")

    # Final check
    time.sleep(0.5)
    if not is_pid_running(pid):
        print(f"PID {pid} has been terminated.")
        return True
    else:
        print(f"PID {pid} is still running after force kill attempt.")
        return False


def find_allure_pids_unix() -> list[int]:
    """Use pgrep -f allure to find processes containing 'allure' in command line."""
    try:
        out = subprocess.check_output(["pgrep", "-f", "allure"], text=True, stderr=subprocess.DEVNULL)
        pids = [int(line.strip()) for line in out.strip().splitlines() if line.strip()]
        return pids
    except subprocess.CalledProcessError:
        return []
    except Exception:
        return []


def find_allure_pids_windows() -> list[int]:
    """Try to find allure processes on Windows using wmic or powershell."""
    pids = set()
    # Try WMIC (older but commonly available)
    try:
        out = subprocess.check_output(
            ['wmic', 'process', 'where', "CommandLine LIKE '%allure%'", 'get', 'ProcessId,CommandLine', '/FORMAT:LIST'],
            text=True, stderr=subprocess.DEVNULL
        )
        for line in out.splitlines():
            if line.strip().startswith("ProcessId="):
                try:
                    pids.add(int(line.split("=", 1)[1].strip()))
                except Exception:
                    continue
    except Exception:
        pass

    # Try PowerShell if WMIC didn't find anything
    if not pids:
        try:
            ps_cmd = [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like '*allure*'} | Select-Object -ExpandProperty ProcessId"
            ]
            out = subprocess.check_output(ps_cmd, text=True, stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    pids.add(int(line))
                except Exception:
                    continue
        except Exception:
            pass

    return sorted(pids)


def find_allure_pids() -> list[int]:
    if os.name == "nt":
        return find_allure_pids_windows()
    else:
        return find_allure_pids_unix()


def remove_pid_file(pid_file: str) -> None:
    try:
        if os.path.isfile(pid_file):
            os.remove(pid_file)
            print(f"Removed PID file: {pid_file}")
    except Exception as e:
        print(f"Failed to remove PID file {pid_file}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Stop Allure serve background process (created by run.py --serve --background).")
    parser.add_argument("--pid-file", "-p", default=DEFAULT_PID_FILE, help=f"PID file to read (default: {DEFAULT_PID_FILE})")
    parser.add_argument("--find", "-f", action="store_true", help="Try to find running 'allure' processes if PID file not found.")
    parser.add_argument("--force", action="store_true", help="Don't prompt; force kill discovered processes.")
    parser.add_argument("--list-only", action="store_true", help="Only list found PIDs, do not kill.")
    args = parser.parse_args()

    pid_file = args.pid_file

    pid = read_pid_file(pid_file)
    if pid is not None:
        print(f"Found PID in file {pid_file}: {pid}")
        if args.list_only:
            print("List-only requested; not killing.")
            return 0
        ok = terminate_pid(pid)
        if ok:
            remove_pid_file(pid_file)
            return 0
        else:
            print("Failed to stop process recorded in PID file.")
            # fallthrough to find option if requested
            if not args.find:
                return 1

    # If no pid file or stopping by pid failed and --find specified, try to discover processes
    if args.find or pid is None:
        pids = find_allure_pids()
        if not pids:
            print("No 'allure' processes found on this machine.")
            return 0
        print("Discovered 'allure' related PIDs:", ", ".join(str(x) for x in pids))
        if args.list_only:
            return 0
        if not args.force:
            try:
                ans = input("Kill these processes? [y/N]: ").strip().lower()
            except KeyboardInterrupt:
                print("\nAborted by user.")
                return 1
            if ans not in ("y", "yes"):
                print("Aborted: not killing processes.")
                return 0

        rc = 0
        for p in pids:
            ok = terminate_pid(p)
            if not ok:
                print(f"Warning: could not stop PID {p}")
                rc = 1
        # Try to remove PID file if exists
        remove_pid_file(pid_file)
        return rc

    print("Nothing to do.")
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        exit_code = 1
    sys.exit(exit_code)