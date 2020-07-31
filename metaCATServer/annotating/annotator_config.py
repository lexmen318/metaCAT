# -*- coding:utf-8 -*-

##############################################
#  IMPORT STATEMENTS
##############################################

# >>>> Native <<<<
from typing import Dict, List, Any, Union

# >>>> Local <<<<
from annotating.dummy_models import SysDummyModel, DomainDummyModel, IntentDummyModel, SlotDummyModel
from annotating.dummy_models import ResponseDummyModel, BookingDummyModel, BookingInfoDummyModel

##############################################
#                  CONFIG Dict
#
# The config dict describes all the data fields.
# This is also the place to specify models and label types.
#
# Available label types:
#
#     => "multilabel_classification" :: displays as checkboxes in front end
#
#     => "multilabel_classification_string" :: displays as a checkbox and text input for string value. Used for
#                                              slot-value pairs.
#
#     => "string" :: displays underneath the user utterance (indicated by label_type of "data")
#
#############################################

##############################################
#  CODE
##############################################


class Configuration(object):
    """
    class responsible for configuration and valid annotation structure
    """

    configDict = {

        "用户": {
            "description" : "用户问题",
            "label_type"  : "data",  # This type, "data", acts the same as "string" but will always be displayed first in UI
            "required"    : True,
            "apply_end": "Usr",
            "slot_rsp": False,
        },

        "系统": {
            "description": "系统响应信息",
            "label_type": "string",
            "required"    : True,
            "apply_end": "Sys",
            "slot_rsp": False,
            "model": SysDummyModel()
        },

        "领域": {
            "description" : "受理业务相关领域(通常单选)",
            "label_type"  : "multilabel_classification",
            "required"    : False,
            "apply_end"   : "Usr",
            "slot_rsp": False,
            "model"       : DomainDummyModel(),
            "labels"      : [
                "通用",
                "酒店",
                "餐馆",
                "旅游",
                "医院",
                "警察",
                "火车",
                "出租车"
            ]
        },

        "意图": {
            "description" : "用户当前意图(可多选)",
            "label_type"  : "multilabel_classification",
            "required"    : False,
            "apply_end"   : "Usr",
            "slot_rsp": False,
            "model"       : IntentDummyModel(),
            "labels"      : [
                "问候",
                "感谢",
                "再见",
                "请求服务(Q)",
                "提供信息(I)"
            ]
        },

        "槽位-酒店": {
            "description": "酒店业务槽位信息: 1.多条同类标签采用逗号分隔; 2.左侧为槽位，右侧为操作类别和位置。",
            "label_type" : "multilabel_classification_string",
            "required"   : False,
            "apply_end"  : "Usr",
            "slot_rsp"   : True,
            "model"      : SlotDummyModel('Hotel'),
            "labels"     : [
                "可能选择",
                "酒店名称",
                "酒店星级",
                "停车信息",
                "酒店网络",
                "入住人数",
                "入住日期",
                "入住天数",
                "类型",
                "价格",
                "方位",
                "电话",
                "邮编",
                "地址",
                "订单号"
            ]
        },

        "槽位-餐馆": {
            "description": "餐馆业务槽位信息: 1.多条同类标签采用逗号分隔; 2.左侧为槽位，右侧为操作类别和位置。",
            "label_type": "multilabel_classification_string",
            "required": False,
            "apply_end": "Usr",
            "slot_rsp": True,
            "model": SlotDummyModel('Restaurant'),
            "labels": [
                "可能选择",
                "餐馆名称",
                "餐馆口味",
                "就餐人数",
                "就餐日期",
                "就餐时间",
                "价格",
                "方位",
                "电话",
                "邮编",
                "地址",
                "订单号"
            ]
        },

        "槽位-旅游": {
            "description" : "旅游业务槽位信息: 1.多条同类标签采用逗号分隔; 2.左侧为槽位，右侧为操作类别和位置。",
            "label_type"  : "multilabel_classification_string",
            "required"    : False,
            "apply_end": "Usr",
            "slot_rsp": True,
            "model"       : SlotDummyModel('Attraction'),
            "labels"      : [
                "可能选择",
                "景点名称",
                "类型",
                "费用",
                "方位",
                "电话",
                "邮编",
                "地址"
            ]
        },

        "槽位-医院": {
            "description": "医院业务槽位信息: 1.多条同类标签采用逗号分隔; 2.左侧为槽位，右侧为操作类别和位置。",
            "label_type": "multilabel_classification_string",
            "required": False,
            "apply_end": "Usr",
            "slot_rsp": True,
            "model": SlotDummyModel('Hospital'),
            "labels": [
                "可能选择",
                "医院名称",
                "医院科室",
                "方位",
                "电话",
                "邮编",
                "地址"
            ]
        },

        "槽位-警察": {
            "description": "警察业务槽位信息: 1.多条同类标签采用逗号分隔; 2.左侧为槽位，右侧为操作类别和位置。",
            "label_type": "multilabel_classification_string",
            "required": False,
            "apply_end": "Usr",
            "slot_rsp": True,
            "model": SlotDummyModel('Police'),
            "labels": [
                "可能选择",
                "警察局名称",
                "方位",
                "电话",
                "邮编",
                "地址"
            ]
        },

        "槽位-火车": {
            "description": "火车业务槽位信息: 1.多条同类标签采用逗号分隔; 2.左侧为槽位，右侧为操作类别和位置。",
            "label_type": "multilabel_classification_string",
            "required": False,
            "apply_end": "Usr",
            "slot_rsp": True,
            "model": SlotDummyModel('Train'),
            "labels": [
                "可能选择",
                "列车号",
                "出发日期",
                "乘车人数",
                "出发时间",
                "出发地",
                "目的地",
                "到达时间",
                "历时",
                "票价",
                "订单号"
            ]
        },

        "槽位-出租车": {
            "description": "出租车业务槽位信息: 1.多条同类标签采用逗号分隔; 2.左侧为槽位，右侧为操作类别和位置。",
            "label_type": "multilabel_classification_string",
            "required": False,
            "apply_end": "Usr",
            "slot_rsp": True,
            "model": SlotDummyModel('Taxi'),
            "labels": [
                "可能选择",
                "出租车型",
                "出发时间",
                "出发地",
                "目的地",
                "到达时间",
                "电话"
            ]
        },

        "预订状态": {
            "description": "服务订单状态(随对话轮次变化)",
            "label_type": "multilabel_classification_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": False,
            "model": BookingDummyModel(),
            "labels": [
                "待定",
                "确认",
                "失败",
                "完成"
            ]
        },

        "响应类别": {
            "description": "系统响应类别(业务响应最多选2个)",
            "label_type": "multilabel_classification_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": False,
            "model": ResponseDummyModel(),
            "labels": [
                "问询",
                "招呼",
                "欢迎",
                "告别",
                "请求信息(Q)",
                "告知信息(I)",
                "无法满足(N)",
                "提供选择(S)",
                "推荐(R)",
            ]
        },

        "预订信息": {
            "description": "服务订单信息: 左侧为订单明细，右侧为产生的轮次",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": False,
            "model": BookingInfoDummyModel(),
            "labels": [
                "领域",
                "订单号",
                "名称(或列车号)",
                "日期(入住/就餐)",
                "时间(就餐)",
                "天数(入住)",
                "人数"
            ]
        },

        "响应-预订": {
            "description": "服务订单响应信息: 1.多条同类标签采用逗号分隔; 2.左侧为响应内容，右侧为类别和位置。",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": True,
            "model": SlotDummyModel('Booking', b_res=True),
            "labels": [
                "订单号",
                "名称(或列车号)",
                "日期(入住/就餐)",
                "时间(就餐)",
                "天数(入住)",
                "人数"
            ]
        },

        "响应-酒店": {
            "description": "酒店业务响应信息: 1.多条同类标签采用逗号分隔; 2.左侧为响应内容，右侧为类别和位置。",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": True,
            "model": SlotDummyModel('Hotel', b_res=True),
            "labels": [
                "可能选择",
                "酒店名称",
                "酒店星级",
                "停车信息",
                "酒店网络",
                "入住人数",
                "入住日期",
                "入住天数",
                "类型",
                "价格",
                "方位",
                "电话",
                "邮编",
                "地址"
            ]
        },

        "响应-餐馆": {
            "description": "餐馆业务响应信息: 1.多条同类标签采用逗号分隔; 2.左侧为响应内容，右侧为类别和位置。",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": True,
            "model": SlotDummyModel('Restaurant', b_res=True),
            "labels": [
                "可能选择",
                "餐馆名称",
                "餐馆口味",
                "就餐人数",
                "就餐日期",
                "就餐时间",
                "价格",
                "方位",
                "电话",
                "邮编",
                "地址"
            ]
        },

        "响应-旅游": {
            "description": "旅游业务响应信息: 1.多条同类标签采用逗号分隔; 2.左侧为响应内容，右侧为类别和位置。",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": True,
            "model": SlotDummyModel('Attraction', b_res=True),
            "labels": [
                "可能选择",
                "景点名称",
                "类型",
                "费用",
                "方位",
                "电话",
                "邮编",
                "地址"
            ]
        },

        "响应-医院": {
            "description": "医院业务响应信息: 1.多条同类标签采用逗号分隔; 2.左侧为响应内容，右侧为类别和位置。",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": True,
            "model": SlotDummyModel('Hospital', b_res=True),
            "labels": [
                "可能选择",
                "医院名称",
                "医院科室",
                "方位",
                "电话",
                "邮编",
                "地址"
            ]
        },

        "响应-警察": {
            "description": "警察业务响应信息: 1.多条同类标签采用逗号分隔; 2.左侧为响应内容，右侧为类别和位置。",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": True,
            "model": SlotDummyModel('Police', b_res=True),
            "labels": [
                "可能选择",
                "警察局名称",
                "方位",
                "电话",
                "邮编",
                "地址"
            ]
        },

        "响应-火车": {
            "description": "火车业务响应信息: 1.多条同类标签采用逗号分隔; 2.左侧为响应内容，右侧为类别和位置。",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": True,
            "model": SlotDummyModel('Train', b_res=True),
            "labels": [
                "可能选择",
                "列车号",
                "出发日期",
                "乘车人数",
                "出发时间",
                "出发地",
                "目的地",
                "到达时间",
                "历时",
                "票价"
            ]
        },

        "响应-出租车": {
            "description": "出租车业务响应信息: 1.多条同类标签采用逗号分隔; 2.左侧为响应内容，右侧为类别和位置。",
            "label_type": "multilabel_classification_string_r",
            "required": False,
            "apply_end": "Sys",
            "slot_rsp": True,
            "model": SlotDummyModel('Taxi', b_res=True),
            "labels": [
                "可能选择",
                "出租车型",
                "出发时间",
                "出发地",
                "目的地",
                "到达时间",
                "电话"
            ]
        },

    }

    @staticmethod
    def validate_dialogue(dialogue: List[Dict[str, Any]]) -> Union[str, List[Dict]]:
        """
        validates the dialogue and makes sure it conforms to the configDict
        """

        for i, turn in enumerate(dialogue):

            for labelName, info in Configuration.configDict.items():

                try:
                    turn[labelName]
                except KeyError:
                    if info["required"]:
                        return "ERROR1: 标签 \'{}\' 在配置文件 (annotator_config.py) 中被定义为 \"required\"， " \
                               "但在所提供对话的轮次 {} 中缺失该标签.".format(labelName, i)
                    else:
                        continue

                if info["required"] and not turn[labelName]:
                    return "ERROR2: 必填标签, \'{}\', 在所提供对话的轮次 " \
                           " {} 中找不到值".format(labelName, i)

                if "multilabel_classification" == info["label_type"] or \
                    "multilabel_classification_r" == info["label_type"]:

                    providedLabels = turn[labelName]

                    if not all(x in info["labels"] for x in providedLabels):
                        return "ERROR3: 对话轮次 {} 的列表中的部分标签值: \'{}\' " \
                               "在配置文件(annotator_config.py)中无定义（非法值）. ".format(i, providedLabels)

        return dialogue



    @staticmethod
    def create_annotation_dict():
        """
        Generates a dictionary mapping label names to a dictionary of their description, label types
        and, if applicable, the possible values the label can take.
        """
        out = {}

        for key,value in Configuration.configDict.items():

            temp = list(value["labels"]) if value.get("labels") else ""

            out[key] = {
                "label_type": value["label_type"],
                "labels": temp,
                "info": value["description"],
                "apply_end": value["apply_end"],
                "slot_rsp": value["slot_rsp"]
            }

        return out


    @staticmethod
    def create_empty_turn(query):
        """
        creates an empty turn based on the configuration dictionary
        """
        out = {}

        for key,value in Configuration.configDict.items():

            labelType = value["label_type"]

            if labelType == "data":
                out[key] = query

            elif labelType in ["multilabel_classification", "multilabel_classification_r",
                               "multilabel_classification_string", "multilabel_classification_string_r"]:
                out[key] = []

            elif labelType == "string":

                out[key] = ""

            else:

                raise ValueError("The label type, {}, is not supported"
                                 .format(labelType))

        return out








##############################################
#  MAIN
##############################################


# EOF
