from tkinter import *
from tkinter import ttk
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
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Colaborador (Nome VARCHAR(45), DtNasc DATE, Lab VARCHAR(45), Funcao VARCHAR(45), CH INT, DtIngresso DATE, DtDesligamento DATE, Status VARCHAR(45), cpf VARCHAR(11), Senha VARCHAR(45) NOT NULL, PRIMARY KEY(cpf))")



def cadastrar_colaborador(tela_anterior, nome, DtNasc, Lab, Funcao, CH, DtIngresso, status, cpf, senha, confirma_senha):
	if senha.get()!=confirma_senha.get():
		inter.pop_up_confirma_senha()
	else:
		cursor = con.cursor
		conexao = con.conexao
		try:
			cursor.execute("INSERT INTO Colaborador (Nome, DtNasc, Lab, Funcao, CH, DtIngresso, Status, cpf, Senha) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome.get(), DtNasc.get(), Lab.get(), Funcao.get(), CH.get(), DtIngresso.get(), status.get(), cpf.get(), senha.get()))
			inter.pop_up_cadastro_valido()
			inter.chamar_tela_cadastro_colaborador(tela_anterior)
		except:
			inter.pop_up_cadastro_invalido()
		conexao.commit()

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

def retorna_lista_lab():
	cursor = con.cursor
	cursor.execute('''SELECT Nome
				   FROM Laboratorio''')
	lista = []
	for nome in cursor.fetchall():
		lista.append(str(nome[0]))
	return lista
	



def escolhe_tela(tela_anterior, login):
	if login.get() == "admin":
		inter.chamar_tela_inicial(tela_anterior)
	