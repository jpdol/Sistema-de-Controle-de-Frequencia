from tkinter import *
import SCF_interface as inter
import sqlite3

def criar_conexao():
	global con
	con = Conexao()

class Conexao():
	def __init__(self):
		self.path = r"C:\Users\ADM\Desktop\SCF\DataBase"
		self.conexao = sqlite3.connect(self.path+r"\SCF.db")
		self.cursor = self.conexao.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Laboratorio (Nome VARCHAR(45), Sigla VARCHAR(45), PRIMARY KEY(Nome, Sigla))")

def cadastrar_colaborador(tela_anterior):
	pass

def cadastrar_laboratorio(tela_anterior, nome, sigla):
	cursor = con.cursor
	conexao = con.conexao
	try:
		cursor.execute("INSERT INTO Laboratorio VALUES (?, ?)", (nome.get(), sigla.get()))
		inter.pop_up_cadastro_valido()
		inter.chamar_tela_cadastro_laboratorio(tela_anterior)
	except:
		inter.pop_up_cadastro_invalido()
	conexao.commit()

def escolhe_tela(tela_anterior, login):
	if login.get() == "admin":
		inter.chamar_tela_inicial(tela_anterior)
	