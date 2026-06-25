Use skill sop-youtube-deep-research to execute this downstream node.

## 节点执行指南
- 边缘：youtube-fetch → youtube-deep-research
- 评估摘要：上下游存在直接输入输出映射，边缘交接指令清晰。
- 交接指令：将 source_url 作为 YouTube 深度研究目标视频地址，metadata 只作为可选上下文。

## 上游产物
1. **source_url**：`raw/node-runs/{pipeline_id}/outputs/files/source-url.txt`
   - 角色：主要源数据，包含目标视频 URL。
   - 使用方式：下游节点直接读取该文件作为 source_url 输入。
2. **metadata_file**：`raw/node-runs/{pipeline_id}/outputs/files/metadata.json`
   - 角色：可选上下文，如不需要可忽略。

## 执行规则
- 使用已解析的边缘输入和上游文件路径。
- 不得绕过当前节点定义的输入契约。
- 执行完成后，验证下游输出文件是否按预期生成。

## 下游输入构造
- `source_url`：由上游 source_url 文件自动解析，支持 file:text 或 file:json 格式。
- 如果上游 URL 为空，则执行失败。

## 校验点
- 确认下游 analysis.md 和 transcript.txt 已生成。
- 确保节点工作区内没有残留敏感数据。
