from concurrent.futures import ThreadPoolExecutor
from main.ETTh.ETTh_main_one_shot_reasoning import ETTh_main_eng_short


data_name = 'ETTh1'
look_back, pred_window = 96, 96
api_key = ''


def run_task(i, attr):
    ETTh_main_eng_short(data_name, attr, look_back, pred_window, i, api_key=api_key)

tasks = [(i, attr) for i in range(10) for attr in ['HUFL', 'HULL', 'MUFL', 'MULL', 'LUFL', 'LULL', 'OT']]

with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(lambda p: run_task(*p), tasks)
  