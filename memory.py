# -*- coding: utf-8 -*-
"""
@author: Xiaolan Zhu
@date: Created on 2023/5/28

"""
import ast
import pathlib
from update_prompt import UpdateSystemMessage
import json

class MessageHistory:

    def __init__(self):
        self._history = []

    def append_message(self, role: str, content: str):
        if role in ["system", "user", "assistant"]:
            msg = {
                "role": role,
                "content": content
            }
            self._history.append(msg)
        else:
            raise ValueError("role must be one of system, user and assistant")

    def get_dialogue(self, length=6, keep_system_message=True):
        if length >= len(self._history):length=len(self._history)-1
        if keep_system_message:
            # return self._history[:1] + self._history[-length:]
            return self._history[-length:] + self._history[:1]
            
        else:
            return self._history[-length:]


    def update_system_message(self,system_mgs:UpdateSystemMessage,**kwargs):
        try:
            system_mgs.update_system_message(**kwargs)
            system_message=system_mgs.system_message
            self._history[0]['content'] = system_message
        except KeyError as e:
            print("无法更新system messsage",e)
            

    def save_history(self, file_name):
        # raise error if file exists
        if pathlib.Path(file_name).exists():
            raise FileExistsError("file already exists")

        # save history as jsonl format
        with open(file_name, "w") as f:
            for msg in self._history:
                f.write(str(msg) + "\n")


    def save_history_json(self):
        # 保存历史消息为 JSONL 格式的字符串
        history_str = ''
        long_str = len(self._history)
        system_prompt = ""
        for msg in self._history:
            if msg['role'] == 'system':system_prompt=msg['content']
            history_str += json.dumps(msg,ensure_ascii=False) + '\n'
        # 返回历史消息字符串
        # history_str = "["+history_str+"]"
        return history_str,long_str,system_prompt


    def load_history_from_str(self,history_str):
    # 解码 JSONL 格式的字符串
        self._history = []
        for line in history_str.strip().split('\n'):
            self._history.append(json.loads(line))
        # 返回历史消息列表
        return self


    @staticmethod
    def load_history(file_name):
        # load history from jsonl format
        history = []
        with open(file_name, "r") as f:
            for line in f:
                history.append(ast.literal_eval(line))

        return history


    @property
    def history(self):
        return self._history

