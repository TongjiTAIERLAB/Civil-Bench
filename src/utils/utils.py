import json
import os
import logging
from logging.handlers import RotatingFileHandler

def load_data(data_dir):
    data_dict = {}
    file_num = 0
    for first_level in os.listdir(data_dir):
        if os.path.isdir(os.path.join(data_dir, first_level)):
            sub_dimension_ls = []
            for second_level in os.listdir(os.path.join(data_dir, first_level)):
                if second_level.endswith('.json'):
                    sub_dimension_ls.append(second_level)
                    file_num += 1
            data_dict[first_level] = sub_dimension_ls
    return data_dict,file_num

def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True


def setup_logger(logger_name = 'main'):
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    # 使用 RotatingFileHandler 而不是 FileHandler
    file_handler = logging.handlers.RotatingFileHandler(
        f'log/{logger_name}.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
    )
    file_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


