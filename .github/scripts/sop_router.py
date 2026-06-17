#!/usr/bin/env python3
"""
SOP Router - reads sop.yaml, detects changed files, calls the right Hermes webhook.
设计原则：零硬编码，所有行为从 sop.yaml 读取。
"""
import os
import sys
import json
import subprocess
import yaml


def decode_git_path(path: str) -> str:
    path = path.strip()
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
        import re
        def replace_octal(m):
            return bytes([int(m.group(0)[1:], 8)]).decode('latin-1')
        path = re.sub(r'\\[0-7]{3}', replace_octal, path)
    return path


def _run_git_diff(diff_filter: str, before_sha: str, after_sha: str) -> list[str]:
    git_env = {**os.environ, 'GIT_CONFIG_NOSYSTEM': '1'}
    cmd = ["-c", "core.quotepath=false", "diff", "--name-only", f"--diff-filter={diff_filter}"]
    try:
        r = subprocess.run(["git"] + cmd + [f"{before_sha}..{after_sha}"],
                           capture_output=True, text=True, check=True, env=git_env)
        return [decode_git_path(f) for f in r.stdout.strip().split("\n") if f.strip()]
    except subprocess.CalledProcessError:
        r = subprocess.run(["git"] + cmd + ["HEAD~1..HEAD"],
                           capture_output=True, text=True, check=True, env=git_env)
        return [decode_git_path(f) for f in r.stdout.strip().split("\n") if f.strip()]


def get_changed_files(before_sha, after_sha):
    return _run_git_diff("AM", before_sha, after_sha)


def get_added_files(before_sha, after_sha):
    return _run_git_diff("A", before_sha, after_sha)


def matches_pattern(filepath, pattern):
    import fnmatch
    return fnmatch.fnmatch(filepath, pattern)


def matches_any(files, pattern):
    return any(matches_pattern(f, pattern) for f in files)


# ── TG 通知（从 sop.yaml 读 token_env 和 chat_id，零硬编码）────────────────

def send_tg(sop: dict, text: str):
    notify = sop.get("notify", {}).get("telegram", {})
    token_env = notify.get("token_env", "")
    chat_id = str(notify.get("chat_id", ""))
    token = os.environ.get(token_env, "")
    if not token or not chat_id:
        print(f"[sop_router] TG 未配置（token_env={token_env}），跳过通知")
        return
    subprocess.run([
        "curl", "-s", "-X", "POST",
        f"https://api.telegram.org/bot{token}/sendMessage",
        "-d", f"chat_id={chat_id}",
        "-d", "disable_web_page_preview=true",
        "--data-urlencode", f"text={text}",
        "--max-time", "10",
    ], capture_output=True)
    print(f"[sop_router] TG 通知已发送")


# ── Webhook 调用 ──────────────────────────────────────────────────────────

def call_webhook(route, payload, base_url, secret):
    url = f"{base_url}/{route}"
    run_id = payload.get("run_id", "unknown")
    result = subprocess.run([
        "curl", "-sS", "-X", "POST", url,
        "-H", "Content-Type: application/json",
        "-H", f"X-Gitlab-Token: {secret}",
        "-H", f"X-Request-ID: {run_id}",
        "-H", "User-Agent: curl/7.81.0",
        "-d", json.dumps(payload),
        "-w", "\nHTTP_STATUS:%{http_code}",
        "--max-time", "30",
    ], capture_output=True, text=True)
    print(f"[sop_router] POST {url}\n{result.stdout[-300:]}")
    if result.returncode != 0:
        return False
    for line in result.stdout.split("\n"):
        if line.startswith("HTTP_STATUS:"):
            return 200 <= int(line.split(":")[1]) < 300
    return False


# ── main ──────────────────────────────────────────────────────────────────

