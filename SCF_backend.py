from tkinter import *
import SCF_interface as inter
import sqlite3


def db_connection():
	path = r"C:\Users\ADM\Desktop\SCF\DataBase"
	conexao = sqlite3.connect(path+r"\SCF.db")
	cursor = conexao.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS Laboratorio (Nome VARCHAR(45), Sigla VARCHAR(45))")
	return (cursor, conexao)

def commit_into_db(conexao):
	con = conexao
	con.commit()

def cadastrar_colaborador(tela_anterior):
	pass

def cadastrar_laboratorio(tela_anterior, nome, sigla):
	cursor = db_connection()[0]
	conexao = db_connection()[1]
	cursor.execute("INSERT INTO Laboratorio (Nome, Sigla) VALUES (%s, %s)"%(nome.get(), sigla.get()))
	commit_into_db(conexao)



def escolhe_tela(tela_anterior, login):
	if login.get() == "admin":
		inter.chamar_tela_inicial(tela_anterior)
	