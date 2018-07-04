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
		self.path = r"C:\Users\ADM\Desktop\SCF\DataBase"
		self.conexao = sqlite3.connect(self.path+r"\SCF.db")
		self.cursor = self.conexao.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Laboratorio (Nome VARCHAR(45), Sigla VARCHAR(45), Logo VARCHAR(45), PRIMARY KEY(Nome, Sigla))")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Colaborador (Nome VARCHAR(45), DtNasc DATE, Lab VARCHAR(45), Funcao VARCHAR(45), CH INT, DtIngresso DATE, DtDesligamento DATE, Status VARCHAR(45), cpf VARCHAR(11), foto VARCHAR(45), Senha VARCHAR(45) NOT NULL, PRIMARY KEY(cpf))")


def cadastrar_colaborador(tela_anterior, nome, DtNasc, Lab, Funcao, CH, DtIngresso, status, cpf, senha, confirma_senha, foto):
	if senha.get()!=confirma_senha.get():
		inter.pop_up("ERROR", "Confirme sua Senha!")
	else:
		cursor = con.cursor
		conexao = con.conexao

		file_name = ImageMethods.get_file_name(foto.get(), cpf.get())
		foto_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagens","users",file_name)
		try:
			ImageMethods.save_image(foto.get(),"users", cpf.get())
			cursor.execute("INSERT INTO Colaborador (Nome, DtNasc, Lab, Funcao, CH, DtIngresso, Status, cpf, foto, Senha) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome.get(), DtNasc.get(), Lab.get(), Funcao.get(), CH.get(), DtIngresso.get(), status.get(), cpf.get(), foto_path, senha.get()))
			inter.pop_up("SUCCESSFUL", "Cadastro Realizado com Sucesso")
			inter.chamar_tela_cadastro_colaborador(tela_anterior)
		except:
			inter.pop_up("ERROR", "Cadastro Inválido")
		conexao.commit()

def cadastrar_laboratorio(tela_anterior, nome, sigla, logo):
	cursor = con.cursor
	conexao = con.conexao

	file_name = ImageMethods.get_file_name(logo.get(), nome.get())
	logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagens","labs",file_name )
	try:
		ImageMethods.save_image(logo.get(), "labs", nome.get())
		cursor.execute("INSERT INTO Laboratorio VALUES (?, ?, ?)", (nome.get(), sigla.get(), logo_path))
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
	def save_image(old_path, user_type, file_name):
		new_name = ImageMethods.get_file_name(old_path, file_name)
		new_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagens", user_type, new_name)
		with open(old_path, 'rb') as oi:
			with open(new_path, 'wb') as ni:
				for line in oi:
					ni.write(line)

	@staticmethod
	def get_file_name(image_path, name):
		file_type = ""
		for i in range(-4,0):
			file_type = file_type + image_path[i]
		return  (name + file_type)

def escolhe_tela(tela_anterior, login):
	if login.get() == "admin":
		inter.chamar_tela_inicial(tela_anterior)
	
