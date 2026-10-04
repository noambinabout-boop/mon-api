import sqlite3
from abc import ABC, abstractmethod


class DataBase(ABC):

    def __init__(self, path):
        self.path = path
        
        self.connexion = sqlite3.connect(self.path)
        self.cursor = self.connexion.cursor()
        self.create_table()

    def execute_in_db(self, sql, parameters=()):
        try:
            self.cursor.execute(sql, parameters)
            self.connexion.commit()
            return True
            
        except sqlite3.Error as e:
            print("Erreur lors de l'insertion : ", e)
            return False

        

    def fetch_all(self, sql, parameters=()):
            try:
                self.cursor.execute(sql, parameters)
                self.connexion.commit()
                return self.cursor.fetchall()
            
            except sqlite3.Error as e:
                print("Erreur lors du fetch : ", e)
    
            return []
    
    def close_connextion(self):
        self.connexion.close()
        return
    
    @abstractmethod
    def create_table(self):
        pass

    
            



