<div style="text-align:center">
<h2> Civil-Bench: An Evaluation Framework for Civil Engineering Professional Qualification Exams</h2>
</div>

<div align="center">
<a href=''><img src='https://img.shields.io/badge/Paper-同济大学学报-red'></a> 
<a href=''><img src='https://img.shields.io/badge/License-Apache--2.0-blue.svg'></a>  

English | [简体中文](README-CN.md)
</div>

# Introduction
Welcome to Civil-Bench
The evaluation framework consists of six key assessment dimensions:

1. **Engineering Management and Construction**: Evaluates the model's knowledge and application abilities in construction technology, project management, cost estimation, construction safety, and green construction.
2. **Architectural and Structural Design**: Tests the model's understanding of building structures, materials, structural calculations, and engineering codes, and examines its application abilities in architectural design and structural analysis.
3. **Safety Engineering**: Measures the model's reasoning and decision-making abilities in structural safety assessment, disaster prevention, engineering accident analysis, and emergency management.
4. **Environmental Engineering**: Assesses the model’s coverage of knowledge and practical guidance capabilities in areas such as water pollution prevention, air pollution control, solid waste management, and environmental impact assessment.
5. **Civil Engineering**: Examines the model's grasp of basic engineering theories and design methods in areas such as foundation engineering, bridges and tunnels, road traffic, and construction machinery.
6. **Surveying and Geographic Information**: Tests the model's capabilities in engineering surveying, construction staking, GIS and remote sensing applications, and deformation monitoring, evaluating its potential in the surveying and geographic information field.

This framework establishes a standardized evaluation benchmark for professional language models in the civil engineering field, providing a comprehensive measure of the model's professionalism, precision, and practical engineering application abilities.

<div align="center">
  <img src="img\Civil-Bench.png" width="100%"/>
  <br />
  <br /></div>

