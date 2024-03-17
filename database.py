import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))
# print(sys.path)

import random
import psycopg2
import config

class DataBase:

    con: None

#! ****************************************COMMANDS FOR FILL CHANNELS********************************
    def __init__(self):
        try: 
            self.con = psycopg2.connect(
                host=config.host,
                user=config.db_user,
                password= config.password,
                database=config.db_name,
                port= config.port
            )
            self.con.autocommit = True

        except Exception as ex:
            print('posgresql exception: ', ex)

    def get_answer(self,channel_link: str) -> tuple:
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT channel_link FROM channels WHERE channel_link = '{}'".format(channel_link)
                )
            answer = cur.fetchone()
       
        return answer


    def get_chan_id(self,channel_link:str) -> int:
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT channel_id FROM channels WHERE channel_link = '{}'".format(channel_link)
                )
            channel_id = cur.fetchone()[0]
        return int(channel_id)   
        

    def get_anime_name(self, channel_link) -> str:
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT channel_name FROM channels WHERE channel_link='{}'".format(channel_link)
                )
            name = cur.fetchone()[0]    
        return name


    def get_counts(self,table_name:str) -> [str, str, str]:
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT seria FROM {}".format(table_name)
                )
            data = cur.fetchall()
            
        seria_count = len(data)
        last_seria = data[-1][0]
        last_count_str = last_seria.replace('Сезон ', '').replace('Серия ','')
        last_count_list = last_count_str.split(' ')
     
        if len(last_count_list) == 1:
            last_season= '1'
            last_seria = last_count_list[0]
            return [seria_count, last_seria, last_season]

        return [seria_count, last_count_list[1], last_count_list[0]]


    def get_url(self,channel_link:str) -> str:
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT url FROM channels WHERE channel_link='{}'".format(channel_link)
                )
            url = cur.fetchone()[0]    
        return url


    def insert_seria(self,table_name:str, msg_id: int, seria: str, title: str, rowid:int):
        with self.con.cursor() as cur:
            cur.execute(
                "INSERT INTO {} (msg_id, seria, title,rowid) VALUES ({} , '{}', '{}', {})".format(table_name, msg_id, seria, title,rowid)
                )
        return      


    def insert_chan_info(self,url,chan_name,chan_link):
        search = chan_name.lower()
        with self.con.cursor() as cur:
            cur.execute(
                "INSERT INTO channels (channel_name, channel_link, search,url) VALUES (%s , %s, %s, %s)",(chan_name,chan_link, search,url)
                )
        return

    
    def insert_data_info(self,channel_link:str, msg_id: int, description: str):
        with self.con.cursor() as cur:
            cur.execute(
                "INSERT INTO anime_info (channel_link, msg_id, description) VALUES ('{}', '{}', '{}')".format(channel_link,msg_id, description)
                )
        return        


    def set_chan_id(self,chan_id:str, channel_name:str):
        with self.con.cursor() as cur:
            cur.execute(
                "UPDATE channels SET channel_id='{}' WHERE channel_name='{}'".format(chan_id, channel_name)                )
        return


    def set_url(self,  url: str, channel_link: str):
        
        with self.con.cursor() as cur:
            cur.execute(
                "UPDATE channels SET url='{}' WHERE channel_link='{}'".format(url,channel_link)
                )


    def create_tables(self, table_name: str):
        with self.con.cursor() as cur:
            cur.execute(
                """ CREATE TABLE {}(
                    msg_id int PRIMARY KEY,
                    seria varchar(30) NOT NULL,
                    title varchar(60) NOT NULL,
                    rowid int DEFAULT 0);
                """.format(table_name)
                )
        return




    # def create_table(self):
    #     with self.con.cursor() as cur:
    #         cur.execute(
    #             """ CREATE TABLE users(
    #                 user_id varchar(20) PRIMARY KEY,
    #                 username TEXT,
    #                 nickname varchar(33) NOT NULL );
    #             """
    #             )
    #     return

# ! *****************************************COMMANDS FOR USER INTERFACE***********************************

    def add_or_update_user(self,user_id,username,nickname):
        try:
            with self.con.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (user_id, username, nickname) VALUES ('{}' , '{}', '{}')".format(user_id, username, nickname)
                    )
        except psycopg2.errors.lookup('23505'):
            with self.con.cursor() as cur:
                cur.execute(
                    "UPDATE users SET username='{}', nickname='{}' WHERE user_id='{}'".format(username, nickname, user_id)
                    )
        except Exception as ex:
            print(ex)


    def search_anime_request(self, pattern:str) -> list:
        pattern = pattern.lower()
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT channel_name FROM channels WHERE search LIKE '%{}%'".format(pattern)
                )           

            response = cur.fetchall() #[(channel_name1,),(channel_name2,),(channel_name3,)]
            return response


    def get_link(self,channel_name:str) -> str:
        try:
            with self.con.cursor() as cur:
                cur.execute(
                    "SELECT channel_link FROM channels WHERE channel_name='{}'".format(channel_name)
                    )
                link = cur.fetchone()[0]    
                return link
        except Exception:
            return False


    def get_infodata(self, link:str) -> [str,str,str]:
        try: 
            with self.con.cursor() as cur:
                cur.execute(
                    "SELECT msg_id, description FROM anime_info WHERE channel_link='{}'".format(link)
                    )
                data = cur.fetchone()
                msg_id = data[0]
                desc = data[1]

            return link, msg_id, desc
        
        except TypeError:
            msg_id = '538' #message, in which we talk about lack of information
            desc = """Информация по данному аниме еще не указана☹️
Постараемся заполнить ее в ближайшее время❤️

P.S. Однако вы все же можете приступить к просмотру
"""
            return link, msg_id, desc


    def get_seria_data(self, table_name: str, seria_num: int) -> [int, str, str]:
        try:
            with self.con.cursor() as cur:
                cur.execute(
                    "SELECT msg_id, seria, title FROM {} WHERE rowid={}".format(table_name, seria_num)
                    )
                data = cur.fetchone()
                msg_id = data[0]
                seria = data[1]
                title = data[2]

            return msg_id, seria, title
        except TypeError:
            return False, False, False


    def get_random_link(self,*args) -> str:
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT channel_link FROM channels"
                )
            data = cur.fetchall()  
            return random.choice(data)[0]


    def get_users(self, param=None) -> tuple:

        with self.con.cursor() as cur:
            if param:
                cur.execute(
                    "SELECT {} FROM users".format(param)
                    )
            else:
                cur.execute(
                    "SELECT * FROM users"
                    )

            data = cur.fetchall()

        return data


database = DataBase()

if __name__ == '__main__':
    db = DataBase()
    print(db.get_users('user_id'))