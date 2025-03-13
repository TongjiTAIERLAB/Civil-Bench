from utils.utils import *
from utils.process_quiz import process_one_quiz_file, process_one_question, Objective_score, Subjective_score 
from utils.eval_score import eval_score
from llm_responsor.LLMTest import LLMFactory
import time
from dotenv import load_dotenv
import os

def main():
    start_time = time.time()
    logger = setup_logger()
    load_dotenv()
    test_model_name = os.getenv("test_model_name")
    test_api_key = os.getenv("test_model_api_key")
    test_model_url = os.getenv("test_model_url")
    teacher_model_name = os.getenv("teacher_model_name")
    teacher_model_api_key = os.getenv("teacher_model_api_key")
    teacher_model_url = os.getenv("teacher_model_url")

    data_dir = "../data"
    data_dict,file_num = load_data(data_dir)
    question_have_done_path = "./log/question_have_done.txt"
    logger.info(f"data_dict: {data_dict}")
    TestModel = LLMFactory.create(test_model_name, test_api_key, base_url=test_model_url)
    TeacherModel = LLMFactory.create(teacher_model_name, teacher_model_api_key, base_url=teacher_model_url)
    i = 0
    for quiz_type, quiz_name_list in data_dict.items():
        for quiz_name in quiz_name_list:
            logger.info(f"Processing quiz: {quiz_name} {i}/{file_num}")
            print(f"Processing quiz:{quiz_type} {quiz_name}")
            process_one_quiz_file(data_dir, quiz_type, quiz_name, question_have_done_path, TestModel, TeacherModel, logger)
            i += 1
    end_time = time.time()
    logger.info(f"Total time: {end_time - start_time} seconds")
    eval_score(data_dir, f"../output/{test_model_name}", test_model_name)
    print(f"Total time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
