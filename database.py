import sqlite3

def create_connection():
    connection = sqlite3.connect("Brain.db")
    return connection

def get_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM question_and_answer")
    return cursor.fetchall()

bot_list=list()
def get_question_and_answer():
    rows = get_table()
    for row in rows:
        print (row)
        bot_list.extend(list(row))
    return bot_list
    