def main():
    base_urls = [u.strip() for u in os.environ.get(
        "HERMES_WEBHOOK_BASE", "https://hermes-webhooks.vyibc.com/webhooks"
    ).split(",") if u.strip()]
    secret    = os.environ.get("HERMES_SOP_SECRET", "")
    before_sha = os.environ.get("BEFORE_SHA", "")
    after_sha  = os.environ.get("AFTER_SHA", "HEAD")
    run_id     = os.environ.get("RUN_ID", "unknown")
    repo       = os.environ.get("REPO", "")

    with open("sop.yaml") as f:
        sop = yaml.safe_load(f)

    pipeline_name = sop.get("name", repo)
    changed    = get_changed_files(before_sha, after_sha)
    added_only = get_added_files(before_sha, after_sha)
    print(f"[sop_router] Changed(AM): {changed}")
    print(f"[sop_router] Added(A):    {added_only}")

    # ── 无变更 ──
    if not changed:
        msg = f"⏸ [{pipeline_name}] 无文件变更，pipeline 跳过"
        print(f"[sop_router] {msg}")
        send_tg(sop, msg)
        return

    # ── 只有终态文件变更 ──
    terminal_paths = sop.get("terminal_paths", [])
    non_terminal = [f for f in changed
                    if not any(matches_pattern(f, p) for p in terminal_paths)]
    if not non_terminal:
        msg = f"✅ [{pipeline_name}] Pipeline 已完成（仅终态文件变更）"
        print(f"[sop_router] {msg}")
        send_tg(sop, msg)
        return

    # ── 匹配阶段（从 sop.yaml 读取，零硬编码）──
    # sop.yaml 每个 stage 可声明 added_only: true，不声明则 ADDED+MODIFIED 都触发
    matched_stage = None
    for stage in sop.get("pipeline", []):
        trigger = stage.get("trigger", "")
        use_added_only = stage.get("added_only", False)   # ← 读配置，非硬编码
        files_to_check = added_only if use_added_only else changed
        if matches_any(files_to_check, trigger):
            matched_stage = stage
            break

    if not matched_stage:
        msg = (f"⏸ [{pipeline_name}] 无阶段匹配\n"
               f"变更文件: {', '.join(non_terminal[:3])}")
        print(f"[sop_router] {msg}")
        send_tg(sop, msg)
        return

    stage_name = matched_stage["stage"]

    # ── Stage D 守卫：只允许 stage-c done commit 触发 ──
    if stage_name == "tg-notify":
        commit_msg = subprocess.run(
            ["git", "log", "-1", "--format=%s", after_sha],
            capture_output=True, text=True
        ).stdout.strip()
        if "stage-c done" not in commit_msg.lower():
            msg = f"⏸ [{pipeline_name}] Stage D 守卫：commit 不是来自 Stage C，跳过"
            print(f"[sop_router] {msg}")
            send_tg(sop, msg)
            return

    # ── 触发阶段 ──
    webhook_route = matched_stage["webhook_route"]
    stage_params  = matched_stage.get("params", {})
    notify        = sop.get("notify", {}).get("telegram", {})
    notebooklm    = stage_params.get("notebooklm", {})

    import re as _re, subprocess as _sp2
    commit_msg_full = _sp2.run(
        ["git", "log", "-1", "--format=%s", after_sha],
        capture_output=True, text=True
    ).stdout.strip()
    pipe_match  = _re.search(r'\[pipe:([^\]]+)\]', commit_msg_full)
    pipeline_id = pipe_match.group(1) if pipe_match else ""

    # 触发前发 TG 通知
    tg_start_msg = (f"⏳ [{pipeline_name}] Stage {stage_name} 开始\n"
                    f"   Run: {run_id}")
    send_tg(sop, tg_start_msg)

    payload = {
        "stage": stage_name,
        "wiki_local_path": sop.get("wiki_local_path", ""),
        "repo": repo or sop.get("repo", ""),
        "repo_url": f"https://github.com/{repo or sop.get('repo','')}",
        "sha": after_sha, "before": before_sha,
        "run_id": run_id, "pipeline_id": pipeline_id,
        "tg_token_env": notify.get("token_env", "TELEGRAM_BOT_TOKEN"),
        "tg_chat_id": notify.get("chat_id", ""),
        "notebooklm_outputs":       notebooklm.get("outputs", ["report", "mindmap"]),
        "notebooklm_language":      notebooklm.get("language", "zh_Hans"),
        "notebooklm_notebook_title": notebooklm.get("notebook_title", ""),
        "notebooklm_report_prompt": notebooklm.get("report_prompt", ""),
        "notebooklm_mindmap_prompt": notebooklm.get("mindmap_prompt", ""),
        "build_mode": stage_params.get("build_mode", "incremental"),
    }

    results = [(u, call_webhook(webhook_route, payload, u, secret)) for u in base_urls]
    succeeded = [u for u, ok in results if ok]
    failed    = [u for u, ok in results if not ok]

    if failed:
        fail_msg = (f"❌ [{pipeline_name}] Stage {stage_name} Webhook 失败\n"
                    f"   失败端点: {len(failed)}/{len(results)}")
        send_tg(sop, fail_msg)
        print(f"[sop_router] {fail_msg}")

    if not succeeded:
        sys.exit(1)

    print(f"[sop_router] ✅ 触发成功: {stage_name} → {len(succeeded)}/{len(results)} 端点")


if __name__ == "__main__":
    main()
