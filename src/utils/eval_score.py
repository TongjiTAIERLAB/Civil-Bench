import os
import json
import pandas as pd
def get_full_score_dict(quiz_dir):
    df = pd.DataFrame(columns=['quiz_type','quiz_name','full_score'])
    quiz_type_ls = os.listdir(quiz_dir)
    for quiz_type in quiz_type_ls:
        quiz_name_ls = os.listdir(os.path.join(quiz_dir, quiz_type))
        for quiz_name in quiz_name_ls:
            quiz_path = os.path.join(quiz_dir, quiz_type, quiz_name)
            with open(quiz_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            score = 0
            for question in data:
                score += question["score"]
            new_row = {'quiz_type':quiz_type,'quiz_name':quiz_name.split('.')[0],'full_score':score}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df


def get_score(output_dir):
    df = pd.DataFrame(columns=['quiz_type','quiz_name','score'])
    quiz_type_ls = os.listdir(output_dir)
    for quiz_type in quiz_type_ls:
        quiz_name_ls = os.listdir(os.path.join(output_dir, quiz_type))
        for quiz_name in quiz_name_ls:
            quiz_path = os.path.join(output_dir, quiz_type, quiz_name)
            with open(quiz_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                score = data["QuizScore"]
            new_row = {'quiz_type':quiz_type,'quiz_name':quiz_name.split('.')[0],'score':score}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

def merge_df(full_score_df,score_df,model_name):
    detailed_df = pd.merge(full_score_df,score_df,on=['quiz_type','quiz_name'],how='left')
    detailed_df['百分制'] = (detailed_df['score'].astype(float) / detailed_df['full_score'].astype(float) * 100).round(2)
    weighted_scores = detailed_df.groupby('quiz_type').apply(
    lambda x: (x['score'].sum() / x['full_score'].sum()) * 100).round(2)
    weighted_scores_df = weighted_scores.reset_index()
    weighted_scores_df.columns = ['题目类型', '加权得分']
    total_weighted_score = (detailed_df['score'].sum() / detailed_df['full_score'].sum() * 100).round(2)

    weighted_scores_df = pd.concat([weighted_scores_df, pd.DataFrame([{'题目类型': '加权总得分', '加权得分': total_weighted_score}])], ignore_index=True)
    if not os.path.exists(f"../score/{model_name}"):
        os.makedirs(f"../score/{model_name}")
    weighted_scores_df.to_csv(f"../score/{model_name}/weighted_scores.csv", index=False)
    detailed_df.to_csv(f"../score/{model_name}/detailed_scores.csv", index=False)
    print(weighted_scores_df)
    print(detailed_df)

def eval_score(quiz_dir,output_dir,model_name):
    full_score_df = get_full_score_dict(quiz_dir)
    score_df = get_score(output_dir)
    merge_df(full_score_df,score_df,model_name)


