import os
import subprocess
from typing import List, Set

TARGET_BRANCH = os.getenv("NUVO_TARGET_BRANCH", "main")
CRITICAL_FILES = [
    "agent_loop.py",
    "core/agent_evolution.py",
    "core/job_queue.py",
    "scripts/test_runtime.py",
]


def _run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def _lines(output: str) -> List[str]:
    return [x.strip() for x in output.splitlines() if x.strip()]


def _changed_files(revspec: str) -> Set[str]:
    proc = _run(["git", "diff", "--name-only", revspec])
    if proc.returncode != 0:
        return set()
    return set(_lines(proc.stdout))


def main():
    print(f"[diagnose] target_branch={TARGET_BRANCH}")

    # 1) conflict markers in working tree files
    markers = ("<" * 7, "=" * 7, ">" * 7)
    marker_hits = []
    for path in CRITICAL_FILES:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if any(m in content for m in markers):
            marker_hits.append(path)

    if marker_hits:
        print("[diagnose] conflict markers found:")
        for item in marker_hits:
            print(f" - {item}")
    else:
        print("[diagnose] no conflict markers in critical files")

    # 2) branch divergence analysis (if target branch exists locally)
    target_ref = f"refs/heads/{TARGET_BRANCH}"
    has_target = _run(["git", "show-ref", "--verify", "--quiet", target_ref]).returncode == 0
    if not has_target:
        print(f"[diagnose] target branch '{TARGET_BRANCH}' not found locally.")
        print("[diagnose] probable reason of persistent PR conflicts: branch divergence with remote target.")
        print("[diagnose] action: fetch target branch and rebase/merge before opening PR.")
        return

    merge_base = _run(["git", "merge-base", "HEAD", TARGET_BRANCH])
    if merge_base.returncode != 0:
        print("[diagnose] unable to compute merge-base")
        return

    base = merge_base.stdout.strip()
    head_changed = _changed_files(f"{base}..HEAD")
    target_changed = _changed_files(f"{base}..{TARGET_BRANCH}")
    overlap = sorted(head_changed & target_changed)

    print(f"[diagnose] files changed in HEAD since merge-base: {len(head_changed)}")
    print(f"[diagnose] files changed in {TARGET_BRANCH} since merge-base: {len(target_changed)}")
    print(f"[diagnose] overlap potentially causing conflicts: {len(overlap)}")
    for path in overlap[:30]:
        print(f" - {path}")


if __name__ == "__main__":
    main()
