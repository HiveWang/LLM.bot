import sys
import time
import redis
from base_data import ResponseData,BaseRequest,BaseResponse
redis_conf ={
# 前端入口
# http://wxwork.aidea.meritco-group.com/dev/chat/user/#/login
    'qa': {
            'host': "114.55.65.101", # 阿里云上使用172.16.194.119内网地址  ;       外网使用'host': "114.55.65.101"
            'port': 6379,
            'password': "Meritco2016",
            'db': 0,
            'request_queue':'a:msg:req-sinopharm:0xTnEi:0E',# 请求队列
            'response_queue':'a:msg:resp-sinopharm:0xTnEi:0E:hEQKbf'# 响应队列
},
# 前端入口
# http://wxwork.aidea.meritco-group.com/qa/chat/user/#/login
    'dev': {
            'host': "47.98.109.236",  #阿里云上使用172.16.103.194内网地址 ;     外网使用 'host': "47.98.109.236",
            'port': 6379,
            'password': "Meritco2016",
            'db': 2,
            'request_queue':'a:msg:req-sinopharm:0xTnEi:0E',# 请求队列
            'response_queue':'a:msg:resp-sinopharm:0xTnEi:0E:hEQJYb'# 响应队列
}
    
# 连接Redis服务
r = redis.Redis(host=redis_conf['qa']['host'], port=redis_conf['qa']['port'], db=redis_conf['qa']['db'], password=redis_conf['qa']['password']) 


    
    
    
  # 进行一些处理并创建响应
def response_func(req:BaseRequest,resp:str,r:redis,logger):
    data = ResponseData(
        tenantId=req.tenantId,
        appId=req.appId,
        userId=req.userId,
        sessionId=req.sessionId,
        convoId=req.convoId,
        reqId=req.reqId,
        reqType=req.reqType,
        respId=req.reqId,#
        modeId="sinopharm",#
        role={'name':'bot'},
        resp=resp,
        reqTime=req.reqTime,
        display='text'
        )

    response = BaseResponse(
        ver='1.0',
        code=0,
        time=str(int(time.time())),
        data=data
    )

    # 将响应推入到队列中
    message = response.json(ensure_ascii = False)
        
    logger.debug(message)
    r.lpush(redis_conf['qa']['response_queue'], message)    

    
    
    
key, human_message = r.blpop(redis_conf['qa']['request_queue'], timeout=None)
        
# # 将消息转换为 BaseRequest 对象
req = BaseRequest.parse_raw(human_message)

#ai_message is response   
resp = ai_message
        # # 处理客户端问题
        
        
response_func(req,resp,r,logger)