import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))
# print(sys.path)

import psycopg2
import config

class DataBase:

    con: None

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
            
                    
    def test(self):
        with self.con.cursor() as cur:
            cur.execute(
                "SELECT version();"
            )

            print(f'server version {cur.fetchone()}')
        return


    def insert_chan_info(self,chan_id,chan_name,chan_link):
        with self.con.cursor() as cur:
            cur.execute(
                "INSERT INTO channels (channel_id, channel_name, channel_link) VALUES (%s , %s, %s)",(chan_id,chan_name,chan_link)
                )
        return

    def create_tables(self, table_name: str):
        with self.con.cursor() as cur:
            cur.execute(
                """ CREATE TABLE %s(
                    msg_id int PRIMARY KEY,
                    seria varchar(30) NOT NULL,
                    title varchar(60) NOT NULL);
                """,(table_name)
                )
        return

    def insert_seria(self,table_name:str, msg_id: int, seria: str, title: str):
        with self.con.cursor() as cur:
            cur.execute(
                "INSERT INTO %s (msg_id, seria, title) VALUES (%s , %s, %s)",(table_name, msg_id, seria, title)
                )
        return      

database = DataBase()

if __name__ == '__main__':
    db = DataBase()
    db.test()
    # db.create_tables()