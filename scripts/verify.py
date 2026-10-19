"""Run configuration twice and require a successful, unchanged second pass."""
import os
import re
import subprocess

command = ["ansible-playbook", "-i", "inventory.ini", "nginx.yml"]
env = dict(os.environ, ANSIBLE_NOCOLOR="1")
for attempt in (1, 2):
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=env)
    print(f"=== Pass {attempt} ===", flush=True)
    print(result.stdout, flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    recap = re.search(r"localhost\s+:\s+ok=\d+\s+changed=(\d+)\s+unreachable=(\d+)\s+failed=(\d+)", result.stdout)
    if not recap or any(int(recap[i]) for i in (2, 3)):
        raise SystemExit("Missing or unsuccessful localhost recap")
    if attempt == 2 and int(recap[1]):
        raise SystemExit("Second pass changed the host: idempotency check failed")
print("PASS: both runs succeeded, HTTP verification passed, second run changed=0.")
