from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import SCF_interface as inter
import sqlite3
import os



def criar_conexao():
	global con
	con = Conexao()

class Conexao():
	def __init__(self):
		self.path = r"DataBase"
		self.conexao = sqlite3.connect(self.path + r"\SCF.db")
		self.cursor = self.conexao.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Laboratorio (Nome VARCHAR(45), Sigla VARCHAR(45), Logo BLOB, Image_type VARCHAR(3), PRIMARY KEY(Nome, Sigla))")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Colaborador (Nome VARCHAR(45), DtNasc DATE, Lab VARCHAR(45), Funcao VARCHAR(45), CH INT, DtIngresso DATE, DtDesligamento DATE, Status VARCHAR(45), cpf VARCHAR(11), Foto BLOB, Image_type VARCHAR(3), Senha VARCHAR(45) NOT NULL, PRIMARY KEY(cpf))")


def cadastrar_colaborador(tela_anterior, nome, DtNasc, Lab, Funcao, CH, DtIngresso, status, cpf, senha, confirma_senha, foto):
	if senha.get()!=confirma_senha.get():
		inter.pop_up("ERROR", "Confirme sua Senha!")
	else:
		cursor = con.cursor
		conexao = con.conexao

		try:
			if foto.get() != "":
				file_type = ImageMethods.get_file_type(foto.get())
				file_binary = ImageMethods.get_binary(foto.get())
				cursor.execute("INSERT INTO Colaborador (Nome, DtNasc, Lab, Funcao, CH, DtIngresso, Status, cpf, Foto, Image_type, Senha) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome.get(), DtNasc.get(), Lab.get(), Funcao.get(), CH.get(), DtIngresso.get(), status.get(), cpf.get(), file_binary, file_type, senha.get()))
			else:
				cursor.execute("INSERT INTO Colaborador (Nome, DtNasc, Lab, Funcao, CH, DtIngresso, Status, cpf, Foto, Image_type, Senha) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome.get(), DtNasc.get(), Lab.get(), Funcao.get(), CH.get(), DtIngresso.get(), status.get(), cpf.get(), None, None, senha.get()))

			inter.pop_up("SUCCESSFUL", "Cadastro Realizado com Sucesso")
			inter.chamar_tela_cadastro_colaborador(tela_anterior)
		except:
			inter.pop_up("ERROR", "Cadastro Inválido")
		conexao.commit()

def atualizar_cadastro_colaborador(tela_anterior, nome, DtNasc, Lab, Funcao, CH, DtIngresso, status, senha, confirma_senha, foto, nome_colab, cpf_colab):
	if senha.get()!=confirma_senha.get():
		inter.pop_up("ERROR", "Confirme sua Senha!")
	else:
		cursor = con.cursor
		conexao = con.conexao

		try:
			if foto.get() != "":
				file_type = ImageMethods.get_file_type(foto.get())
				file_binary = ImageMethods.get_binary(foto.get())
				cursor.execute('''UPDATE Colaborador 
					SET Nome = (?), DtNasc = (?), Lab = (?), Funcao=(?), CH=(?), DtIngresso=(?), Status=(?), Foto=(?), Image_type = (?), Senha=(?) WHERE cpf = (?) ''', (nome.get(), DtNasc.get(), Lab.get(), Funcao.get(), CH.get(), DtIngresso.get(), status.get(), file_binary, file_type, senha.get(), cpf_colab))
			else:
				cursor.execute('''UPDATE Colaborador 
					SET Nome=(?), DtNasc=(?), Lab=(?), Funcao=(?), CH=(?), DtIngresso=(?), Status=(?), Senha=(?) WHERE cpf = (?) ''', (nome.get(), DtNasc.get(), Lab.get(), Funcao.get(), CH.get(), DtIngresso.get(), status.get(), senha.get(), cpf_colab))
			inter.pop_up("SUCCESSFUL", "Cadastro Atualizado com Sucesso")
		except:
			inter.pop_up("ERROR", "Cadastro Inválido")
		conexao.commit()

def cadastrar_laboratorio(tela_anterior, nome, sigla, logo):
	cursor = con.cursor
	conexao = con.conexao

	try:
		if logo.get() != "":
			file_type = ImageMethods.get_file_type(logo.get())
			file_binary = ImageMethods.get_binary(logo.get())
			cursor.execute("INSERT INTO Laboratorio VALUES (?, ?, ?, ?)", (nome.get(), sigla.get(), file_binary, file_type))
		else:
			cursor.execute("INSERT INTO Laboratorio VALUES (?, ?, ?, ?)", (nome.get(), sigla.get(), None, None))

		inter.pop_up("SUCCESSFUL", "Cadastro Realizado com Sucesso")
		inter.chamar_tela_cadastro_laboratorio(tela_anterior)
	except:
		inter.pop_up("ERROR", "Cadastro Inválido")
	conexao.commit()

def retorna_lista_lab():
	cursor = con.cursor
	cursor.execute('''SELECT Nome
				   FROM Laboratorio''')
	lista = []
	for nome in cursor.fetchall():
		lista.append(str(nome[0]))
	return lista

def retorna_lista_colab(lab):
	cursor = con.cursor
	cursor.execute("SELECT Nome FROM Colaborador WHERE Lab = '%s'"%lab.get())
	lista = []
	for nome in cursor.fetchall():
		lista.append(str(nome[0]))
	return lista

class Colaborador():
	def __init__(self, nome, DtNasc, Lab, Funcao, CH, DtIngresso, status, cpf, Senha):
		self.nome = nome
		self.DtNasc = DtNasc
		self.Lab = Lab
		self.Funcao = Funcao
		self.CH = CH
		self.DtIngresso = DtIngresso
		self.status = status
		self.cpf = cpf
		self.Senha = Senha

def retorna_colab(nome):
	cursor = con.cursor
	cursor.execute("SELECT * FROM Colaborador WHERE Nome = '%s'"%nome.get())
	lista = cursor.fetchall()
	tupla = lista[0]
	colab = Colaborador(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[7], tupla[8], tupla[11])
	return colab

class ImageMethods():
	@staticmethod
	def get_path(line_path):
		tk_dialog = Tk()
		tk_dialog.withdraw()
		file_types=[('PNG file',"*.png"), ('JPG file', "*.jpg")]
		file_name = askopenfilename(filetypes=file_types, title="Selecione o logo")
		line_path.set(file_name)
		tk_dialog.destroy()

	@staticmethod
	def get_binary(image_path):
		binary = ''
		with open(image_path, 'rb') as image:
			binary = image.read()
		return binary

	@staticmethod
	def get_file_type(image_path):
		file_type = ""
		for i in range(-3,0):
			file_type = file_type + image_path[i]
		return  (file_type)

def validar_login(tela_anterior, login):
	if login.get() == "admin":
		inter.chamar_tela_inicial(tela_anterior)
	else:
		inter.pop_up("ERROR", "Login ou Senha Inválida")
	
def validar_consulta(tela_anterior, lab):
	if lab.get() != "":
		inter.chamar_tela_consulta_2(tela_anterior, lab)
	else:
		inter.pop_up("ERROR", "Consulta Inválida")

def validar_consulta_2(tela_anterior, nome_colab):
	try:
		colab = retorna_colab(nome_colab)
		inter.chamar_tela_dados_colaborador(tela_anterior, nome_colab)
	except:
		inter.pop_up("ERROR", "Consulta Inválida")
