import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt

load_dotenv()

print("读取到的 KEY:", os.getenv("LLM_API_KEY"))
print("读取到的 URL:", os.getenv("LLM_BASE_URL"))

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)
console = Console()

def read_code_file(filepath):
    """读取本地代码文件的工具"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件失败: {str(e)}"

SYSTEM_PROMPT = """你是一个专业的代码助手 Agent。
你的任务是帮助用户分析代码、解释逻辑、发现Bug。
你可以使用工具来读取代码文件。如果用户需要你分析某个文件，请返回：
[READ_FILE: 文件名]
例如：用户说“帮我看看 test.py”，你应该返回：[READ_FILE: test.py]
如果用户只是普通提问，直接回答即可，不要乱用工具。
请注意：你不能执行代码，只能分析。不要胡编乱造代码内容。"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

console.print("[bold green]🤖 代码助手 Agent 已启动！[/bold green]")
console.print("[yellow]输入 'exit' 退出程序。试着输入：帮我分析一下 test.py[/yellow]\n")

while True:
    user_input = Prompt.ask("[bold blue]你[/bold blue]")
    if user_input.lower() == 'exit':
        console.print("[green]再见！[/green]")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    max_retries = 3 
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",  
                messages=messages,
                temperature=0.2
            )
            reply_content = response.choices[0].message.content
            
            if "[READ_FILE:" in reply_content:
                start_idx = reply_content.find("[READ_FILE:") + len("[READ_FILE:")
                end_idx = reply_content.find("]", start_idx)
                filepath = reply_content[start_idx:end_idx].strip()
                
                console.print(f"[magenta]🔧 Agent 正在调用工具读取文件: {filepath}...[/magenta]")
                
                file_content = read_code_file(filepath)
                
                messages.append({"role": "assistant", "content": reply_content})
                messages.append({"role": "system", "content": f"文件 {filepath} 的内容如下：\n{file_content}"})
                
                console.print("[magenta]🧠 Agent 正在分析代码...[/magenta]")
                continue 
            
            console.print(f"[bold green]🤖 Agent:[/bold green] {reply_content}")
            messages.append({"role": "assistant", "content": reply_content})
            break
            
        except Exception as e:
            console.print(f"[bold red]⚠️ 请求出错 (尝试 {attempt+1}/{max_retries}): {str(e)}[/bold red]")
            time.sleep(2) 
    else:
        console.print("[bold red]❌ 多次重试失败，请检查网络或API Key。[/bold red]")
