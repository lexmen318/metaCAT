# -*- coding:utf-8 -*-

import os
from utils import comm_util


def generate_new_turn(usr_text, usr_domains, sys_text, sys_domains):
    default_turn = {
        "usr": {
            "text": usr_text,
            "general": [],
            "domains": usr_domains,
            "slots": {},
            "turn_info": {'status': 'SUCCESS', 'desc': ''}
        },
        "sys": {
            "text": sys_text,
            "general": [],
            "domains": sys_domains,
            "slots": {},
            "turn_info": {'status': 'SUCCESS', 'desc': ''}
        }
    }

    return default_turn


class DataLoader(object):

    @staticmethod
    def load_raw_data(raw_file_name):
        usr_domains = []
        sys_domains = []

        raw_json = comm_util.load_json_file(raw_file_name)

        batch = dict()
        for dialogue_id, dialogue_list in raw_json.items():
            turns = []
            for dialogue_text in dialogue_list:
                usr_text = dialogue_text['usr']
                sys_text = dialogue_text['sys']
                new_turn = generate_new_turn(usr_text, usr_domains, sys_text, sys_domains)
                # print(new_turn)
                turns.append(new_turn)

            batch[dialogue_id] = {'turns': turns}

        return batch


if __name__ == '__main__':
    raw_file_name = "d:/test_data/1594115108376.json"
    batch = DataLoader.load_raw_data(raw_file_name)
    print(batch)
