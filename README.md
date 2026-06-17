# YouTube 视频研究 Wiki

自动化 YouTube 视频研究知识图谱，由 `agent-brain-plugins/youtube-wiki` 驱动。

<!-- youtube-wiki-commands -->
## YouTube Wiki SOP

初始化脚本会自动把本节替换为当前 wiki 仓库的 CLI 和 Codex skill 使用命令。
<!-- /youtube-wiki-commands -->

## 结构
- `raw/youtube-links/` — 推送 YouTube 链接触发流水线
- `raw/youtube-metadata/` — Stage A 获取的视频元数据
- `wiki/` — 生成的知识图谱页面
- `raw/notebooklm-analysis/` — NotebookLM 分析报告
- `raw/notebooklm-mindmaps/` — NotebookLM 脑图 JSON
- `raw/retry/` — 手动重跑指定阶段的触发目录
