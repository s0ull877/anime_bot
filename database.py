import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))
# print(sys.path)

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
        

    def insert_chan_info(self,chan_id,chan_name,chan_link):
        with self.con.cursor() as cur:
            cur.execute(
                "INSERT INTO channels (channel_id, channel_name, channel_link) VALUES (%s , %s, %s)",(chan_id,chan_name,chan_link)
                )
        return



    def get_chan_id(self,channel_link:str) -> int:
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT channel_id FROM channels WHERE channel_link = '{}'".format(channel_link)
                )
            channel_id = cur.fetchone()[0]
        
        return int(channel_id)   


    def create_tables(self, table_name: str):
        with self.con.cursor() as cur:
            cur.execute(
                """ CREATE TABLE {}(
                    msg_id int PRIMARY KEY,
                    seria varchar(30) NOT NULL,
                    title varchar(60) NOT NULL);
                """.format(table_name)
                )
        return



    def insert_seria(self,table_name:str, msg_id: int, seria: str, title: str):
        with self.con.cursor() as cur:
            cur.execute(
                "INSERT INTO {} (msg_id, seria, title) VALUES ({} , '{}', '{}')".format(table_name, msg_id, seria, title)
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











database = DataBase()

if __name__ == '__main__':
    db = DataBase()
    # db.create_table()
    # db.add_or_update_user('1215105453', '😃💁;', 'adwada')