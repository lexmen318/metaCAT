# -*- coding:utf-8 -*-

import re

slot_value_similar = 0.8

# WOZ word translator
phrase_from_woz = {'usr-greet': '问候', 'usr-thank': '感谢', 'usr-bye': '再见', 'usr-Request': '请求服务(Q)',
                   'usr-Inform': '提供信息(I)', 'sys-reqmore': '问询', 'sys-greet': '招呼', 'sys-welcome': '欢迎',
                   'sys-bye': '告别', 'sys-Request': '请求信息(Q)', 'sys-Inform': '告知信息(I)', 'sys-NoOffer': '无法满足(N)',
                   'sys-Select': '提供选择(S)', 'sys-Recommend': '推荐(R)', 'general': '通用', 'Hotel': '酒店',
                   'Taxi': '出租车', 'Train': '火车', 'Attraction': '旅游', 'Restaurant': '餐馆', 'Hospital': '医院',
                   'Police': '警察', 'Phone': '电话', 'Post': '邮编', 'Fee': '价格', 'Addr': '地址', 'Price': '价格',
                   'Time': '时间', 'Type': '类型', 'Ref': '订单号', 'Booking-Request': '待定', 'Booking-Inform': '确认',
                   'Booking-NoBook': '失败', 'Booking-Book': '完成', 'OfferBook': '确认', 'OfferBooked': '完成',
                   'Booking-Domain': '领域', 'Booking-Ref': '订单号', 'Booking-Name': '名称(或列车号)',
                   'Hotel-Ref': '订单号', 'Restaurant-Ref': '订单号', 'Train-Ref': '订单号',
                   'Booking-Day': '日期(入住/就餐)', 'Booking-Time': '时间(就餐)', 'Booking-Stay': '天数(入住)',
                   'Booking-People': '人数', 'Booking': '预订', 'Hotel-Choice': '可能选择', 'Hotel-Type': '类型',
                   'Hotel-Area': '方位', 'Hotel-Name': '酒店名称', 'Hotel-Price': '价格', 'Hotel-Stars': '酒店星级',
                   'Hotel-Parking': '停车信息', 'Hotel-Phone': '电话', 'Hotel-Internet': '酒店网络', 'Hotel-Post': '邮编',
                   'Hotel-Addr': '地址', 'Hotel-People': '入住人数', 'Hotel-Day': '入住日期', 'Hotel-Stay': '入住天数',
                   'Restaurant-Choice': '可能选择', 'Restaurant-Food': '餐馆口味', 'Restaurant-Area': '方位',
                   'Restaurant-Name': '餐馆名称', 'Restaurant-Price': '价格', 'Restaurant-Phone': '电话',
                   'Restaurant-Post': '邮编',
                   'Restaurant-Addr': '地址', 'Restaurant-People': '就餐人数', 'Restaurant-Day': '就餐日期',
                   'Restaurant-Time': '就餐时间', 'Attraction-Choice': '可能选择', 'Attraction-Type': '类型',
                   'Attraction-Area': '方位', 'Attraction-Name': '景点名称', 'Attraction-Fee': '费用', 'Attraction-Post': '邮编',
                   'Attraction-Phone': '电话', 'Attraction-Addr': '地址', 'Hospital-Choice': '可能选择',
                   'Hospital-Name': '医院名称', 'Hospital-Department': '医院科室', 'Hospital-Phone': '电话',
                   'Hospital-Post': '邮编', 'Hospital-Addr': '地址', 'Police-Choice': '可能选择', 'Police-Name': '警察局名称',
                   'Police-Addr': '地址', 'Police-Phone': '电话', 'Police-Post': '邮编', 'Train-Id': '列车号',
                   'Train-Day': '出发日期', 'Train-People': '乘车人数', 'Train-Choice': '可能选择', 'Train-Leave': '出发时间',
                   'Train-Depart': '出发地', 'Train-Dest': '目的地', 'Train-Arrive': '到达时间', 'Train-Time': '历时',
                   'Train-Ticket': '票价', 'Taxi-Choice': '可能选择', 'Taxi-Car': '出租车型', 'Taxi-Leave': '出发时间',
                   'Taxi-Depart': '出发地', 'Taxi-Dest': '目的地', 'Taxi-Arrive': '到达时间', 'Taxi-Phone': '电话'}

