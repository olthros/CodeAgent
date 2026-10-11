# Code Agent 1 - 代码审查助手
## 项目说明
基于大模型API构建的简单代码助手Agent，支持自然语言交互，能自动识别需求并调用本地工具读取代码文件，进行代码解析与Bug发现。

## 使用方法
1. 安装依赖：`pip install openai python-dotenv rich`
2. 配置 `.env` 文件（填入你的 API Key）。
3. 运行：`python main.py`，输入“帮我分析一下 test.py”。

## 设计文档
- **Agent 架构**：采用极简的 ReAct (Reasoning + Acting) 模式。主程序维持一个 `while` 循环。
- **工具集成**：内置 `read_code_file` 工具。当大模型输出 `[READ_FILE: xxx]` 指令时，主程序拦截并执行该工具，将结果注入上下文。
- **上下文记忆**：使用 `messages` 列表进行多轮对话历史追踪。
- **错误处理**：使用 `try...except` 和 `for` 循环实现 API 调用的重试机制（最多3次）。
