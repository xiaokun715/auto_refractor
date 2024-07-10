import openai
import os
from pylint import epylint as lint

# 设置你的API密钥
openai.api_key = 'your-api-key-here'

# 定义不同坏味道对应的提示词
prompts = {
    "Long Method": "Refactor the following long method to make it shorter and more modular:",
    "Large Class": "Refactor the following large class to make it smaller and more cohesive:",
    "Duplicated Code": "Refactor the following duplicated code to remove redundancy:",
    "Complex Code": "Refactor the following complex code to make it simpler and more readable:"
}

# 定义函数，调用OpenAI API进行代码重构
def refactor_code(code_chunk, prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # 选择合适的模型
        prompt=f"{prompt}\n\n{code_chunk}",
        max_tokens=2048,  # 根据需要调整最大tokens数量
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text.strip()

# 分析代码并返回坏味道和对应的代码块
def analyze_code(file_path):
    (pylint_stdout, pylint_stderr) = lint.py_run(file_path, return_std=True)
    output = pylint_stdout.getvalue()
    
    # 示例解析（具体解析逻辑需根据实际情况调整）
    code_smells = []
    current_smell = None
    current_code = []
    
    for line in output.splitlines():
        if "Long Method" in line:
            if current_smell:
                code_smells.append((current_smell, "\n".join(current_code)))
            current_smell = "Long Method"
            current_code = []
        elif "Large Class" in line:
            if current_smell:
                code_smells.append((current_smell, "\n".join(current_code)))
            current_smell = "Large Class"
            current_code = []
        # 添加更多坏味道的检测
        else:
            current_code.append(line)
    
    if current_smell:
        code_smells.append((current_smell, "\n".join(current_code)))
    
    return code_smells

# 定义函数，将重构后的代码写入新文件
def write_to_file(output_path, refactored_code):
    with open(output_path, 'a', encoding='utf-8') as file:
        file.write(refactored_code + '\n')

# 主函数
def main(input_file, output_file):
    # 清空或创建输出文件
    open(output_file, 'w').close()
    
    code_smells = analyze_code(input_file)
    
    for smell, code_chunk in code_smells:
        if smell in prompts:
            refactored_chunk = refactor_code(code_chunk, prompts[smell])
            write_to_file(output_file, refactored_chunk)
            print(f"Processed chunk for {smell}")
        else:
            print(f"Unknown code smell: {smell}")

if __name__ == "__main__":
    input_file = 'path_to_your_large_code_file.py'
    output_file = 'path_to_your_refactored_code_file.py'
    main(input_file, output_file)
