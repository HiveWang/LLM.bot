import sqlite3 as sql
from contextlib import contextmanager


class sql_db:
    def __init__(self,db_name,lock=True,isolation_level='EXCLUSIVE'):
        self.db_name = db_name
        self.lock = lock
        self.isolation_level = isolation_level

    @contextmanager
    def __get_conn(self):
        self.__conn = sql.connect(self.db_name,timeout=10,isolation_level=self.isolation_level)
        if self.lock:
            self.__conn.execute('BEGIN IMMEDIATE TRANSACTION')
        try:
            yield self.__conn
        except:
            self.__conn.rollback()
            raise
        finally:
            self.__conn.commit()
            self.__conn.close()
            
        # # 加锁以避免多线程或多进程竞争写入
        # if lock:
        #     self.__cursor.execute('PRAGMA locking_mode=EXCLUSIVE')

    def __execute(self,query,*params):
        with self.__get_conn() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query,params)
                result = cursor.fetchall()
                # conn.commit()
                return result
            except Exception as e:
                print(e)
            # return self

    def insert_data(self,table_name,**params):
        fields = ','.join(params.keys())
        placeholders = ', '.join(['?' for _ in range(len(params))])
        query = f'INSERT INTO {table_name} ({fields}) VALUES ({placeholders})'
        try:
            self.__execute(query, *params.values())
        except:
            return "Duplicate primary key"
        # self.__conn.commit()   

    def create_tb(self,table_name,fields_str):
        # 检查表是否存在
        print(self.__table_exist(table_name))
        if self.__table_exist(table_name):
            print(f"Table '{table_name}' already exists!")
            result = f"Table '{table_name}' already exists!"
            return result
        # 如果表不存在，则创建表
        print("Creating tab.......")
        query = f'CREATE TABLE {table_name} ({fields_str})'
        self.__execute(query)
        
        # 查询表是否被成功创建
        if not self.__table_exist(table_name):
            raise RuntimeError(f'Failed to create table \"{table_name}\"!')


    
    def update_data(self,table_name,condition,**params):
        """更新数据"""
        update_str = ', '.join([f'{key} = ?' for key in params])
        query = f'UPDATE {table_name} SET {update_str} WHERE {condition}'
        self.__execute(query, *params.values())

 

    def query_data(self,table_name,fields='*',condition=None):
        """查询数据"""
        fields_str = ', '.join(fields) if fields else '*'
        query = f'SELECT {fields_str} FROM {table_name}'
        if condition:
            query += f' WHERE {condition}'
        cursor = self.__execute(query)
        return cursor   


    def __table_exist(self, table_name):
        # 检查表是否存在
        with self.__get_conn() as conn:
            cursor = conn.cursor()
            result = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'").fetchall()
            # print(result)
            if len(result) > 0:return True
            else: return False


if __name__ == "__main__":        
    db = sql_db('bjsw_gpt')
    print("connect -----------")
    table_name="bjsw_message_tb"
    creatb = '''CREATE TABLE IF NOT EXISTS bs_prompt_tb (
                    tenant_id TEXT,
                    app_id TEXT,
                    user_id TEXT ,
                    session_id TEXT,
                    convo_id TEXT PRIMARY KEY,
                    hist_message TEXT, 
                    state INTEGER,
                    create_time DATETIME DEFAULT (datetime('now')),
                    update_time DATETIME
                    )
        '''
    field_str = '''tenant_id TEXT,
                app_id TEXT,
                user_id TEXT ,
                session_id TEXT,
                convo_id TEXT PRIMARY KEY,
                hist_message TEXT, 
                state INTEGER,
                create_time DATETIME DEFAULT (datetime('now')),
                update_time DATETIME
                '''
    db.create_tb(table_name,field_str)

# #     #insert data.
    hist_messasge='''uuuuuuuuuuu
        '''
    user_id="HiveWang"
    db.insert_data(table_name,tenant_id="1111",
                    app_id="2222",
                    user_id=user_id,
                    session_id="999999777777777777777777",
                    convo_id="7777",
                    hist_message = hist_messasge,
                    state = 0,# valid
                )
    result = db.query_data(table_name,condition=f"user_id='{user_id}'")
    # result = db.query_data(table_name)

    print(len(result))
    print(result[0][5])
    # for i in result:
    #     print(i)

# #update 
#     # db.update_data(table_name, 'user_id = ?', session_id='9999999',convo_id='7777')
#     t=db.update_data(table_name, condition="session_id = \'000000\' and app_id=\'2222\'and user_id=\'3333\' and state = 0", hist_message='DDDDDDDDDfDDDDDDDDDDDDD', convo_id='DDDDDDD')
#     print(t)

#     # db.update_data(table_name,tenant_id="1111",
#     #                 app_id="2222",
#     #                 user_id="3333",
#     #                 session_id="5555",
#     #                 convo_id="7777",
#     #                 hist_message = hist_messasge,
#     #                 state = 0,# valid
# #     #             )
#     session_id = "0000000000000000"
#     user_id = "ddfpppppdd"
#     result = db.query_data(table_name,condition=f"session_id={session_id} and user_id='{user_id}'")
#     # db.insert_data(table_name,tenant_id="1111",
    #                 app_id="2222",
    #                 user_id=user_id,
    #                 session_id=session_id,
    #                 convo_id="7777",
    #                 hist_message = hist_messasge,
    #                 state = 0,# valid
    #             )





    # print(result)
    # if result:
    #     print("存在历史")
    # else:
    #     print("不存在，insert888888888888")


    # result = db.query_data(table_name,condition=f"session_id=={session_id} and user_id=='{user_id}'")
    # result = db.query_data(table_name)

    # print(result)
    # if result:
    #     print("存在历史")
    # else:
    #     print("不存在，insert")
        # db.insert_data(table_name,tenant_id="1111",
        #             app_id="2222",
        #             user_id=user_id,
        #             session_id=session_id,
        #             convo_id="7777",
        #             hist_message = hist_messasge,
        #             state = 0,# valid
        #         )
#     # import sqlite3

#     # with sqlite3.connect('example.db') as conn:
#     #     cursor = conn.cursor()

#     #     # 删除 bs_prompt_tb 表格
#     #     cursor.execute('DROP TABLE IF EXISTS bs_prompt_tb;')