phrase_to_woz = {'问候': 'greet', '感谢': 'thank', '再见': 'bye', '请求服务(Q)': 'Request', '提供信息(I)': 'Inform', '告别': 'bye',
                 '问询': 'reqmore', '欢迎': 'welcome', '招呼': 'greet', '请求信息(Q)': 'Request', '告知信息(I)': 'Inform',
                 '推荐(R)': 'Recommend', '无法满足(N)': 'NoOffer', '提供选择(S)': 'Select', '待定': 'Request',
                 '确认': 'Inform', '失败': 'NoBook', '完成': 'Book', '领域': 'Domain', '人数': 'People',
                 '名称(或列车号)': 'Name', '日期(入住/就餐)': 'Day', '时间(就餐)': 'Time', '天数(入住)': 'Stay', '预订': 'Booking',
                 '通用': 'general', '酒店': 'Hotel', '出租车': 'Taxi', '火车': 'Train', '旅游': 'Attraction',
                 '餐馆': 'Restaurant', '医院': 'Hospital', '警察': 'Police', '电话': 'Phone', '邮编': 'Post', '地址': 'Addr',
                 '价格': 'Price', '类型': 'Type', '方位': 'Area', '费用': 'Fee', '订单号': 'Ref', '可能选择': 'Choice',
                 '酒店名称': 'Name', '酒店星级': 'Stars', '停车信息': 'Parking', '酒店网络': 'Internet', '入住人数': 'People',
                 '入住日期': 'Day', '入住天数': 'Stay', '餐馆口味': 'Food', '餐馆名称': 'Name', '就餐人数': 'People',
                 '就餐日期': 'Day', '就餐时间': 'Time', '景点名称': 'Name', '医院名称': 'Name', '医院科室': 'Department',
                 '警察局名称': 'Name', '列车号': 'Id', '出发日期': 'Day', '乘车人数': 'People', '出发时间': 'Leave',
                 '出发地': 'Depart', '目的地': 'Dest', '历时': 'Time', '到达时间': 'Arrive', '票价': 'Ticket', '出租车型': 'Car'}


