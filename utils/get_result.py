import re

def get_result(text):
    res_list = []
    pattern = r"```*([\s\S]*?)```"
    match = re.search(pattern, text)
    if match is None:
        pattern = r"\|.*\|"
        text_list = re.findall(pattern, text)
    else:
        text = match.group(1).strip()
        text_list = text.split('\n')
    
    for index, item in enumerate(text_list):
        if index == 0:
            continue
        item = item.strip()
        if item.endswith('|'):
            item = item.rstrip('|').strip()
        match = re.search(r'(-?\d+\.\d+|-?\d+)$', item)
        if match:
            number = float(match.group(0))
            res_list.append(number)
    
    return res_list