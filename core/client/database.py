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
    # cur = connection.cursor()
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

    # def create_tables(self):# channel_id, channel_name, channel_url
    #     with self.con.cursor() as cur:
    #         cur.execute(
    #             """ CREATE TABLE channels(
    #                 channel_id TEXT PRIMARY KEY,
    #                 channel_name varchar(65) NOT NULL,
    #                 channel_link varchar(45) NOT NULL);
    #             """
    #             )
    #     return

database = DataBase()

if __name__ == '__main__':
    db = DataBase()
    db.test()
    # db.create_tables()