class DataConvertor(object):

    @staticmethod
    def from_dataset(cur_json, data_set='MultiWOZ'):
        ret_json = cur_json
        if data_set in ['MultiWOZ', 'MULTIWOZ']:
            ret_json = DataConvertor.from_multiwoz(cur_json)
        for dialogue_id, dialogue_item in ret_json.items():
            for idx in range(len(dialogue_item['turns'])):
                turn = dialogue_item['turns'][idx]
                turn['usr']['turn_info'] = {'status': 'SUCCESS', 'desc': ''}
                turn['sys']['turn_info'] = {'status': 'SUCCESS', 'desc': ''}
        return ret_json

    @staticmethod
    def to_dataset(cur_json, data_set='MultiWOZ'):
        if data_set == 'MultiWOZ':
            return DataConvertor.to_multiwoz(cur_json)

    @staticmethod
    def from_multiwoz(cur_json):
        def get_exist_slot(lst_slot, slot_name):
            for idx in range(len(lst_slot)):
                if lst_slot[idx]['slot_name'] == slot_name:
                    return idx
            return -1

        def get_slot_value(lst_slot_item, slot_value):
            for idx in range(len(lst_slot_item)):
                # sm_ratio = difflib.SequenceMatcher(a=slot_value, b=lst_slot_item[idx]['slot_value']).quick_ratio()
                if lst_slot_item[idx]['slot_value'] == slot_value:  # or \
                    # ' ' in slot_value and sm_ratio >= slot_value_similar:
                    return idx
            return -1

        ret_json = dict()
        for name, dialog in cur_json.items():
            turns = []
            turn = {}
            utters = dialog['log']
            for ind in range(len(utters)):
                # if name == 'MUL2405' and ind == 1:
                #     print('here!')
                if ind % 2 == 0:
                    if turn:
                        turns.append(turn)
                        turn = {}
                    end_type = 'usr'
                else:
                    end_type = 'sys'

                turn[end_type] = {}
                turn[end_type]['text'] = re.sub('[\s]+', ' ', utters[ind]['text'])
                turn_text = utters[ind]['text'].lower()
                words = turn_text.split()
                turn[end_type]['general'] = []
                turn[end_type]['domains'] = []
                turn[end_type]['slots'] = {}
                for act_key, slot_lst in utters[ind]['dialog_act'].items():
                    dom, intent = act_key.split('-')
                    if dom == 'general':
                        if intent not in turn[end_type]['general']:
                            turn[end_type]['general'].append(intent)
                        continue
                    if dom not in turn[end_type]['domains']:
                        turn[end_type]['domains'].append(dom)
                    if dom not in turn[end_type]['slots'].keys():
                        turn[end_type]['slots'][dom] = []
                    for slot_item in slot_lst:
                        slot_idx = get_exist_slot(turn[end_type]['slots'][dom], slot_item[0])
                        if slot_idx < 0:
                            cur_slot = {'slot_name': slot_item[0], 'slot_type': 'string'}
                            if slot_item[0] in ['Internet', 'Parking', 'none']:
                                cur_slot['slot_type'] = 'enumeration'
                            cur_slot['slot_items'] = []
                            turn[end_type]['slots'][dom].append(cur_slot)
                        else:
                            cur_slot = turn[end_type]['slots'][dom][slot_idx]
                        slot_item = {'slot_intent': intent, 'slot_value': slot_item[1], 'slot_span': ''}
                        cur_slot['slot_items'].append(slot_item)
                for span_info in utters[ind]['span_info']:
                    dom, intent = span_info[0].split('-')
                    # Slot positions transformed to integer
                    span_info[3], span_info[4] = int(span_info[3]), int(span_info[4])
                    slot_idx = get_exist_slot(turn[end_type]['slots'][dom], span_info[1])
                    if slot_idx < 0:
                        print('Error—— dialog: {}, turn: {}, slot: {}'.format(name, ind, span_info[1]))
                        continue
                    value_idx = get_slot_value(turn[end_type]['slots'][dom][slot_idx]['slot_items'], span_info[2])
                    if value_idx < 0:
                        print('Info—— dialog: {}, turn: {}, slot: {}, value: {}'.format(name, ind, span_info[1],
                                                                                        span_info[2]))
                        slot_item = {'slot_intent': intent, 'slot_value': span_info[2], 'slot_span': ''}
                        value_idx = len(turn[end_type]['slots'][dom][slot_idx]['slot_items'])
                        turn[end_type]['slots'][dom][slot_idx]['slot_items'].append(slot_item)
                    try_span_test = turn_text[span_info[3]:span_info[4]]
                    if try_span_test == span_info[2].lower():
                        span = '{}-{}'.format(span_info[3], span_info[4])
                    else:
                        if span_info[3] == 0:
                            start = 0
                        else:
                            start = len(' '.join(words[:span_info[3]])) + 1
                        end = start + len(span_info[2])
                        span = '{}-{}'.format(start, end)
                    turn[end_type]['slots'][dom][slot_idx]['slot_items'][value_idx]['slot_span'] = span

            if turn:
                if 'sys' not in turn.keys():
                    turn['sys'] = {}
                turns.append(turn)

            ret_json['Dialogue_' + name.split('.')[0]] = {
                "turns": turns
            }

        return ret_json

    @staticmethod
    # archived， not used
    def from_multiwoz_archived(cur_json):
        ret_json = dict()

        def get_span(sp_lst, int_rsp, sp_slot, sp_value):
            for every in sp_lst:
                if every[0] == int_rsp and every[1] == sp_slot and every[2] == sp_value:
                    return str(every[3]) + '-' + str(every[4])
            return ''

        def get_opr_code(operation):
            if operation == 'Inform' or operation == 'OfferBook' or operation == 'OfferBooked':
                return 'I'
            elif operation == 'Request':
                return 'Q'
            elif operation == 'Recommend':
                return 'R'
            elif operation == 'NoOffer' or operation == 'NoBook':
                return 'N'
            elif operation == 'Select':
                return 'S'
            elif operation == 'Book':
                return 'B'
            else:
                return ''

        def update_slots(ret_lst, operation, sl_name, sl_value, sp_value):
            b_found = False
            new_sl = new_sp = new_op = ''
            if sl_name == '订单号' and sl_value != '?':
                operation = 'B'
            for idx in range(len(ret_lst), 0, -1):
                if ret_lst[idx - 1][0] == sl_name:
                    b_found = True
                    new_sl = ret_lst[idx - 1][1] + ',' + sl_value
                    new_sp = ret_lst[idx - 1][2] + ',' + sp_value
                    new_op = ret_lst[idx - 1][3] + ',' + operation
                    ret_lst.__delitem__(idx - 1)
                    break
            if b_found:
                ret_lst.append((sl_name, new_sl, new_sp, new_op))
            else:
                ret_lst.append((sl_name, sl_value, sp_value, operation))

        def treat_acts(ret_lst, act_lst, sp_lst, sp_domain, int_rsp):
            int_rsp_name = sp_domain + '-' + int_rsp
            for every in act_lst:
                slot_name = sp_domain + '-' + every[0]
                if slot_name not in phrase_from_woz.keys():
                    continue
                slot_value = every[1]
                span_value = get_span(sp_lst, int_rsp_name, every[0], slot_value)
                update_slots(ret_lst, get_opr_code(int_rsp), phrase_from_woz[slot_name], slot_value, span_value)

        def add_book_field(lst_fields, label, lst_values):
            if len(lst_values) == 0:
                return
            str_value, str_turn = lst_values[0]
            for idx in range(len(lst_values) - 1):
                str_value += ',' + lst_values[idx + 1][0]
                str_turn += ',' + lst_values[idx + 1][1]
            lst_fields.append((phrase_from_woz[label], str_value, str_turn, ''))

        def decide_turn(dic_cache, turn_str, dom, label):
            dic_key = dom + '-' + label
            if dic_key in dic_cache.keys() and dic_cache[dic_key] != '':
                return dic_cache[dic_key]
            else:
                dic_cache[dic_key] = turn_str
                return turn_str

        def clear_cache(dic_cache, dom, label):
            dic_key = dom + '-' + label
            dic_cache[dic_key] = ''

        def transfer_label(label):
            if label == 'reference':
                return 'Ref'
            if label == 'trainID':
                return 'Name'
            return label.title()

        def retrieve_booking_info(dic_meta, cur_turn, dic_cache):
            book_fields = dict()
            for every in ['Domain', 'People', 'Day', 'Time', 'Stay', 'Name', 'Ref']:
                book_fields[every] = []
            for dom, meta in dic_meta.items():
                if dom not in ['hotel', 'restaurant', 'train']:
                    continue
                book_info = meta['book']
                turn_no = 'T' + str(cur_turn)
                set_dom_turn = set()
                for field in ['people', 'day', 'time', 'stay']:
                    if field in book_info.keys() and book_info[field] != '':
                        real_turn = decide_turn(dic_cache, turn_no, dom, field)
                        book_fields[transfer_label(field)].append((book_info[field], real_turn))
                        set_dom_turn.add(real_turn)
                    else:
                        clear_cache(dic_cache, dom, field)
                if len(book_info['booked']) > 0:
                    name_ref = book_info['booked'][0]
                    for field in ['name', 'trainID', 'reference']:
                        if field in name_ref.keys() and name_ref[field] != '':
                            real_turn = decide_turn(dic_cache, turn_no, dom, field)
                            book_fields[transfer_label(field)].append((name_ref[field], real_turn))
                            set_dom_turn.add(real_turn)
                        else:
                            clear_cache(dic_cache, dom, field)
                for every in set_dom_turn:
                    book_fields['Domain'].append((dom, every))
            if len(book_fields['Domain']) == 0:
                return []
            ret_info = list()
            for label, field in book_fields.items():
                add_book_field(ret_info, 'Booking-' + label, field)
            return ret_info

        for name, dialog in cur_json.items():
            turns = []
            turn = dict()
            utters = dialog['log']
            prev_domains = []
            turn_cache = dict()
            for ind in range(len(utters)):
                if ind % 2 == 0:
                    turn = dict()
                    domains = []
                    turn['用户'] = utters[ind]['text']
                    user_act = utters[ind]['dialog_act']
                    user_span = utters[ind]['span_info']
                    turn['意图'] = []
                    for key, value in user_act.items():
                        domain, intent = key.split('-')
                        if 'usr-' + intent not in phrase_from_woz.keys():
                            continue
                        if domain not in domains:
                            domains.append(phrase_from_woz[domain])
                        if 'usr-' + intent not in phrase_from_woz.keys():
                            continue
                        turn['意图'] = [phrase_from_woz['usr-' + intent]]
                        slot_label = '槽位-' + phrase_from_woz[domain]
                        if slot_label not in turn.keys():
                            turn[slot_label] = []
                        treat_acts(turn[slot_label], value, user_span, domain, intent)
                        if domain == 'general' and len(turn['意图']) == 0:
                            turn['意图'] = [phrase_from_woz['usr-' + intent]]
                    if len(domains) > 0:
                        prev_domains = domains
                    else:
                        domains = prev_domains
                    turn['领域'] = domains
                else:
                    turn['系统'] = utters[ind]['text']
                    system_meta = utters[ind]['metadata']
                    system_act = utters[ind]['dialog_act']
                    system_span = utters[ind]['span_info']
                    turn['预订状态'] = []
                    turn['响应类别'] = []
                    turn_index = ind // 2
                    turn['预订信息'] = retrieve_booking_info(system_meta, turn_index + 1, turn_cache)
                    for key, value in system_act.items():
                        domain, response = key.split('-')
                        if domain == 'Booking':
                            turn['预订状态'].append(phrase_from_woz[key])
                            rsp_label = '响应-' + phrase_from_woz[domain]
                            if rsp_label not in turn.keys():
                                turn[rsp_label] = []
                            treat_acts(turn[rsp_label], value, system_span, domain, response)
                            real_resp = response
                            if response == 'Book':
                                real_resp = 'Inform'
                            elif response == 'NoBook':
                                real_resp = 'NoOffer'
                            turn['响应类别'].append(phrase_from_woz['sys-' + real_resp])
                        elif domain == 'general':
                            turn['响应类别'].append(phrase_from_woz['sys-' + response])
                        elif response in ['Request', 'Inform', 'Recommend', 'NoOffer', 'Select',
                                          'OfferBook', 'OfferBooked']:
                            rsp_label = '响应-' + phrase_from_woz[domain]
                            if rsp_label not in turn.keys():
                                turn[rsp_label] = []
                            treat_acts(turn[rsp_label], value, system_span, domain, response)
                            if response in ['OfferBook', 'OfferBooked']:
                                turn['响应类别'].append(phrase_from_woz['sys-Inform'])
                                turn['预订状态'].append(phrase_from_woz[response])
                            else:
                                turn['响应类别'].append(phrase_from_woz['sys-' + response])
                    if '响应-火车' in turn.keys():
                        for idx in range(len(turn['响应-火车']), 0, -1):
                            if turn['响应-火车'][idx - 1][0] == '订单号':
                                if '响应-预订' not in turn.keys():
                                    turn['响应-预订'] = []
                                turn['响应-预订'].append(turn['响应-火车'][idx - 1])
                                turn['响应-火车'].__delitem__(idx - 1)
                                break

                    turn['响应类别'] = list(set(turn['响应类别']))
                    turns.append(turn)

            # ret_json['Dialogue_' + name.split('.')[0]] = turns
            ret_json['Dialogue_' + name.split('.')[0]] = {
                "status": 'PROCESSING',
                "turns": turns
            }

        return ret_json

    @staticmethod
    def to_multiwoz(cur_json):
        ret_json = dict()

        def transfer_span(slot_value, sp_st, dialog_text):
            slot_words = slot_value.split()
            words = dialog_text.split()
            dst_start = word_index = 0
            while dst_start < sp_st and word_index < len(words):
                dst_start += len(words[word_index])
                while re.match('[\s]', dialog_text[dst_start:dst_start+1]):
                    dst_start += 1
                word_index += 1
            return word_index, word_index + len(slot_words) - 1

        def build_acts(d_turn):
            dialog_act = {}
            span_info = []
            for every in d_turn['general']:
                dialog_act['general-' + every] = [['none', 'none']]
            for dom in d_turn['domains']:
                if dom not in d_turn['slots'].keys():
                    continue
                for slot_obj in d_turn['slots'][dom]:
                    for slot_item in slot_obj['slot_items']:
                        act_key = dom + '-' + slot_item['slot_intent']
                        if act_key not in dialog_act.keys():
                            dialog_act[act_key] = []
                        dialog_act[act_key].append([slot_obj['slot_name'], slot_item['slot_value']])
                        if slot_item['slot_span'] != '':
                            start, _ = slot_item['slot_span'].split('-')
                            sp_st, sp_ed = transfer_span(slot_item['slot_value'], int(start), d_turn['text'])
                            span_info.append([act_key, slot_obj['slot_name'], slot_item['slot_value'], sp_st, sp_ed])

            return dialog_act, span_info

        for name, dialog in cur_json.items():
            dialog_name = name.split('_')[1] + '.json'
            ret_dialog = dict()
            ret_dialog['log'] = []
            for turn in dialog['turns']:
                log = dict()
                log['text'] = turn['usr']['text']
                acts, spans = build_acts(turn['usr'])
                log['metadata'] = {}
                log['dialog_act'] = acts
                log['span_info'] = spans
                ret_dialog['log'].append(log)
                log = dict()
                log['text'] = turn['sys']['text']
                log['metadata'] = {}
                acts, spans = build_acts(turn['sys'])
                log['dialog_act'] = acts
                log['span_info'] = spans
                ret_dialog['log'].append(log)
            ret_json[dialog_name] = ret_dialog

        return ret_json

    @staticmethod
    # archived， not used
    def to_multiwoz_archived(cur_json):
        ret_json = dict()

        def get_opr_str(opr_code, b_booking=False):
            if opr_code == 'I':
                return 'Inform'
            elif opr_code == 'Q':
                return 'Request'
            elif opr_code == 'R':
                return 'Recommend'
            elif opr_code == 'N':
                if b_booking:
                    return 'NoBook'
                else:
                    return 'NoOffer'
            elif opr_code == 'S':
                return 'Select'
            elif opr_code == 'B':
                return 'Book'
            else:
                return 'Inform'

        def build_booking_info(dic_meta, lst_book_info):
            for domain in ['hotel', 'restaurant', 'train']:  # ignore other domains without booking info
                dic_meta[domain] = dict()
                dic_meta[domain]['book'] = dict()
                dic_meta[domain]['book']['booked'] = [dict()]
                dic_meta[domain]['semi'] = dict()  # ignore 'semi' field, just let it be null

            if len(lst_book_info) < 2:
                return

            domains = []
            turns = []
            for lbl, vals, turns, _ in lst_book_info:
                if lbl == '领域':
                    domains = vals.split(',')
                    turns = turns.split(',')
                    break
            if len(domains) == 0:
                return
            td_map = dict()
            for tn, dom in zip(turns, domains):  # suppose that different turns booking different domains
                td_map[tn] = dom
            for every in lst_book_info:
                if len(every) < 4:
                    print("wrong!")
                lbl, vals, turns, _ = every
                if lbl == '领域':
                    continue
                lbl_en = phrase_to_woz[lbl].lower()
                if lbl_en == 'ref':
                    lbl_en = 'reference'
                vals = vals.split(',')
                turns = turns.split(',')
                for tn, val in zip(turns, vals):
                    domain = td_map[tn]
                    if lbl_en == 'name' and domain == 'train':
                        lbl_en = 'trainID'
                    if lbl_en in ['reference', 'name', 'trainID']:
                        dic_meta[domain]['book']['booked'][0][lbl_en] = val
                    else:
                        dic_meta[domain]['book'][lbl_en] = val

        def build_acts(d_turn, b_sys=False):
            prefix = '响应-' if b_sys else '槽位-'
            default_op = '告知信息(I)' if b_sys else '提供信息(I)'
            int_rsp = '响应类别' if b_sys else '意图'
            if b_sys:
                general_operations = ['招呼', '欢迎', '告别', '问询']
            else:
                general_operations = ['问候', '感谢', '再见']
            service_domains = ['酒店', '餐馆', '医院', '旅游', '警察', '火车', '出租车']
            if b_sys:
                service_domains.append('预订')

            ret_acts = dict()
            ret_spans = []

            d_acts = [['none', 'none']]
            for every in general_operations:
                if every in d_turn[int_rsp]:
                    domain_intent = 'general' + '-' + phrase_to_woz[every]
                    ret_acts[domain_intent] = d_acts

            for dom in service_domains:
                slot_domain = prefix + dom
                domain = phrase_to_woz[dom]
                if slot_domain not in d_turn.keys():
                    if dom in d_turn['领域'] and default_op in d_turn[int_rsp] and '完成' not in d_turn['预订状态']:
                        ret_acts[domain + '-Inform'] = [['none', 'none']]
                    continue
                for key, value, span, opr in d_turn[slot_domain]:
                    if key not in phrase_to_woz.keys():
                        continue
                    slot = phrase_to_woz[key]
                    val_lst = value.split(',')
                    sp_lst = span.split(',')
                    opr_lst = opr.split(',')
                    for val, sp, op in zip(val_lst, sp_lst, opr_lst):
                        op_str = get_opr_str(op, b_booking=(domain == 'Booking'))
                        if val == '?':
                            op_str = 'Request'
                        domain_intent = domain + '-' + op_str
                        if sp != '':
                            sp1, sp2 = sp.split('-')
                            ret_spans.append([domain_intent, slot, val, sp1, sp2])
                        if domain_intent not in ret_acts.keys():
                            ret_acts[domain_intent] = [[slot, val]]
                        else:
                            ret_acts[domain_intent].append([slot, val])
            if b_sys and len(d_turn['预订状态']) > 0:
                for state in d_turn['预订状态']:
                    domain_intent = 'Booking-' + phrase_to_woz[state]
                    if domain_intent not in ret_acts.keys():
                        ret_acts[domain_intent] = [['none', 'none']]

            return ret_acts, ret_spans

        for name, dialog in cur_json.items():
            dialog_name = name.split('_')[1] + '.json'
            ret_dialog = dict()
            logs = []
            dialogTurns = dialog['turns']
            for turn in dialogTurns:
                log = dict()
                log['text'] = turn['用户']
                acts, spans = build_acts(turn)
                log['metadata'] = {}
                log['dialog_act'] = acts
                log['span_info'] = spans
                logs.append(log)
                log = dict()
                log['text'] = turn['系统']
                log['metadata'] = {}
                build_booking_info(log['metadata'], turn['预订信息'])
                acts, spans = build_acts(turn, b_sys=True)
                log['dialog_act'] = acts
                log['span_info'] = spans
                logs.append(log)
            ret_dialog['goal'] = {}  # ignore the 'goal' content
            ret_dialog['log'] = logs
            ret_json[dialog_name] = ret_dialog

        return ret_json
