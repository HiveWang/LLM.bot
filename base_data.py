# -*- coding: utf-8 -*-
# @date: 2023/4/26
# @file: base_data .py
# 
# @author: lingjing.lin
from pydantic import BaseModel
from typing import Optional, List
import time


class FlowStrategyConf(BaseModel):
    flow_type: str
    conf: dict = {}


class Role(BaseModel):
    name: Optional[str] = "bot" #bot|helpdesk|system|user，未提供则默认为bot
    type: Optional[str] = None #name=system的情况下，区分tip|verbose | action|loading


class BaseRequest(BaseModel):
    # must
    ver: str = "1.0"  # 默认1.0
    tenantId: Optional[str] = None # 租户ID
    appId: Optional[str] = None  # 使用系统定义，不使用外部如企微定义
    userId: Optional[str] = None # 用户ID
    sessionId: Optional[str] = None  # 标识属于某一个会话
    convoId: Optional[str] = None  # 标识属于某一个对话
    reqId: Optional[str] = None  # 请求ID
    reqType: Optional[str] = None  # h5|wxwork
    reqTime: Optional[int] = None  # 请求时间
    req: Optional[str] = None  # 请求内容
    machineId: Optional[str] = None  # 机器ID
    modeId: Optional[str] = "sinopharm"  #

    # end

    # flow property
    flowConf: Optional[dict] = None  # 流程定义
    flowVar: Optional[dict] = None   # 流程变量

    # 0605 modified for rebecca, init = true,触发服务端流程（用户刚登录/ clear chat.round）
    ext: Optional[dict] = None

    # 以下暂未实现
    # 0526 added
    format: Optional[str] = ''
    # 0608 modified 补充标识说明，暂未实现
    # init: name = system, type = init
    # msg:  name = user, type = msg
    role: Optional[Role] = None

    # 以下deprecated 0621
    uid: Optional[str] = None
    chatMode: Optional[int] = None
    flowId: Optional[int] = None
    chatSessionKey: Optional[str] = ''
    chatHistoryKey: Optional[str] = ''
    flowKey: Optional[str] = 'flow:default:0'  # 默认值用来兼容老代码
    flowType: str = "0"
    modeId: Optional[str] = None  # 0608 added /mode:x指令后或者默认登录模式的模式id


class ResponseData(BaseModel):
    # must
    tenantId: Optional[str] = None   # 租户ID，必须从req中获取
    appId: Optional[str] = None      # 应用ID，必须从req中获取
    userId: Optional[str] = None     # 用户ID，必须从req中获取
    sessionId: Optional[str] = None  # 标识属于某一个会话，必须从req中获取
    convoId: Optional[str] = None  # 标识属于某一个对话，必须从req中获取
    reqId: Optional[str] = None    # 请求ID，必须从req中获取
    reqType: Optional[str] = None  # h5|wxwork，必须从req中获取
    modeId: Optional[str] = None # 回复ID，唯一即可
    respId: Optional[str] = None    # 回复ID，唯一即可
    resp: Optional[str] = None      # 回复内容
    respSeq: Optional[int] = 0      # 如果使用流式回复，该值用于标识内容的顺序，Int,默认0
    respStop: Optional[str] = True  # 如果使用流式回复，标识该回复是否已经完整结束，true|false
    reqTime: Optional[int] = None
    respTime: Optional[int] = None
    # resp: name = bot, type = action
    # tip:  name = system, type = tip
    # verbose:  name = system, type = verbose
    # loading:  name = system, type = loading
    role: Optional[Role] = None      # 角色定义，默认为bot+action（需要主动设置）
    format: Optional[str] = 'text'  # 答案类型 默认为text，text|json|csv
    # end

    # 以下均为可选项
    originResp: Optional[str] = None
    hdId: Optional[str] = None
    # 230615 added
    display: Optional[str] = None,  # 展示类型, ""|md|table|image|audio|video|file|link|chart_bar|chart_line|chart_pie
    machineId: Optional[str] = None
    # 230602 added
    # 1. 存在上下文菜单，menuEnabled: true|false (默认为空或者false)
    # 2. 存在原始回复内容，originalResp: json str
    # 3. 指定tip的图标，icon: str
    ext: Optional[dict] = None
    

class BaseResponse(BaseModel):
    ver: Optional[str] = '1.0'
    code: Optional[int] = None  # 0:成功，非0:失败
    time:  Optional[str] = None  # 时间戳
    data: Optional[ResponseData] = None


    
    