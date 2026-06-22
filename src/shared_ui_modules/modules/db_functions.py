import sqlite3

from shared_ui_modules.modules.log_class import logger
from PySide6.QtCore import QObject

class SharedDbClass(QObject):
    def __init__(self, parent = None):
        super().__init__()

        
        self.db_name = None
        self.initial_query_list = []
        
        self.initialize_database()
        
    def get_db_name(self):
        return
    
    def get_query_list(self):
        return

    def initialize_module(self):
        try:
            self.initial_query_list = self.get_query_list()
            self.db_name = self.get_db_name()
            #variable setup

            if not self.initial_query_list or not self.db_name:
                raise(f"relevant components not recieved: {self.initial_query_list}, {self.db_name}")

            if self.db_name:
                self.conn = sqlite3.connect(self.db_name+".db")
                self.conn.execute("PRAGMA foreign_keys = ON;")#why do foreign keys need to be enabled?
                self.cur = self.conn.cursor()
                self.initialize_database()
        except Exception as e:
            logger.error(f"SharedDbClass initialize_module error: {e}")    

    #add returning to every query
    def execute_single_query(self,q=None,values=None):
        if q[len(q) - 1] != ";":
            logger.error(f"Não esqueça do ; na query: {q}")
            return
        res = ''
        try:
            if q and values:
                self.cur.execute(q,values)
            elif q and values == None:
                self.cur.execute(q)
            else:
                logger.error(f"Query: {q}\nValores: {q}")
                return
            res = self.cur.fetchall()
            self.conn.commit()
            if self.cur.rowcount == 0:
                return None
            else:
                return res
        except Exception as e:
            logger.error(f"SharedDbClass execute_single_query error: {e}\nquery: {q}")    
            
    def execute_multiple_queries(self,q=None,values_array=None):
        if q[len(q) - 1] != ";":
            logger.error(f"Não esqueça do ; na query: {q}")
            return
        res = ''
        try:
            if q and values_array:
                self.cur.executemany(q,values_array)
                res = self.cur.fetchall()
                self.conn.commit()
                if self.cur.rowcount == 0:
                    return None
                else:
                    return res
            else:
                logger.error(f"Query: {q}\nValores: {q}")
        except Exception as e:
            logger.error(f"SharedDbClass execute_multiple_queries error: {e}\nquery: {q}")    
             
    def initialize_database(self):
        for q in self.initial_query_list:
            self.execute_single_query(q)