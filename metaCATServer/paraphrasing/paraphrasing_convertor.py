# -*- coding:utf-8 -*-
##############################################
# paraphrasing convertor
##############################################

import re
import chinese2digits as c2d
import recognizers_suite as Recognizers
from recognizers_suite import Culture, ModelResult

lst_special_slot_name = ['评分', '价格', '时长', '准点率', '出发时间', '到达时间', '开始时间', '结束时间', '时间',
                         '人数', '天数', '数量', '距离', 'choice']


def revise_value(value, raw_value, b_check_half=False, b_time=False):
    dst_value = value
    if b_check_half and '半' in raw_value:
        dst_value += 0.5
    if not b_time:
        return dst_value
    if '天' in raw_value:
        dst_value = dst_value * 8
    if '分钟' in raw_value and '小时' not in raw_value:
        dst_value = dst_value / 60
    return dst_value


def retrieve_punctuality(raw_value):
    p_result = Recognizers.recognize_percentage(raw_value, Culture.Chinese)
    if len(p_result) == 0:
        f_result = Recognizers.recognize_number(raw_value, Culture.Chinese)
        if len(f_result) == 0:
            return 0.0
        return float(f_result[0].resolution['value'])

    return float(p_result[0].resolution['value'].rstrip('%')) / 100


def time_delta(hour_minute, delta_time):
    if not re.match('[0-2][0-9]:[0-5][0-9]', hour_minute):
        result = Recognizers.recognize_datetime(hour_minute, Culture.Chinese)
        if not result or not result[0].resolution['values'] or result[0].resolution['values'][0]['type'] != 'time':
            hour_minute = '12:00'
        else:
            hour_minute = result[0].resolution['values'][0]['value'][:5]
    h_str_src, m_str_src = hour_minute.split(':')
    h_int_src, m_int_src = int(h_str_src), int(m_str_src)
    h_int_dst, m_int_dst = h_int_src + delta_time[0], m_int_src + delta_time[1]
    if m_int_dst >= 60:
        m_int_dst -= 60
        h_int_dst += 1
    elif m_int_dst < 0:
        m_int_dst += 60
        h_int_dst -= 1
    if h_int_dst >= 24:
        h_int_dst -= 24
    elif h_int_dst < 0:
        h_int_dst += 24
    return "%02d:%02d" % (h_int_dst, m_int_dst)