# Content
-[QuickStart](#QuickStart)<br/>
-[TestResult](#TestResult)

# QuickStart

## Directory description

data----data of questions<br/>
src----codes of evaluation

## Install

Here are simple steps to download the repository and create an environment.
 ```cmd
    conda create --name CivilBench python=3.10
    conda activate CivilBench
 ```
 ```cmd
    git clone https://github.com/TongjiTierLab/Civil-Bench
    cd Civil-Bench
    cd src
    pip install -r requirements.txt
```

## Evaluation
Please first open the src/llm_resonsor/LLMTest.py file, and write the Your_Model class according to the calling method of the model that needs to be evaluated/used for scoring. You can refer to OpenAI_model as an example.
```python
class OpenAI_Model(BaseLLM):

    """兼容OpenAI模型的实现"""
    def __init__(self, model_name: str, api_key: str,**kwargs):
        self.ModelName = model_name
        self.ApiKey = api_key
        if "base_url" in kwargs:
            self.base_url = kwargs.get("base_url")
            self.client = OpenAI(api_key=self.ApiKey, base_url=self.base_url)
        else:
            self.client = OpenAI(api_key=self.ApiKey)
    def call_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        response = self.client.chat.completions.create(
            model=self.ModelName,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
class Your_Model(BaseLLM):
    """兼容你的模型的实现"""
    def __init__(self, model_name: str, api_key: str,**kwargs):
        pass
    def call_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass
```

Fill in the information of the models to be evaluated in the .env file.

```
# Information of test model
test_model_name=<test_model_name>
test_model_api_key=<test_model_api_key>
test_model_url = <test_model_url>

# Information of teacher model
teacher_model_name=<teacher_model_name>
teacher_model_api_key=<teacher_model_api_key>
teacher_model_url = <teacher_model_url>
```

Run the src/main.py file in the command line to start the evaluation.
```python
python main.py
```
The code execution status and completed questions will be logged in the log folder.<br/>
Detailed responses will be saved in the output folder.<br/>
Evaluation scores will be stored in the score folder.

# TestResult

The performance of some large models is shown in the table below:

## Overall Score
| 模型名称 | 组织/团队名称 | 发布日期 | 类型 | 参数量 | 综合得分 | 安全工程类 | 工程管理与建造类 | 测绘与地理信息类 | 建筑与结构设计类 | 土木工程类 | 环境工程类 |
|---------|-------------|----------|------|--------|----------|------------|-----------------|-----------------|------------------|------------|------------|
| CivilGPT | 同济大学土木工程学院 | 2024-11-09 | 闭源 | 72B | 74.74 | 77.47 | 74.77 | 82.99 | 75.92 | 66.43 | 74.86 |
| Qwen-Max | 阿里云 | 2025-01-27 | 闭源 | N/A | 70.28 | 73.11 | 71.06 | 79.82 | 71.65 | 58.73 | 70.80 |
| Hunyuan-Turbo | 腾讯混元 | 2025-01-10 | 闭源 | N/A | 67.44 | 68.71 | 68.53 | 72.77 | 69.20 | 57.62 | 69.57 |
| Doubao-1.5-pro-32K | 字节跳动 | 2025-01-22 | 闭源 | N/A | 65.64 | 65.13 | 65.71 | 69.66 | 69.65 | 61.18 | 62.41 |
| DeepSeek-R1 | 深度求索 | 2025-01-20 | 开源 | 671B | 64.81 | 68.43 | 64.17 | 74.96 | 65.95 | 54.90 | 70.38 |
| Qwen2.5-7b-Instruct | 阿里云 | 2024-09-19 | 开源 | 72B | 64.40 | 65.18 | 65.91 | 74.51 | 66.28 | 54.10 | 62.37 |
| MiniMax-Text-01 | 稀宇科技 | 2025-01-15 | 开源 | 456B | 62.46 | 62.99 | 62.63 | 72.05 | 65.30 | 55.69 | 60.41 |
| Yi-Lightning | 零一万物 | 2024-10-16 | 闭源 | N/A | 59.62 | 61.16 | 59.22 | 70.58 | 60.87 | 53.61 | 60.62 |
| GLM-4-Plus | 智谱AI | 2024-08-29 | 闭源 | 130B | 58.88 | 60.18 | 58.72 | 68.91 | 62.41 | 51.04 | 56.22 |
| GPT-4o | OpenAI | 2024-05-14 | 闭源 | N/A | 52.87 | 57.02 | 52.35 | 48.69 | 55.94 | 46.33 | 47.01 |
| Moonshot-v1-128k | 月之暗面 | 2014-01-31 | 闭源 | N/A | 49.19 | 51.48 | 47.75 | 55.13 | 54.63 | 42.12 | 46.42 |
| Mistral Large 2 | Mistral AI | 2024-09-18 | 闭源 | 128B | 44.81 | 47.83 | 41.57 | 46.07 | 48.92 | 40.99 | 54.38 |
| Spark4.0-Ultra | 科大讯飞 | 2024-06-27 | 闭源 | N/A | 44.61 | 48.48 | 44.94 | 47.27 | 48.01 | 33.14 | 40.83 |
| ERNIE-Speed-Pro-128K | 百度 | 2024-03-14 | 闭源 | N/A | 42.59 | 45.97 | 39.61 | 47.99 | 48.13 | 38.14 | 40.96 |
## Safety Engineering
| 模型名称 | 组织/团队名称 | 发布日期 | 类型 | 参数量 | 消防工程师 | 核安全工程师 | 安全工程师 | 综合得分 |
|---------|-------------|----------|------|--------|------------|--------------|------------|----------|
| CivilGPT | 同济大学土木工程学院 | 2024-11-09 | 闭源 | 72B | 62.44 | 79.75 | 80.76 | 78.56 |
| Qwen-Max | 阿里云 | 2025-01-27 | 闭源 | N/A | 57.74 | 76.00 | 73.50 | 73.11 |
| Hunyuan-Turbo | 腾讯混元 | 2025-01-10 | 闭源 | N/A | 60.34 | 66.53 | 72.55 | 68.71 |
| DeepSeek-R1 | 深度求索 | 2025-01-20 | 开源 | 671B | 53.76 | 69.72 | 70.22 | 68.43 |
| Qwen2.5-7b-Instruct | 阿里云 | 2024-09-19 | 开源 | 72B | 48.18 | 66.82 | 67.12 | 65.18 |
| Doubao-1.5-pro-32K | 字节跳动 | 2025-01-22 | 闭源 | N/A | 55.47 | 63.25 | 68.94 | 65.13 |
| MiniMax-Text-01 | 稀宇科技 | 2025-01-15 | 开源 | 456B | 45.32 | 64.77 | 64.92 | 62.99 |
| Yi-Lightning | 零一万物 | 2024-10-16 | 闭源 | N/A | 46.40 | 60.44 | 64.92 | 61.16 |
| GLM-4-Plus | 智谱AI | 2024-08-29 | 闭源 | 130B | 41.44 | 61.09 | 63.19 | 60.18 |
| GPT-4o | OpenAI | 2024-05-14 | 闭源 | N/A | 37.01 | 59.49 | 58.77 | 57.02 |
| Moonshot-v1-128k | 月之暗面 | 2014-01-31 | 闭源 | N/A | 34.55 | 50.66 | 55.78 | 51.48 |
| Spark4.0-Ultra | 科大讯飞 | 2024-06-27 | 闭源 | N/A | 42.25 | 41.55 | 56.45 | 48.43 |
| Mistral Large 2 | Mistral AI | 2024-09-19 | 闭源 | 128B | 35.89 | 48.89 | 51.01 | 47.83 |
| ERNIE-Speed-Pro-128K | 百度 | 2024-03-14 | 闭源 | N/A | 31.84 | 46.62 | 48.27 | 45.97 |
## Engineering Management and Construction
| 模型名称 | 组织/团队名称 | 发布日期 | 类型 | 参数量 | 造价工程师 | 咨询工程师 | 建造师 | 综合得分 |
|---------|-------------|----------|------|--------|------------|------------|--------|----------|
| CivilGPT | 同济大学土木工程学院 | 2024-11-09 | 闭源 | 72B | 64.11 | 75.69 | 80.14 | 74.77 |
| Qwen-Max | 阿里云 | 2025-01-27 | 闭源 | N/A | 56.60 | 66.78 | 79.72 | 71.06 |
| Hunyuan-Turbo | 腾讯混元 | 2025-01-10 | 闭源 | N/A | 52.95 | 68.32 | 76.68 | 68.53 |
| Qwen2.5-7b-Instruct | 阿里云 | 2024-09-19 | 开源 | 72B | 51.82 | 71.22 | 71.87 | 65.91 |
| Doubao-1.5-pro-32K | 字节跳动 | 2025-01-22 | 闭源 | N/A | 48.80 | 64.82 | 75.56 | 65.71 |
| DeepSeek-R1 | 深度求索 | 2025-01-20 | 开源 | 671B | 42.70 | 64.70 | 76.29 | 64.17 |
| MiniMax-Text-01 | 稀宇科技 | 2025-01-15 | 开源 | 456B | 48.19 | 65.44 | 69.16 | 62.63 |
| Yi-Lightning | 零一万物 | 2024-10-16 | 闭源 | N/A | 45.15 | 63.42 | 66.31 | 59.22 |
| GLM-4-Plus | 智谱AI | 2024-08-29 | 闭源 | 130B | 47.18 | 65.00 | 63.67 | 58.72 |
| GPT-4o | OpenAI | 2024-05-14 | 闭源 | N/A | 42.61 | 59.09 | 57.06 | 52.35 |
| Moonshot-v1-128k | 月之暗面 | 2014-01-31 | 闭源 | N/A | 36.20 | 57.21 | 53.31 | 47.75 |
| Spark4.0-Ultra | 科大讯飞 | 2024-06-27 | 闭源 | N/A | 34.02 | 53.01 | 46.99 | 44.94 |
| Mistral Large 2 | Mistral AI | 2024-09-18 | 闭源 | 128B | 33.77 | 48.51 | 44.83 | 41.57 |
| ERNIE-Speed-Pro-128K | 百度 | 2024-03-14 | 闭源 | N/A | 30.51 | 43.90 | 43.70 | 39.61 |
## Surveying and Geoinformatics
| 模型名称 | 组织/团队名称 | 发布日期 | 类型 | 参数量 | 测绘案例分析 | 测绘管理与法律法规 | 测绘综合能力 | 综合得分 |
|---------|-------------|----------|------|--------|--------------|------------------|--------------|----------|
| CivilGPT | 同济大学土木工程学院 | 2024-11-09 | 闭源 | 72B | 73.17 | 88.25 | 87.54 | 82.99 |
| Qwen-Max | 阿里云 | 2025-01-27 | 闭源 | N/A | 76.80 | 76.23 | 86.43 | 79.82 |
| DeepSeek-R1 | 深度求索 | 2025-01-20 | 开源 | 671B | 71.59 | 80.07 | 73.21 | 74.96 |
| Qwen2.5-7b-Instruct | 阿里云 | 2024-09-19 | 开源 | 72B | 63.96 | 81.35 | 78.23 | 74.51 |
| Hunyuan-Turbo | 腾讯混元 | 2025-01-10 | 闭源 | N/A | 60.31 | 84.54 | 73.46 | 72.77 |
| MiniMax-Text-01 | 稀宇科技 | 2025-01-15 | 开源 | 456B | 68.27 | 68.46 | 79.43 | 72.05 |
| Yi-Lightning | 零一万物 | 2024-10-16 | 闭源 | N/A | 65.69 | 75.27 | 70.77 | 70.58 |
| Doubao-1.5-pro-32K | 字节跳动 | 2025-01-22 | 闭源 | N/A | 52.21 | 82.56 | 74.20 | 69.66 |
| GLM-4-Plus | 智谱AI | 2024-08-29 | 闭源 | 130B | 69.31 | 59.39 | 78.03 | 68.91 |
| Moonshot-v1-128k | 月之暗面 | 2014-01-31 | 闭源 | N/A | 62.20 | 45.33 | 57.86 | 55.13 |
| GPT-4o | OpenAI | 2024-05-14 | 闭源 | N/A | 61.55 | 39.40 | 45.10 | 48.69 |
| ERNIE-Speed-Pro-128K | 百度 | 2024-03-14 | 闭源 | N/A | 54.27 | 50.98 | 38.71 | 47.99 |
| Spark4.0-Ultra | 科大讯飞 | 2024-06-27 | 闭源 | N/A | 62.82 | 45.51 | 33.47 | 47.27 |
| Mistral Large 2 | Mistral AI | 2024-09-18 | 闭源 | 128B | 58.98 | 30.57 | 48.67 | 46.07 |
## Architecture and Structural Design
| 模型名称 | 组织/团队名称 | 发布日期 | 类型 | 参数量 | 注册结构工程师 | 注册建筑师 | 城乡规划师 | 综合得分 |
|---------|-------------|----------|------|--------|----------------|------------|------------|----------|
| CivilGPT | 同济大学土木工程学院 | 2024-11-09 | 闭源 | 72B | 62.32 | 87.92 | 78.29 | 75.92 |
| Qwen-Max | 阿里云 | 2025-01-27 | 闭源 | N/A | 52.90 | 88.09 | 75.13 | 71.65 |
| Doubao-1.5-pro-32K | 字节跳动 | 2025-01-22 | 闭源 | N/A | 55.70 | 84.50 | 68.29 | 69.65 |
| Hunyuan-Turbo | 腾讯混元 | 2025-01-10 | 闭源 | N/A | 53.55 | 83.67 | 70.95 | 69.20 |
| Qwen2.5-7b-Instruct | 阿里云 | 2024-09-19 | 开源 | 72B | 49.70 | 81.83 | 67.82 | 66.28 |
| DeepSeek-R1 | 深度求索 | 2025-01-20 | 开源 | 671B | 43.15 | 83.68 | 73.56 | 65.95 |
| MiniMax-Text-01 | 稀宇科技 | 2025-01-15 | 开源 | 456B | 50.48 | 74.97 | 73.01 | 65.30 |
| GLM-4-Plus | 智谱AI | 2024-08-29 | 闭源 | 130B | 48.06 | 73.61 | 67.12 | 62.41 |
| Yi-Lightning | 零一万物 | 2024-10-16 | 闭源 | N/A | 47.84 | 70.78 | 65.54 | 60.87 |
| GPT-4o | OpenAI | 2024-05-14 | 闭源 | N/A | 41.24 | 69.33 | 57.89 | 55.94 |
| Moonshot-v1-128k | 月之暗面 | 2014-01-31 | 闭源 | N/A | 43.26 | 64.47 | 56.93 | 54.63 |
| Mistral Large 2 | Mistral AI | 2024-09-18 | 闭源 | 128B | 39.93 | 55.49 | 52.53 | 48.92 |
| ERNIE-Speed-Pro-128K | 百度 | 2024-03-14 | 闭源 | N/A | 38.34 | 57.60 | 48.62 | 48.13 |
| Spark4.0-Ultra | 科大讯飞 | 2024-06-27 | 闭源 | N/A | 34.99 | 57.44 | 53.41 | 48.01 |
## Civil Engineering
| 模型名称 | 组织/团队名称 | 发布日期 | 类型 | 参数量 | 岩土 | 水利水电工程 | 道路工程 | 公共基础 | 综合得分 |
|---------|-------------|----------|------|--------|------|--------------|----------|----------|----------|
| CivilGPT | 同济大学土木工程学院 | 2024-11-09 | 闭源 | 72B | 60.67 | 69.29 | 66.89 | 86.78 | 66.43 |
| Doubao-1.5-pro-32K | 字节跳动 | 2025-01-22 | 闭源 | N/A | 53.54 | 75.95 | 58.53 | 75.56 | 61.18 |
| Qwen-Max | 阿里云 | 2025-01-27 | 闭源 | N/A | 52.79 | 70.00 | 52.58 | 86.76 | 58.73 |
| Hunyuan-Turbo | 腾讯混元 | 2025-01-10 | 闭源 | N/A | 51.50 | 64.77 | 55.47 | 80.13 | 57.62 |
| MiniMax-Text-01 | 稀宇科技 | 2025-01-15 | 开源 | 456B | 52.92 | 57.29 | 53.75 | 73.58 | 55.69 |
| DeepSeek-R1 | 深度求索 | 2025-01-20 | 开源 | 671B | 45.78 | 67.69 | 50.14 | 89.67 | 54.90 |
| Qwen2.5-7b-Instruct | 阿里云 | 2024-09-19 | 开源 | 72B | 46.95 | 59.94 | 52.60 | 82.24 | 54.10 |
| Yi-Lightning | 零一万物 | 2024-10-16 | 闭源 | N/A | 50.00 | 52.55 | 53.05 | 76.42 | 53.61 |
| GLM-4-Plus | 智谱AI | 2024-08-29 | 闭源 | 130B | 48.26 | 52.39 | 48.20 | 73.15 | 51.04 |
| GPT-4o | OpenAI | 2024-05-14 | 闭源 | N/A | 39.62 | 48.25 | 48.57 | 66.47 | 46.33 |
| Moonshot-v1-128k | 月之暗面 | 2014-01-31 | 闭源 | N/A | 37.07 | 38.19 | 46.49 | 59.13 | 42.12 |
| Mistral Large 2 | Mistral AI | 2024-09-18 | 闭源 | 128B | 36.05 | 37.00 | 42.81 | 67.72 | 40.99 |
| ERNIE-Speed-Pro-128K | 百度 | 2024-03-14 | 闭源 | N/A | 34.85 | 33.92 | 41.03 | 52.94 | 38.14 |
| Spark4.0-Ultra | 科大讯飞 | 2024-06-27 | 闭源 | N/A | 28.31 | 41.99 | 29.71 | 50.35 | 33.14 |
## Environmental Engineering
| 模型名称 | 组织/团队名称 | 发布日期 | 类型 | 参数量 | 案例分析 | 相关法律法规 | 技术方法 | 技术导则与标准 | 综合得分 |
|---------|-------------|----------|------|--------|----------|--------------|----------|----------------|----------|
| CivilGPT | 同济大学土木工程学院 | 2024-11-09 | 闭源 | 72B | 59.53 | 83.96 | 71.32 | 84.60 | 74.86 |
| Qwen-Max | 阿里云 | 2025-01-27 | 闭源 | N/A | 52.87 | 81.96 | 73.83 | 74.55 | 70.80 |
| DeepSeek-R1 | 深度求索 | 2025-01-20 | 开源 | 671B | 56.00 | 75.53 | 83.16 | 66.82 | 70.38 |
| Hunyuan-Turbo | 腾讯混元 | 2025-01-10 | 闭源 | N/A | 39.20 | 83.05 | 72.54 | 83.50 | 69.57 |
| Doubao-1.5-pro-32K | 字节跳动 | 2025-01-22 | 闭源 | N/A | 36.53 | 70.30 | 73.07 | 69.74 | 62.41 |
| Qwen2.5-7b-Instruct | 阿里云 | 2024-09-19 | 开源 | 72B | 39.80 | 73.31 | 63.10 | 73.28 | 62.37 |
| Yi-Lightning | 零一万物 | 2024-10-16 | 闭源 | N/A | 52.00 | 59.47 | 67.64 | 63.39 | 60.62 |
| MiniMax-Text-01 | 稀宇科技 | 2025-01-15 | 开源 | 456B | 33.47 | 73.67 | 68.30 | 66.19 | 60.41 |
| GLM-4-Plus | 智谱AI | 2024-08-29 | 闭源 | 130B | 48.73 | 58.98 | 59.72 | 57.47 | 56.22 |
| Mistral Large 2 | Mistral AI | 2024-09-18 | 闭源 | 128B | 48.47 | 54.64 | 56.78 | 57.62 | 54.38 |
| GPT-4o | OpenAI | 2024-05-14 | 闭源 | N/A | 29.00 | 50.68 | 51.25 | 57.09 | 47.01 |
| Moonshot-v1-128k | 月之暗面 | 2014-01-31 | 闭源 | N/A | 30.47 | 46.22 | 52.10 | 56.87 | 46.42 |
| ERNIE-Speed-Pro-128K | 百度 | 2024-03-14 | 闭源 | N/A | 31.00 | 45.33 | 47.68 | 39.84 | 40.96 |
| Spark4.0-Ultra | 科大讯飞 | 2024-06-27 | 闭源 | N/A | 33.47 | 58.47 | 18.87 | 52.50 | 40.83 |

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.