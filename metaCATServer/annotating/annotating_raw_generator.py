# -*- coding:utf-8 -*-

import json
import time
from typing import Dict, List, Any, Tuple, Hashable, Iterable, Union


def get_timestamp_key():
    current_milli_time = int(round(time.time() * 1000))
    return str(current_milli_time)


def save_json_cn_file(obj: Any, path: str) -> None:
    """Saves a JSON file."""
    with open(path, "w", encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def load_raw_data(raw_file_name):
    line_array = []
    with open(raw_file_name, 'r', encoding='utf-8') as lines:  # 一次性读入txt文件，并把内容放在变量lines中
        line_array = lines.readlines()  # 返回的是一个列表，该列表每一个元素是txt文件的每一行

    batch = {}
    dialogue_index = 0
    for line in line_array:
        dialogue_id = "Dialogue_" + get_timestamp_key() + str(dialogue_index)
        dialogue_index += 1

        raw_json = json.loads(line, encoding='utf-8')
        texts = raw_json['text']
        dialogue_text = []
        for text in texts:
            dialogue_text.append({
                "usr": text,
                "sys": ""
            })

        batch[dialogue_id] = dialogue_text

    return batch


if __name__ == '__main__':
    raw_file_name = "d:/test_data/raw_data.txt"
    batch = load_raw_data(raw_file_name)
    batch_file = "d:/test_data/" + get_timestamp_key() + ".json"

    print(batch)
    save_json_cn_file(batch, batch_file)
