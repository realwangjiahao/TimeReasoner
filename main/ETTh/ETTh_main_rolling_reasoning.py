import pandas as pd
from utils.api_ouput import deepseek_api_output
import json
import os
import re


def get_result(text):
    res_list = []
    pattern = r"```([\s\S]*?)```"
    match = re.search(pattern, text)
    if match is None:
        pattern = r"\|.*\|" 
        text_list = re.findall(pattern, text)
    else:
        text = match.group(1).strip()
        text_list = text.split('\n')
    
    for _, item in enumerate(text_list):
        item = item.strip()
        if item.endswith('|'):
            item = item.rstrip('|').strip()
        match = re.search(r'(-?\d+\.\d+|-?\d+)$', item)
        if match:
            number = float(match.group(0))
            res_list.append(number)
    return res_list







meaning_dict={'HUFL':'High UseFul Load','HULL':'High UseLess Load','MUFL':'Middle UseFul Load',
              'MULL':'Middle UseLess Load','LUFL':'Low UseFul Load','LULL':'Low UseLess Load','OT':'Oil Temperature'}

def ETTh_main_eng_rolling_reasoning(data_name,attr,look_back,pred_window,number,api_key,step_num,step):

    data_dir = '/dataset/ETT-small/' + data_name + '.csv'
    data = pd.read_csv(data_dir)
    data = data[12 * 30 * 24 + 4 * 30 * 24 - look_back : 12 * 30 * 24 + 8 * 30 * 24]
    date = data.loc[:, 'date'].to_numpy()
    attr_data = data.loc[:, attr].to_numpy()
    data = pd.DataFrame(date, columns=['date'])
    data[attr] = attr_data
    data_lookback = []
    for i in range(10):
        data_lookback.append(data.iloc[i * look_back:(i + 1) * look_back])
    step_length=pred_window//step_num
    


    
    if step==1:
        prompt=''
        prompt +='Here is the '+meaning_dict[attr]+' data of the transformer.'
        prompt +=f'I will now give you data for the past {look_back} recorded dates, and please help me forecast the data for next {step_length} recorded dates, remember to give me the complete data.'
        prompt +='The data is as follows:'
        prompt += data_lookback[number].to_string(index=False)
        prompt +='And your final answer must follow the format'
        prompt+="""
        <answer>
            \n```\n
            ...
            \n```\n
        </answer>
        Please obey the format strictly. And you must give me the complete answer.
        """

    elif step==2:
        prompt=''
        prompt +='Here is the '+meaning_dict[attr]+' data of the transformer.'
        prompt +=f'I will now give you data for the past {look_back+step_length} recorded dates, and please help me forecast the data for next {step_length} recorded dates, remember to give me the complete data.'
        with open(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json', 'r') as f:
            answer=json.load(f)
        answer_1=get_result(answer[0]['answer1'])
        answer_1=str(answer_1)
        prompt +='The data is as follows:'
        prompt += data_lookback[number].to_string(index=False)
        prompt += answer_1
        prompt +='And your final answer must follow the format'
        prompt+="""
        <answer>
            \n```\n
            ...
            \n```\n
        </answer> 
        Please obey the format strictly. And you must give me the complete answer.
        """


    elif step==3:
        prompt=''
        prompt +='Here is the '+meaning_dict[attr]+' data of the transformer.'
        prompt +=f'I will now give you data for the past {look_back+step_length*2} recorded dates, and please help me forecast the data for next {step_length} recorded dates, remember to give me the complete data.'
        
        with open(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json', 'r') as f:
            answer=json.load(f)
        answer_1=get_result(answer[0]['answer1'])
        answer_2=get_result(answer[1]['answer2'])
        
        prompt +='The data is as follows:'  
        prompt += data_lookback[number].to_string(index=False)
        prompt += str(answer_1)
        prompt += str(answer_2)
        
        prompt +='And your final answer must follow the format'
        prompt+="""
        <answer>
            \n```\n
            ...
            \n```\n
        </answer> 
        Please obey the format strictly. And you must give me the complete answer.
        """
    
    elif step==4:
        prompt=''
        prompt +='Here is the '+meaning_dict[attr]+' data of the transformer.'
        prompt +=f'I will now give you data for the past {look_back+step_length*3} recorded dates, and please help me forecast the data for next {step_length} recorded dates, remember to give me the complete data.'  

        with open(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json', 'r') as f:
            answer=json.load(f)
        answer_1=get_result(answer[0]['answer1'])
        answer_2=get_result(answer[1]['answer2'])
        answer_3=get_result(answer[2]['answer3'])

        prompt +='The data is as follows:'
        prompt += data_lookback[number].to_string(index=False)
        prompt += str(answer_1)
        prompt += str(answer_2)
        prompt += str(answer_3)

        prompt +='And your final answer must follow the format'
        prompt+="""
        <answer>
            \n```\n
            ...
            \n```\n
        </answer> 
        Please obey the format strictly. And you must give me the complete answer.
        """

    else:
        print('The step number is not correct!')
        return
    
    if not os.path.exists(f'/output/rolling/prompt/{data_name}'):
        os.makedirs(f'/output/rolling/prompt/{data_name}')
    if not os.path.exists(f'/output/rolling/result/{data_name}'):
        os.makedirs(f'/output/rolling/result/{data_name}')


    with open(f'/output/rolling/prompt/{data_name}/prompt_{attr}_{data_name}_{look_back}_{pred_window}_{number}_step_{step}.txt', 'w') as f:
        f.write(prompt)
        
    model=deepseek_api_output(api_key=api_key)
    answer=[]

    if os.path.exists(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json'):
        with open(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json', 'r') as f:
            answer=json.load(f)
        if len(answer)==step_num:
            print('This task has been done!')
            return
        else:
            len_answer=len(answer)
    else:
        len_answer=0

    if step<=len_answer:
        print('This task has been done!')
        return
    else:
        if step==1:
            reasoning1,result1=model(prompt)
            while len(get_result(result1))!=step_length:
                reasoning1,result1=model(prompt)
            answer.append({'reasoning1':reasoning1,'answer1':result1})
            with open(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json', 'w') as f:
                json.dump(answer, f,indent=4)

        elif step==2:
            reasoning2,result2=model(prompt)
            while len(get_result(result2))!=step_length:
                reasoning2,result2=model(prompt)
            answer.append({'reasoning2':reasoning2,'answer2':result2})
            with open(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json', 'w') as f:
                json.dump(answer, f,indent=4)

        elif step==3:
            reasoning3,result3=model(prompt)
            while len(get_result(result3))!=step_length:
                reasoning3,result3=model(prompt)
            answer.append({'reasoning3':reasoning3,'answer3':result3})
            with open(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json', 'w') as f:
                json.dump(answer, f,indent=4)

        elif step==4:
            reasoning4,result4=model(prompt)
            while len(get_result(result4))!=step_length:
                reasoning4,result4=model(prompt)
            answer.append({'reasoning4':reasoning4,'answer4':result4})
            with open(f'/output/rolling/result/{data_name}/result_{attr}_{data_name}_{look_back}_{pred_window}_{number}_rolling_reasoning.json', 'w') as f:
                json.dump(answer, f,indent=4)
        else:
            print('The step number is not correct!')
            return