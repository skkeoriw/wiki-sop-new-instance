# YouTube 视频研究 Wiki

自动化 YouTube 视频研究知识图谱，由 `agent-brain-plugins/youtube-wiki` 驱动。

<!-- youtube-wiki-commands -->
## YouTube Wiki SOP

本仓库由 `agent-brain-plugins/youtube-wiki` 驱动，用于把 YouTube 视频自动转成 NotebookLM 研究报告、知识图谱 wiki 页面和 Telegram 通知。

### 流程阶段

```text
Stage A: youtube-fetch          获取 YouTube 元数据
Stage B: notebooklm-research    调用远程 NotebookLM Bridge 生成研究报告
Stage B2: youtube-deep-research 调用 YouTube Worker 深度研究并补充 Stage C 输入
Stage C: wiki-build             调用 Gemini 构建知识图谱页面
Stage D: tg-notify              发送 Telegram 总结并归档运行记录
```

### 一键安装 Skill

```bash
bash <(curl -fsSL 'https://skill.vyibc.com/install-youtube-wiki.sh?ts=20260601121037')
```

安装后，可以直接对 Codex/Claude 说：

```text
使用 youtube-wiki，帮我把这个 YouTube 链接跑进 skkeoriw/wiki-sop-new-instance: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 任意机器直接执行 CLI

触发流程：

```bash
bash <(curl -fsSL https://skill.vyibc.com/youtube-wiki.sh) \
  --endpoint=https://runtime-152-32-214-95.chxyka.ccwu.cc \
  --mode=trigger \
  --repo=skkeoriw/wiki-sop-new-instance \
  --url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
```

查询状态：

```bash
bash <(curl -fsSL https://skill.vyibc.com/youtube-wiki.sh) \
  --endpoint=https://runtime-152-32-214-95.chxyka.ccwu.cc \
  --mode=status \
  --repo=skkeoriw/wiki-sop-new-instance \
  --pipeline-id='<pipeline_id>'
```

持续等待直到 A/B/C/D 完成：

```bash
bash <(curl -fsSL https://skill.vyibc.com/youtube-wiki.sh) \
  --endpoint=https://runtime-152-32-214-95.chxyka.ccwu.cc \
  --mode=status \
  --repo=skkeoriw/wiki-sop-new-instance \
  --pipeline-id='<pipeline_id>' \
  --watch=true \
  --timeout=900
```

列出服务机器暴露的 wiki 仓库：

```bash
bash <(curl -fsSL https://skill.vyibc.com/youtube-wiki.sh) \
  --endpoint=https://runtime-152-32-214-95.chxyka.ccwu.cc \
  --mode=list
```

### 服务机器本地 CLI

```bash
youtube-wiki trigger --repo skkeoriw/wiki-sop-new-instance --url 'https://www.youtube.com/watch?v=5MgBikgcWnY'
youtube-wiki trigger --repo skkeoriw/wiki-sop-new-instance --url 'https://www.youtube.com/watch?v=5MgBikgcWnY' --watch
youtube-wiki status --repo skkeoriw/wiki-sop-new-instance --pipeline-id '<pipeline_id>'
youtube-wiki validate
```

### 新机器初始化 Skill

初始化脚本会自动安装私有 machine-init skill：

```text
~/.codex/skills/youtube-wiki-machine-init
~/.codex/skills/youtube-wiki-sop-engineering
```

后续可以让 Codex 初始化新的 wiki 仓库：

```text
使用 youtube-wiki-machine-init，在这台服务机器上初始化 skkeoriw/new-wiki-repo。
```
<!-- /youtube-wiki-commands -->


## 结构
- `raw/youtube-links/` — 推送 YouTube 链接触发流水线
- `raw/youtube-metadata/` — Stage A 获取的视频元数据
- `wiki/` — 生成的知识图谱页面
- `raw/notebooklm-analysis/` — NotebookLM 分析报告
- `raw/notebooklm-mindmaps/` — NotebookLM 脑图 JSON
- `raw/retry/` — 手动重跑指定阶段的触发目录
