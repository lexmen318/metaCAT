# -*- coding:utf-8 -*-
##############################################
# paraphrasing validator
##############################################

import binascii
import collections
import difflib
from flask_babel import gettext, ngettext

general_diff_ratio = 0.3
general_diff_length = 0.5
trimmed_diff_ratio = 0.15
trimmed_diff_length = 0.3
least_english_space_count = 4

lst_special_slot_value = ['dontcare', 'unknown', 'unk', 'n/a', 'none', 'yes', 'no']


def get_word_ratio(tkl1, tkl2):
    all_seq = list(set(tkl1 + tkl2))

    tok_to_hexid = collections.OrderedDict(
        [(tok, binascii.a2b_hex('{0:02x}'.format(idx))) for idx, tok in enumerate(all_seq)])

    seq1 = list(tok_to_hexid.get(t) for t in tkl1)
    seq2 = list(tok_to_hexid.get(t) for t in tkl2)

    str1 = b''.join(seq1)
    str2 = b''.join(seq2)

    word_ratio = difflib.SequenceMatcher(a=str1, b=str2).quick_ratio()

    return word_ratio


# 暂时不允许槽位之间发生重叠或包含现象
def judge_repeat_span(para_obj, slot_name, slot_span):
    for slot, item in para_obj['single_slot'].items():
        if slot == slot_name or item[1] == 0 and item[2] == 0:
            continue
        if item[1] <= slot_span[0] < item[2] or item[1] < slot_span[1] <= item[2]:
            return True

    if 'batch_slot' in para_obj.keys():
        for slot, item_lst in para_obj['batch_slot'].items():
            for item in item_lst:
                if slot == slot_name and item[1] == slot_span[0] and item[2] == slot_span[1]:
                    continue
                if item[1] <= slot_span[0] < item[2] or item[1] < slot_span[1] <= item[2]:
                    return True

    return False


def get_slot_length_sum(dialogue):
    ret_len = 0
    for slot, item in dialogue['single_slot'].items():
        if item[1] == 0 and item[2] == 0:
            continue
        ret_len += item[2] - item[1]

    for slot, item_lst in dialogue['batch_slot'].items():
        for item in item_lst:
            if item[1] == 0 and item[2] == 0:
                continue
            ret_len += item[2] - item[1]
    return ret_len


