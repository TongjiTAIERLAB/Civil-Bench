from typing import List, Dict, Any, Tuple
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import os
from utils.utils import read_json_file, write_json_file
import re
from tqdm import tqdm

# from LLMTest_upload import BaseLLM

def process_one_quiz_file(data_dir:str,quiz_type:str,CurrentQuizName:str, question_have_done_path:str, 
                          TestModel,
                          TeacherModel,
                          logger: logging.Logger = None,
                          max_workers: int = 2) -> Tuple[Dict[str, Any], float]:
    """处理单个测试文件的函数"""
    CurrentQuiz = read_json_file(os.path.join(data_dir, quiz_type, CurrentQuizName))

    output_dir = os.path.join('../output', TestModel.ModelName,quiz_type)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.path.exists(os.path.join(output_dir, CurrentQuizName)):
        QuizScore = read_json_file(os.path.join(output_dir, CurrentQuizName))['QuizScore']
        QuizAnswers = read_json_file(os.path.join(output_dir, CurrentQuizName))['QuizAnswers']
    else:
        QuizScore = 0
        QuizAnswers = []
    
    
    # 准备题目处理参数
    questions_to_process = []
    if os.path.exists(question_have_done_path):
        with open(question_have_done_path, 'r', encoding='UTF-8') as f:
            Questions_have_done = f.readlines()
            Questions_have_done = [line.strip() for line in Questions_have_done]
    else:
        Questions_have_done = []
        with open(question_have_done_path, 'w', encoding='UTF-8') as f:
            pass
    for ID in range(len(CurrentQuiz)):
        # 检查是否已完成
        if (TestModel.ModelName + '-' + CurrentQuiz[ID]['unique_ID']) in Questions_have_done:
            continue
            
        question_data = CurrentQuiz[ID]
        
        
        # 准备参数
        args = (
            TestModel,
            TeacherModel,
            question_data,
            CurrentQuizName,
            logger
        )
        questions_to_process.append(args)
    logger.info(f"Processing {len(questions_to_process)} questions")


    # 使用线程池并行处理题目
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_question = {
            executor.submit(process_one_question, *args): args 
            for args in questions_to_process
        }
        with tqdm(total=len(questions_to_process), 
                 desc="Processing questions",
                 unit="q",  # 单位为问题
                 ncols=100,  # 进度条宽度
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            for future in as_completed(future_to_question):
                args = future_to_question[future]
                result = future.result()
                if result is not None:
                    QuizAnswers.append({
                        'question': args[2]['question'],
                        'model_response': result['model_analysis'],
                        'model_answer': result['model_answer'],
                        'model_score': result['model_score'],
                        'unique_ID': args[2]['unique_ID'],
                        'true_answer':args[2]['answer'],
                        'type': args[2]['type']
                    })
                    QuizScore += result['model_score']
                    
                    # 更新已完成题目列表
                    question_id = TestModel.ModelName + '-' + args[2]['unique_ID']
                    Questions_have_done.append(question_id)
                    with open(question_have_done_path, 'a', encoding='UTF-8') as f:
                        f.write(question_id + '\n')
                pbar.update(1)

    write_json_file(os.path.join(output_dir,CurrentQuizName), {'QuizAnswers': QuizAnswers, 'QuizScore': QuizScore})
    logger.info(f"Model {TestModel.ModelName} processed {CurrentQuizName} with {QuizScore} score")
    
    return QuizAnswers, QuizScore


def process_one_question(TestModel,TeacherModel,question_data,CurrentQuizName,logger=None):

    # 设置提示信息
    if question_data['type'] == 'single_choice':
        prompt = f'请你做一道土木工程师从业资格考试单项选择题。\n你将从A, B, C, D中选出正确的答案，并写在【答案】和【答案结束】之间。\n例如：【答案】 A 【答案结束】\n完整的题目回答的格式如下：\n【答案】 ... 【答案结束】\n请你严格按照上述格式作答，仅返回问题的答案即可，无需添加额外解释或前言。\n题目如下：{question_data["question"]}'
    elif question_data['type'] == 'multi_choice':
        prompt = f'请你做一道土木工程师从业资格考试多项选择题。\n你将从A, B, C, D ,E中选出所有符合题意的答案，并写在【答案】和【答案结束】之间。\n例如：【答案】 AB 【答案结束】\n完整的题目回答的格式如下：\n【答案】 ... 【答案结束】\n请你严格按照上述格式作答，仅返回问题的答案即可，无需添加额外解释或前言。\n题目如下：{question_data["question"]}'
    elif question_data['type'] == 'subjective':
        prompt = f'请你做一道土木工程师从业资格考试问答题。\n请你根据题目要求写出完整的答案，并写在【答案】和【答案结束】之间。\n例如：【答案】 ... 【答案结束】\n完整的题目回答的格式如下：【答案】 ... 【答案结束】\n请你严格按照上述格式作答。\n题目如下：{question_data["question"]}'
    else:
        raise ValueError(f"Question {question_data['index']} of Quiz {CurrentQuizName} has other type of question, which has type:{question_data['type']}")
    try:
        model_response = TestModel.call_with_messages(prompt)
        # logger.info(f"Model {TestModel.ModelName} in Question {question_data['index']} of Quiz {CurrentQuizName} has successfully responsed")
    except Exception as e:
        logger.error(f"Error getting answer for question {question_data['index']} with error {e}")
        return None
    
    if question_data['type'] == 'single_choice' or question_data['type'] == 'multi_choice':
        model_analysis, model_answer, model_score = Objective_score(model_response, question_data,TestModel.ModelName,CurrentQuizName,logger)
    elif question_data['type'] == 'subjective':
        model_analysis, model_answer, model_score = Subjective_score(model_response, question_data,TestModel.ModelName,TeacherModel,CurrentQuizName,logger)


    # 检查回答是否有效
    if ('Unsuccessful_response_obtained' in model_analysis or 
        'Unsuccessful_evalution_obtained' in model_analysis or 
        'Not outputted in format' in model_analysis or 
        'Incorrect rating' in model_analysis):
        return None

    # 返回处理结果
    return {
        'model_answer': model_answer,
        'model_analysis': model_analysis,
        'model_score': model_score,
    }


def Objective_score(raw_response, question_data,TestModelName,CurrentQuizName,logger):

    answer = question_data['answer'].upper()
    if raw_response == '':
        model_analysis = 'raw_response is empty'
        model_answer = ''
        model_score = 0
        return model_analysis, model_answer, model_score

    #单选题
    if question_data['type'] == 'single_choice':
        #try-except防止模型回答不符合规范导致程序崩溃
        try:
            #获取答案
            if '【答案】' in raw_response:
                if '【答案结束】' in raw_response:
                    model_answer = re.search(r'【答案】[(\s\S)]*【答案结束】', raw_response).group()
                else:
                    model_answer = re.search(r'【答案】[(\s\S)]*', raw_response).group()
 
            elif '【答案】' not in raw_response:
                if '【答案结束】' in raw_response:
                    model_answer = re.search(r'[(\s\S)]*【答案结束】', raw_response).group()
                elif '【答案结束】' not in raw_response:
                    model_answer = raw_response
            model_answer = re.sub(r'【答案】', '', model_answer)
            model_answer = re.sub(r'【答案结束】', '', model_answer)
            model_answer = re.sub(r'\s+', '', model_answer)
            temp_answer = re.findall(r'[A-Z]', model_answer)
            if len(temp_answer) > 0:
                model_answer = temp_answer[0]
            else:
                model_answer = model_answer

            #获取分数
            if model_answer == answer:
                model_score = question_data['score']
            else:
                model_score = 0
            
            #记录日志文件
            logger.info(f'Model:{TestModelName} in Question:{question_data["index"]} of Quiz:{CurrentQuizName} has successfully responsed with answer:{model_answer} and score:{model_score:.2f}/{question_data["score"]:.2f} corresponding to the standard answer:{answer}.')
        except:
            model_analysis = 'Not outputted in format:' + raw_response
            model_answer = ''
            model_score = 0
            logger.error(f'Model:{TestModelName} in Question:{question_data["index"]} of Quiz:{CurrentQuizName} has unformattedly responsed with answer:{model_answer} and score:{model_score:.2f}/{question_data["score"]:.2f} corresponding to the standard answer:{answer}.\n which has responses:{model_analysis}.')
    #多选题
    elif question_data['type'] == 'multi_choice':
        #try-except防止模型回答不符合规范导致程序崩溃
        try:
            #获取答案
            if '【答案】' in raw_response:
                if '【答案结束】' in raw_response:
                    model_answer = re.search(r'【答案】[(\s\S)]*【答案结束】', raw_response).group()
                elif '【答案结束】' not in raw_response:
                    model_answer = re.search(r'【答案】[(\s\S)]*', raw_response).group()
            elif '【答案】' not in raw_response:
                if '【答案结束】' in raw_response:
                    model_answer = re.search(r'[(\s\S)]*【答案结束】', raw_response).group()
                elif '【答案结束】' not in raw_response:
                    model_answer = raw_response
            model_answer = re.sub(r'【答案】', '', model_answer)
            model_answer = re.sub(r'【答案结束】', '', model_answer)
            model_answer = re.sub(r'\s+', '', model_answer)
            temp_answer = re.findall(r'[A-Z]', model_answer)
            if len(temp_answer) > 0:
                model_answer = ''
                for char in temp_answer:
                    model_answer += char
            else:
                model_answer = model_answer
            
            #获取分数
            num_char = 0
            for char in model_answer:
                if char in answer: #模型答案中当前字母在标准答案中
                    num_char += 1
            if num_char == len(model_answer) and len(model_answer) == len(answer): #多选题模型答案正确
                model_score = question_data['score']
            elif num_char == len(model_answer) and len(model_answer) < len(answer) and len(model_answer) != 0: #多选题模型答案部分正确
                model_score = question_data['score'] * 0.5
            elif num_char < len(model_answer) or len(model_answer) == 0: #多选题模型答案有错选或者没有选择
                model_score = 0
            
            #记录日志文件
            logger.info(f'Model:{TestModelName} in Question:{question_data["index"]} of Quiz:{CurrentQuizName} has successfully responsed with answer:{model_answer} and score:{model_score:.2f}/{question_data["score"]:.2f} corresponding to the standard answer:{answer}.')
        except:
            model_analysis = 'Not outputted in format:' + model_analysis
            model_answer = ''
            model_score = 0
            logger.error(f'Model:{TestModelName} in Question:{question_data["index"]} of Quiz:{CurrentQuizName} has unformattedly responsed with answer:{model_answer} and score:{model_score:.2f}/{question_data["score"]:.2f} corresponding to the standard answer:{answer}.\n which has responses:{model_analysis}.')
    else:
        logger.error(f'Model:{TestModelName} in Question:{question_data["index"]} of Quiz:{CurrentQuizName} has other type of question, which has type:{question_data["type"]}')   
        return "","",0
    
    return raw_response, model_answer, model_score



def Subjective_score(raw_response, question_data, TestModelName, TeacherModel, CurrentQuizName, logger):


    #try-except防止模型回答不符合规范导致程序崩溃
    try:
        if '【答案】' in raw_response:
            if '【答案结束】' in raw_response:
                model_answer = re.search(r'【答案】[(\s\S)]*【答案结束】', raw_response).group()
            elif '【答案结束】' not in raw_response:
                model_answer = re.search(r'【答案】[(\s\S)]*', raw_response).group()
        elif '【答案】' not in raw_response:
            if '【答案结束】' in raw_response:
                raw_response = re.search(r'[(\s\S)]*【答案结束】', raw_response).group()
            elif '【答案结束】' not in raw_response:
                raw_response = raw_response
        raw_response = re.sub(r'【答案】', '', raw_response)
        raw_response = re.sub(r'【答案结束】', '', raw_response)
        raw_response = re.sub(r'\s+', '', raw_response)
        model_answer = raw_response
        model_score = 0
    except Exception as e:
        model_answer = ''
        model_score = 0
        logger.error(f'Model:{TestModelName} in Question:{question_data["index"]} of Quiz:{CurrentQuizName} has unformattedly responsed.\n which has responses:{raw_response}.The error is:{e}')


        #信息设置
    eva_prompt = '你是一位专业的土木工程从业资格考试主观题阅卷人，\n请你根据标准答案对该考生给出的答案进行评分。我们将严格按照顺序给出【题目】、【标准答案】及【考生答案】。题目将在【题目】和【题目结束】之间给出，形如：【题目】 ... 【题目结束】；标准答案将在【标准答案】和【标准答案结束】之间给出，形如：【标准答案】 ... 【标准答案结束】；考生答案将在【考生答案】和【考生答案结束】之间给出，形如：【考生答案】 ... 【考生答案结束】。\n题目、标准答案及考生答案完整的信息格式如下：\n【题目】 ... 【题目结束】\n【标准答案】 ... 【标准答案结束】\n【考生答案】 ... 【考生答案结束】。\n当前题目满分为100分，请将该考生的得分写在【得分】和【得分结束】之间，考生得分必须小于等于满分，形式为：考生得分/满分。\n例如：【得分】 85/100 【得分结束】\n完整的打分格式的格式如下：\n【得分】 85/100 【得分结束】\n请你严格按照上述格式评分，仅返回考生的得分即可，无需添加额外解释或前言。\n题目、标准答案及考生答案如下：'
    eva_content = '【题目】' + question_data['question'] + '【题目结束】\n' + '【标准答案】' + question_data['answer'] + '【标准答案结束】\n' + '【考生答案】' + model_answer + '【考生答案结束】\n'
    eva_message = [{'role': 'system', 'content': eva_prompt},
                {'role': 'user', 'content': eva_content}]
    
        #得到响应结果
    try:
        temp_teacher_score = TeacherModel.call_with_messages(eva_message)
            

    except Exception as e:

        logger.error(f'Model:{TestModelName} in Question:{question_data["index"]} of Quiz:{CurrentQuizName} has failed to evaluate.\n which has answer:{raw_response}.The error is:{e}')
        return raw_response, model_answer, 0

    #获取分数
    temp_teacher_score = re.sub(r'\s+', '', temp_teacher_score)
    temp_teacher_score = re.search(r'【得分】[(\s\S)]*', temp_teacher_score).group()
    temp_teacher_score = re.sub(r'【得分】', '', temp_teacher_score)
    temp_teacher_score = re.sub(r'【得分结束】', '', temp_teacher_score)
    temp_teacher_score = re.sub(r'\s+', '', temp_teacher_score)
    final = temp_teacher_score.strip().split('/')
    model_score = float(final[0]) / 100 * question_data['score']

    #记录日志文件
    logger.info(f'Model:{TestModelName} in Subjective Question:{question_data["index"]} of Quiz:{CurrentQuizName} has successfully responsed with score:{model_score:.2f}/{question_data["score"]:.2f}.')

    return raw_response, model_answer, model_score