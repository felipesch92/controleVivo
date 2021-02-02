import sqlite3
from sqlite3 import Error


def conexao_banco():
    try:
        conn = sqlite3.connect('banco.db')
    except Error as ex:
        print(ex)
    return conn


def dql(query): #select
    vcon = conexao_banco()
    c = vcon.cursor()
    c.execute(query)
    res = c.fetchall()
    vcon.close()
    return res


def dml(query): #insert, update, delete
    try:
        vcon = conexao_banco()
        c = vcon.cursor()
        c.execute(query)
        vcon.commit()
        vcon.close()
    except Error as ex:
        print(ex)