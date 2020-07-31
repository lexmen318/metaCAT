# -*- coding:utf-8 -*-
##############################################
# annotating validator
##############################################
from flask_babel import gettext, ngettext


def judge_repeat_slot(dic_slots, slot_name, slot_value):
    b_meet_self = False
    for slot_lst in dic_slots.values():
        for each_slot in slot_lst:
            for each_item in each_slot['slot_items']:
                if each_slot['slot_name'] == slot_name and each_item['slot_value'] == slot_value:
                    if not b_meet_self:
                        b_meet_self = True
                    else:
                        return True
    return False


def judge_repeat_value(dic_slots, slot_name, slot_value, span_info):
    b_meet_self = False
    for slot_lst in dic_slots.values():
        for each_slot in slot_lst:
            for each_item in each_slot['slot_items']:
                if each_item['slot_span'] == '':
                    continue
                str_st, str_ed = each_item['slot_span'].split('-')
                st, ed = int(str_st), int(str_ed)
                if each_slot['slot_name'] == slot_name and each_item['slot_value'] == slot_value and \
                        st == span_info[0] and ed == span_info[1]:
                    if not b_meet_self:
                        b_meet_self = True
                    else:
                        return True

    return False


# 暂时不允许槽位之间发生重叠或包含现象
def judge_repeat_span(dic_slots, slot_name, slot_value, slot_span):
    for slot_lst in dic_slots.values():
        for each_slot in slot_lst:
            for each_item in each_slot['slot_items']:
                if each_slot['slot_name'] == slot_name and each_item['slot_value'] == slot_value \
                        or each_item['slot_span'] == '':
                    continue
                str_st, str_ed = each_item['slot_span'].split('-')
                st, ed = int(str_st), int(str_ed)
                if st <= slot_span[0] < ed or st < slot_span[1] <= ed:
                    return True
    return False


def get_slot_meta(slot_metadata, slot_name):
    for every in slot_metadata:
        if every['slot_name'] == slot_name:
            return every
    return None


def validate_each_turn(dialog_turn, slot_metadata):
    lst_null_domain = []
    lst_enum_with_span = []
    lst_wrong_intent = []
    lst_wrong_span = []
    lst_repeat_span = []
    lst_repeat_slot = []
    lst_repeat_value = []
    lst_enum_with_str = []

    for dom in dialog_turn['domains']:
        if dom not in dialog_turn['slots'].keys():
            lst_null_domain.append(dom)

    for dom, slot_lst in dialog_turn['slots'].items():
        lst_slot_names = [slot['slot_name'] for slot in slot_lst]
        for slot in slot_lst:
            slot_name = slot['slot_name']
            if slot_name.endswith('-enum') and slot_name.replace('-enum', '-str') not in lst_slot_names or \
                    slot_name.endswith('-str') and slot_name.replace('-str', '-enum') not in lst_slot_names:
                lst_enum_with_str.append(slot['slot_name'])
            for item in slot['slot_items']:
                if slot['slot_type'] == 'enumeration' and item['slot_span'] != '':
                    lst_enum_with_span.append(slot['slot_name'])
                slot_meta = get_slot_meta(slot_metadata[dom], slot['slot_name'])
                if slot_meta and 'slot_intent' in slot_meta.keys():
                    if len(slot_meta['slot_intent']) > 0 and \
                            item['slot_intent'] not in slot_meta['slot_intent'] or \
                            item['slot_intent'] != 'Request' and item['slot_value'] in ['?', 'what'] or \
                            item['slot_intent'] == 'Request' and item['slot_value'] not in ['?', 'what']:
                        lst_wrong_intent.append(slot['slot_name'])
                if item['slot_span'] != '':
                    str_st, str_ed = item['slot_span'].split('-')
                    st, ed = int(str_st), int(str_ed)
                    span_info = [st, ed]
                    if st >= ed or item['slot_value'].lower() != dialog_turn['text'][st:ed].lower():
                        lst_wrong_span.append(item['slot_value'])
                    if judge_repeat_value(dialog_turn['slots'], slot['slot_name'], item['slot_value'], span_info):
                        lst_repeat_value.append(item['slot_value'])
                    if judge_repeat_span(dialog_turn['slots'], slot['slot_name'], item['slot_value'], span_info):
                        lst_repeat_span.append(slot['slot_name'])
                else:
                    if judge_repeat_slot(dialog_turn['slots'], slot['slot_name'], item['slot_value']):
                        lst_repeat_slot.append(slot['slot_name'])

    # str_error = '测试用错误消息。'
    str_error = ''
    if lst_null_domain:
        str_error += gettext(u'errorNullDomain') + ": " + '、'.join(lst_null_domain) + '。'
    if lst_enum_with_span:
        str_error += gettext(u'errorEnumWithSpan') + ": " + '、'.join(lst_enum_with_span) + '。'
    if lst_wrong_intent:
        str_error += gettext(u'errorWrongIntent') + ": " + '、'.join(lst_wrong_intent) + '。'
    if lst_wrong_span:
        str_error += gettext(u'errorWrongSpan') + ": " + '、'.join(lst_wrong_span) + '。'
    if lst_repeat_span:
        str_error += gettext(u'errorRepeatSpan') + ": " + '、'.join(lst_repeat_span) + '。'
    if lst_repeat_slot:
        str_error += gettext(u'errorRepeatSlot') + ": " + '、'.join(lst_repeat_slot) + '。'
    if lst_repeat_value:
        str_error += gettext(u'errorRepeatValue') + ": " + '、'.join(lst_repeat_value) + '。'
    if lst_enum_with_str:
        str_error += gettext(u'errorEnumNoStr') + ": " + '、'.join(lst_enum_with_str) + '。'

    return str_error


def validate_turn(dialog_turn, metadata_value):
    str_usr = validate_each_turn(dialog_turn['usr'], metadata_value['usr_slot'])
    str_sys = validate_each_turn(dialog_turn['sys'], metadata_value['sys_slot'])

    if str_usr:
        usr_validation = {'status': 'FAILED', 'desc': str_usr}
    else:
        usr_validation = {'status': 'SUCCESS', 'desc': str_usr}

    if str_sys:
        sys_validation = {'status': 'FAILED', 'desc': str_sys}
    else:
        sys_validation = {'status': 'SUCCESS', 'desc': str_sys}

    return usr_validation, sys_validation


def validate_dialogue(lst_turns, metadata_value):
    lst_invalid_turn = []
    n_error = 0
    turn_id = 0
    for turn in lst_turns:
        usr_validation, sys_validation = validate_turn(turn, metadata_value)
        # 保存检测结果
        turn['usr']['turn_info'] = usr_validation
        turn['sys']['turn_info'] = sys_validation
        lst_invalid_turn.append(turn)
        if usr_validation['status'] != 'SUCCESS' or sys_validation['status'] != 'SUCCESS':
            n_error += 1
        turn_id += 1
    if n_error > 0:
        str_error = gettext(u'partTurnError')
        return {'status': 'FAILED', 'desc': str_error, 'err_turns': lst_invalid_turn}

    return {'status': 'SUCCESS'}
