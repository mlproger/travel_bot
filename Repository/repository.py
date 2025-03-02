from abc import ABC, abstractmethod
from typing import Any
import psycopg2


class AbstractRepository(ABC):

    @abstractmethod
    def add():
        raise NotImplementedError
    
    @abstractmethod
    def get():
        raise NotImplementedError
    
    @abstractmethod
    def update():
        raise NotImplementedError
    
    @abstractmethod
    def create_table():
        raise NotImplementedError
    
    @abstractmethod
    def add_by_msg():
        raise NotImplementedError
    
    @abstractmethod
    def delete():
        raise NotImplementedError
    
    

    

class Repository(AbstractRepository):
    tables = None
    init_msg = None
    try:
        # __conn = psycopg2.connect(dbname = "postgres", user = "postgres", password = "postgres", host = "localhost", port = "5432")
        __conn = psycopg2.connect(dbname = "postgres", user = "postgres", password = "postgres", host = "bot_db", port = "5432")
    except:
        print("BAD CONNETC")


    def add(self, data: dict):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(f"SELECT column_name, data_type FROM information_schema. columns WHERE table_name = '{self.tables}'")
            names = dict(cursor.fetchall())
            names = list(names.keys())
            names.pop(0)
            f = f"""INSERT INTO {self.tables} ({",".join(str(x) for x in names)}) VALUES {*data.values(),}"""
            cursor.execute(f)
            self.__conn.commit()
        except:
            self.__conn.rollback()
            return "Error"


    def get(self, id: str, offset=0, id_trip = 0, name = "", flag = 0):
        cursor = self.__conn.cursor()
        if flag == -3:
            cursor.execute(f"SELECT * FROM {self.tables} where id_trip = '{id_trip}'")
        elif id_trip == -2:
            cursor.execute(f"SELECT * FROM {self.tables} where name = '{name}'")
        elif id_trip == -1:
            cursor.execute(f"SELECT * FROM {self.tables} where id = '{id}'")
        elif id_trip == 0:
            cursor.execute(f"SELECT * FROM {self.tables} where entity_id = '{id}' limit 5 offset {offset}")
        else:
            cursor.execute(f"SELECT * FROM {self.tables} where id = '{id_trip}' limit 5 offset {offset}")
        try:
            entity = cursor.fetchall()
            print(entity[0])
            cursor.execute(f"SELECT column_name, data_type FROM information_schema. columns WHERE table_name = '{self.tables}' ORDER BY ordinal_position ASC;")
            names = list(dict(cursor.fetchall()))
            data = []

            for i in entity:
                data_dict = {}
                for j in zip(names, i):
                    data_dict[j[0]] = j[1]
                    
                data.append(data_dict)
                print(data)

                        
        except IndexError as e:
            print(e)
            return 0

            
        return data
            

    def create_table(self):
        cursor = self.__conn.cursor()
        cursor.execute(self.init_msg)
        self.__conn.commit()


    def update(self, field: str, value: Any, id: str):
        try:
            cursor = self.__conn.cursor()
            f = f"UPDATE {self.tables} set {field} = '{value}' WHERE entity_id = '{id}'"
            cursor.execute(f)
            self.__conn.commit()
        except:
            self.__conn.rollback()
            return "Error"


    def add_by_msg(self, msg: str):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(msg)
            self.__conn.commit()
        except Exception as e:
            print(e)
            self.__conn.rollback()
            return "Error"

    def __init__(self) -> None:
        super().__init__()
        self.create_table()

    def delete(self, msg: str):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(msg)
            self.__conn.commit()
        except Exception as e:
            print(e)
            self.__conn.rollback()
            return "Error"
