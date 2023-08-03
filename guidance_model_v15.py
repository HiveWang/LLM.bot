import openai
from memory import MessageHistory
from colorama import Fore, Back, Style
import ast
from functools import partial
import os
from config import openai_conf,proxy
import tiktoken
import json

# proxy = 'http://127.0.0.1:2001'#local

os.environ['http_proxy'] = proxy['proxy'] 
os.environ['HTTP_PROXY'] = proxy['proxy'] 
os.environ['https_proxy'] = proxy['proxy'] 
os.environ['HTTPS_PROXY'] = proxy['proxy'] 
os.environ["OPENAI_API_KEY"]=openai_conf['azure']['api_key']  #azure



#Azure account
temperature = openai_conf['temperature']
openai.api_key = openai_conf['azure']['api_key']
openai.api_base = openai_conf['azure']['api_base']
openai.api_type = 'azure'
openai.api_version = openai_conf['azure']['api_version']
api_engine: str = openai_conf['azure']['api_engine']

def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


class GuidanceModel:

    def __init__(self,api_engine,temperature=0.3):
        openai.api_key = openai_conf['azure']['api_key']
        openai.api_base = openai_conf['azure']['api_base']
        openai.api_type = 'azure'
        openai.api_version = openai_conf['azure']['api_version']
        os.environ["OPENAI_API_KEY"]=openai_conf['azure']['api_key']  #azure
        self.model = partial(openai.ChatCompletion.create,
                            model=api_engine,
                            engine=api_engine,  
                            # stream=False,
                            temperature=temperature)

    def get_response(self, interview_history: MessageHistory,logger,stream=False):
        message = interview_history.get_dialogue(length=5)
        openai.api_key = openai_conf['azure']['api_key']
        openai.api_base = openai_conf['azure']['api_base']
        openai.api_version = openai_conf['azure']['api_version']
        os.environ["OPENAI_API_KEY"]=openai_conf['azure']['api_key']  #azure
        api_engine: str = openai_conf['azure']['api_engine']
        logger.info("The final message:")
        logger.info(f"Model:{api_engine}")
        logger.info(f"Key:{openai.api_key}")
        logger.info("--------------------------------------------------------------")
        for i in message:
            logger.info(i['role'])
            logger.info(i['content'])

        response = self.model(
            messages=message,#返回最后4个消息
            stream=stream
        )
        return response


    
    def run(self, history: MessageHistory,stream,logger,max_retry=6):

        num_retry = 0

        while num_retry < max_retry:
            try:
                response = self.get_response(history,logger,stream)
                logger.info(f"Retry -{num_retry}")
                if stream:
                    logger.info("Streaming start.....")
                    
                    return response,"Null"
                    
                response,usage=GuidanceModel.parse_response(response)
                return response,usage
                
            except Exception as e:
                num_retry += 1
                print(Fore.RED + f"Error: {e}")

        return None

    
    @staticmethod
    def fix_model_response(response):
        if isinstance(response, str):

            response = ast.literal_eval(response)
            if "your answer" in response:
                response.pop("your answer")

        return response

    
    @staticmethod
    def parse_response(response):
        # response = fix_model_response(response)

        message = response['choices'][0]['message']['content']
        # print(response)
        # print("=" *200)
        # message = GuidanceModel.fix_model_response(message)

        return message,response['usage']

    
if __name__ == "__main__":
    m = GuidanceModel()
    print("hello")

