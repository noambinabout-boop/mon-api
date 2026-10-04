import sqlite3
from dataBaseManagment.dataBase import DataBase


class NotesDataBase(DataBase):

    def __init__(self, path):
        super().__init__(path)
        

    def insert_new_note(self, titre: str, note: str, date: str):
        sql = "INSERT INTO notes (title, note, date) VALUES (?, ?, ?);"
        return self.execute_in_db(sql, parameters=(titre, note, date))
               
    def delete_note_with_id(self, id: int):
        sql = "DELETE FROM notes WHERE id = ?;"
        return self.execute_in_db(sql, parameters=(id,))

    def create_table(self):
         sql = "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT NOT NULL, note TEXT NOT NULL, date TEXT NOT NULL);"
         self.execute_in_db(sql)
         self.connexion.commit()
         return True

    def get_notes_with_id(self, id: int):
         sql = "SELECT * FROM notes WHERE id = ?;"
         return self.fetch_all(sql, parameters=(id,))
         

    def get_notes_with_title(self, title: str):
        sql = "SELECT * FROM notes WHERE title = ?;"
        return self.fetch_all(sql, parameters=(title,))
        
    