def validate_turn(src_dialogue, para_dialogue, role='usr'):
    lst_missing_slot = []
    lst_missing_value = []
    lst_missing_src = []
    lst_repeat_span = []
    lst_wrong_span = []
    lst_extra_slot = []
    lst_extra_value = []

    src_len, para_len = len(src_dialogue['text']), len(para_dialogue['text'])

    diff_length, diff_ratio = general_diff_length, general_diff_ratio
    slot_len_sum = get_slot_length_sum(src_dialogue)
    if slot_len_sum >= src_len * 0.5:  # 槽位总长度超过对话文本的一半
        diff_length, diff_ratio = trimmed_diff_length, trimmed_diff_ratio

    if role == 'sys':
        diff_length, diff_ratio = diff_length / 2.0, diff_ratio / 2.0

    if para_dialogue['text'] == '':
        return {'status': 'FAILED', 'error': gettext(u'errorNoParaphrasing')}
    if para_len < src_len * diff_length:
        return {'status': 'FAILED', 'error': gettext(u'errorIncompleteParaphrasing')}

    src_space_count = src_dialogue['text'].count(' ')
    para_space_count = para_dialogue['text'].count(' ')
    if src_space_count >= least_english_space_count or para_space_count >= least_english_space_count:
        sm_ratio = get_word_ratio(src_dialogue['text'].split(), para_dialogue['text'].split())
    else:
        sm_ratio = difflib.SequenceMatcher(a=src_dialogue['text'], b=para_dialogue['text']).quick_ratio()

    if sm_ratio > 1 - diff_ratio:
        return {'status': 'FAILED', 'error': gettext(u'errorParaphrasingLackChange')}

    for slot, item in para_dialogue['single_slot'].items():
        if item[1] == '':
            item[1] = 0
        else:
            item[1] = int(item[1])
        if item[2] == '':
            item[2] = 0
        else:
            item[2] = int(item[2])
        para_dialogue['single_slot'][slot] = item

    for slot, item_lst in para_dialogue['batch_slot'].items():
        for idx in range(len(item_lst)):
            if item_lst[idx][1] == '':
                item_lst[idx][1] = 0
            else:
                item_lst[idx][1] = int(item_lst[idx][1])
            if item_lst[idx][2] == '':
                item_lst[idx][2] = 0
            else:
                item_lst[idx][2] = int(item_lst[idx][2])

    for slot, item in src_dialogue['single_slot'].items():
        if item[1] == 0 and item[2] == 0:
            continue
        if slot not in para_dialogue['single_slot'].keys():
            lst_missing_slot.append(slot)
        para_item = para_dialogue['single_slot'][slot]
        if para_item[0] == '' or para_item[0] == para_item[1] == 0:
            lst_missing_slot.append(slot)
            continue
        if item[3] != '' and para_item[3] == '':
            lst_missing_src.append(slot)
        if para_item[1] >= para_item[2] or para_dialogue['text'][para_item[1]:para_item[2]] != para_item[0]:
            if para_item[0] not in lst_special_slot_value:
                lst_wrong_span.append(slot)
        elif judge_repeat_span(para_dialogue, slot, para_item[1:3]):
            lst_repeat_span.append(slot)

    if 'batch_slot' in src_dialogue.keys():
        for slot, item_lst in src_dialogue['batch_slot'].items():
            if 'batch_slot' not in para_dialogue.keys():  # or slot not in para_dialogue['batch_slot'].keys():
                lst_missing_slot.append(slot)
                continue
            if slot not in para_dialogue['batch_slot'].keys():
                continue
            para_item_lst = para_dialogue['batch_slot'][slot]
            real_para_item_lst = [item for item in para_item_lst if item[0] != '']
            src_value_num = len(item_lst)
            para_value_num = len(real_para_item_lst)
            if para_value_num == 0:
                lst_missing_slot.append(slot)
            # elif src_value_num > para_value_num:
            #     lst_missing_value.append(slot)
            elif src_value_num < para_value_num:
                lst_extra_value.append(slot)

            for item in real_para_item_lst:
                if item[0] == '':
                    continue
                if item[1] >= item[2] or para_dialogue['text'][item[1]:item[2]] != item[0]:
                    if item[0] not in lst_special_slot_value:
                        lst_wrong_span.append(slot)
                elif judge_repeat_span(para_dialogue, slot, item[1:3]):
                    lst_repeat_span.append(slot)

    for slot, item in para_dialogue['single_slot'].items():
        if item[1] == 0 and item[2] == 0:
            continue

        if slot not in src_dialogue['single_slot'].keys():
            lst_extra_slot.append(slot)

    if 'batch_slot' in para_dialogue.keys():
        for slot, item_lst in para_dialogue['batch_slot'].items():
            if slot not in src_dialogue['batch_slot'].keys():
                lst_extra_slot.append(slot)

    str_error = ''
    if lst_missing_slot:
        str_error += gettext(u'errorNotAnnotatedSlot') + ": " + '、'.join(lst_missing_slot) + '。'
    if lst_missing_value:
        str_error += gettext(u'errorNoSlotValue') + ": " + '、'.join(lst_missing_value) + '。'
    if lst_missing_src:
        str_error += gettext(u'errorNoRealValue') + ": " + '、'.join(lst_missing_src) + '。'
    if lst_repeat_span:
        str_error += gettext(u'errorRepeatSpan') + ": " + '、'.join(lst_repeat_span) + '。'
    if lst_wrong_span:
        str_error += gettext(u'errorWrongSpan') + ": " + '、'.join(lst_wrong_span) + '。'
    if lst_extra_slot:
        str_error += gettext(u'errorExtraSlot') + ": " + '、'.join(lst_extra_slot) + '。'
    if lst_extra_value:
        str_error += gettext(u'errorExtraSlotValue') + ": " + '、'.join(lst_extra_value) + '。'

    if str_error != '':
        return {'status': 'FAILED', 'error': str_error}

    return {'status': 'SUCCESS'}


def validate_dialogue(lst_turns):
    lst_invalid_turn = []
    n_error = 0
    for turn in lst_turns:
        src_dialogue = turn['src_dialog']
        para_dialogue = turn['para_dialog']
        turn_obj = validate_turn(src_dialogue, para_dialogue, turn['role'])
        turn_obj['turn_id'] = turn['turn_id']
        lst_invalid_turn.append(turn_obj)
        if turn_obj['status'] != 'SUCCESS':
            n_error += 1
    if n_error > 0:
        str_error = gettext(u'partTurnError')
        return {'status': 'FAILED', 'error': str_error, 'err_turns': lst_invalid_turn}

    return {'status': 'SUCCESS'}