# 获取槽位的真实值（其中相对日期如“明天”等将基于当前日期计算）
def get_real_slot_value(slot_name, slot_value):
    if slot_name == '评分':
        f_rating = f_rating1 = f_rating2 = 4.0
        b_about = False
        digit_items = c2d.takeNumberFromString(slot_value)['digitsStringList']
        if len(digit_items) == 0 or len(digit_items) > 2:
            return '[{:.2f}, ∞)'.format(f_rating)
        elif len(digit_items) == 1:
            f_rating = float(digit_items[0])
        else:
            b_about = True
            f_rating = float(digit_items[0]), float(digit_items[1])
            f_rating1, f_rating2 = min(f_rating[0], f_rating[1]), max(f_rating[0], f_rating[1])
        if not b_about:
            f_rating = revise_value(f_rating, slot_value, b_check_half=True)
            if re.search('最少|至少|以上|超过|超出', slot_value):
                return '[{:.2f}, ∞)'.format(f_rating)
            if re.search('最多|最高|以下|不超过|以内|之内', slot_value):
                return '[0.0, {:.2f}]'.format(f_rating)
            if re.search('左右|上下|差不多|大概', slot_value):
                return '[{:.2f}, {:.2f}]'.format(f_rating * 0.95, f_rating * 1.05)
            return '{:.2f}'.format(f_rating)
        else:
            obj = re.search('至|到|-|—', slot_value)
            if obj:
                raw_value1, raw_value2 = slot_value[:obj.start()], slot_value[obj.end():]
                f_rating1 = revise_value(f_rating1, raw_value1, b_check_half=True)
                f_rating2 = revise_value(f_rating2, raw_value2, b_check_half=True)
            if abs(f_rating1 - f_rating2) <= 0.01:
                return '{:.2f}'.format((f_rating1 + f_rating2) / 2)
            else:
                return '[{:.2f}, {:.2f}]'.format(f_rating1, f_rating2)

    if slot_name == '价格':
        f_price1 = f_price2 = 100
        b_about = False
        digit_items = c2d.takeNumberFromString(slot_value)['digitsStringList']
        if len(digit_items) == 0 or len(digit_items) > 2:
            return slot_value
        elif len(digit_items) == 1:
            f_price = abs(float(digit_items[0]))
        else:
            b_about = True
            f_price = abs(float(digit_items[0])), abs(float(digit_items[1]))
            f_price1, f_price2 = min(f_price[0], f_price[1]), max(f_price[0], f_price[1])
        if not b_about:
            f_price = revise_value(f_price, slot_value)
            if re.search('最少|至少|以上|超过|超出', slot_value):
                return '[{:.2f}, ∞)'.format(f_price)
            if re.search('最多|最高|以下|不超过|以内|之内', slot_value):
                return '[0.0, {:.2f}]'.format(f_price)
            if re.search('左右|上下|差不多|大概', slot_value):
                return '[{:.2f}, {:.2f}]'.format(f_price * 0.8, f_price * 1.2)
            return '{:.2f}'.format(f_price)
        else:
            obj = re.search('至|到|-|—', slot_value)
            if obj:
                raw_value1, raw_value2 = slot_value[:obj.start()], slot_value[obj.end():]
                f_price1 = revise_value(f_price1, raw_value1)
                f_price2 = revise_value(f_price2, raw_value2)
            if abs(f_price1 - f_price2) <= 1.0:
                return '{:.2f}'.format((f_price1 + f_price2) / 2)
            else:
                return '[{:.2f}, {:.2f}]'.format(f_price1, f_price2)

    if slot_name == '时长':
        f_hour1 = f_hour2 = 2
        b_about = False
        digit_items = c2d.takeNumberFromString(slot_value)['digitsStringList']
        if len(digit_items) == 0 or len(digit_items) > 2:
            if '半' in slot_value:
                f_hour = 0.
            else:
                return slot_value
        elif len(digit_items) == 1:
            f_hour = float(digit_items[0])
        elif re.search('[1-9]小时[1-9][0-9]分钟', slot_value):
            f_hour = float(digit_items[0]) + float(digit_items[1]) / 60.0
        else:
            b_about = True
            f_hour = float(digit_items[0]), float(digit_items[1])
            f_hour1, f_hour2 = min(f_hour[0], f_hour[1]), max(f_hour[0], f_hour[1])
        if not b_about:
            f_hour = revise_value(f_hour, slot_value, b_check_half=True, b_time=True)
            if re.search('最少|至少|以上|超过|超出', slot_value):
                return '[{:.2f}, ∞)'.format(f_hour)
            if re.search('最多|最高|以下|不超过|以内|之内', slot_value):
                return '[0.0, {:.2f}]'.format(f_hour)
            if re.search('左右|差不多|大概', slot_value):
                return '[{:.2f}, {:.2f}]'.format(f_hour * 0.8, f_hour * 1.2)
            return '{:.2f}'.format(f_hour)
        else:
            obj = re.search('至|到|-|—', slot_value)
            if obj:
                raw_value1, raw_value2 = slot_value[:obj.start()], slot_value[obj.end():]
                f_hour1 = revise_value(f_hour1, raw_value1, b_check_half=True, b_time=True)
                f_hour2 = revise_value(f_hour2, raw_value2, b_check_half=True, b_time=True)
            if abs(f_hour1 - f_hour2) <= 0.1:
                return '{:.2f}'.format((f_hour1 + f_hour2) / 2)
            else:
                return '[{:.2f}, {:.2f}]'.format(f_hour1, f_hour2)

    if slot_name == '准点率':
        obj = re.search('至|到|-|—', slot_value)
        if obj and '至少' not in slot_value:
            value1, value2 = slot_value[:obj.start()], slot_value[obj.end():]
            f_punctuality1, f_punctuality2 = retrieve_punctuality(value1), retrieve_punctuality(value1)
            if f_punctuality1 < 0.1 or f_punctuality2 < 0.1:
                return slot_value
            if abs(f_punctuality1 - f_punctuality2) <= 0.01:
                return '{:.2f}'.format((f_punctuality1 + f_punctuality2) / 2)
            else:
                return '[{:.2f}, {:.2f}]'.format(f_punctuality1, f_punctuality2)
        f_punctuality = retrieve_punctuality(slot_value)
        if f_punctuality < 0.1:
            return slot_value
        if re.search('最低|至少|最少|以上|不低于', slot_value):
            return '[{:.2f}, ∞)'.format(f_punctuality)
        if re.search('大概|左右|上下|差不多', slot_value):
            return '[{:.2f}, {:.2f}]'.format(f_punctuality * 0.8, f_punctuality * 1.2)
        return slot_value

    if slot_name in ['出发时间', '到达时间']:
        result = Recognizers.recognize_datetime(slot_value, Culture.Chinese)
        if not result or not result[-1].resolution['values']:
            return slot_value
        str_type = result[-1].resolution['values'][0]['type']
        if str_type == 'time':
            time_str = result[-1].resolution['values'][0]['value'][:5]
            if re.search('大概|左右|前后|差不多', slot_value):
                time_left, time_right = time_delta(time_str, [0, -10]), time_delta(time_str, [0, 10])
                return '[{}, {}]'.format(time_left, time_right)
            if re.search('最早|后|以后|之后', slot_value):
                return '[{}, ∞)'.format(time_str)
            if re.search('最迟|最晚|前|以前|之前', slot_value):
                return '(-∞, {}]'.format(time_str)
            return time_str
        elif str_type == 'timerange':
            time_left = result[-1].resolution['values'][0]['start'][:5]
            time_right = result[-1].resolution['values'][0]['end'][:5]
            return '[{}, {}]'.format(time_left, time_right)
        return slot_value

    if slot_name in ['时间', '开始时间', '结束时间']:
        result = Recognizers.recognize_datetime(slot_value, Culture.Chinese)
        if not result or not result[-1].resolution['values'] or result[-1].resolution['values'][0]['type'] != 'time':
            return slot_value
        return result[-1].resolution['values'][0]['value'][:5]

    if slot_name in ['人数', '天数', '数量', '距离', 'choice']:
        if slot_name == 'choice' and '两' in slot_value:
            return '2'
        digit_items = c2d.takeNumberFromString(slot_value)['digitsStringList']
        if len(digit_items) == 0 or len(digit_items) > 2:
            return slot_value
        return str(digit_items[0]).split('.')[0]

    return slot_value


def convert_real_slot_value(dialogue):
    lst_turns = dialogue['dialogue']['turn_list']
    for turn in lst_turns:
        src_dialogue = turn['src_dialog']
        for slot_name, slot_item in src_dialogue['single_slot'].items():
            if slot_name not in lst_special_slot_name or slot_item[0] in ['what', 'min', 'max', 'upper', 'lower'] or \
                    not isinstance(slot_item[0], str):
                continue
            slot_item[3] = get_real_slot_value(slot_name, slot_item[0])
        for slot_name, item_lst in src_dialogue['batch_slot'].items():
            if slot_name not in lst_special_slot_name:
                continue
            for slot_item in item_lst:
                if slot_item[0] in ['what', 'min', 'max', 'upper', 'lower'] or not isinstance(slot_item[0], str):
                    continue
                slot_item[3] = get_real_slot_value(slot_name, slot_item[0])
