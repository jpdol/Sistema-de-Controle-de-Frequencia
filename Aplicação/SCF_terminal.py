import serial
from tkinter import *
import sqlite3 
from functools import partial
from datetime import datetime
from PIL import Image, ImageTk
import io
import time
import os


class Conexao():
	def __init__(self):
		self.path = r"DataBase"
		self.conexao = sqlite3.connect(self.path + r"\SCF.db")
		self.cursor = self.conexao.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Digital (cpf VARCHAR(11), idDigital INT, PRIMARY KEY(cpf))")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS IdDisponivel (idDigital INT, disponivel INT, PRIMARY KEY(idDigital))")
		self.cursor.execute('''SELECT *
				   FROM IdDisponivel''')
		lista = []
		for nome in self.cursor.fetchall():
			lista.append(str(nome[0]))
		if len(lista)!=127:
			for i in range(127):
				self.cursor.execute("INSERT INTO IdDisponivel VALUES(?,?)", (i+1, 0))

		self.cursor.execute("CREATE TABLE IF NOT EXISTS Frequencia (cpf VARCHAR(11), entrada DATETIME, saida DATETIME, PRIMARY KEY(cpf, entrada))")
		self.conexao.commit()

#Conexao BD:
global con
con = Conexao()


#Conexao Serial:
porta = "COM7"
velocidade = 9600
conexao = serial.Serial(porta, velocidade)
linha = conexao.readline()

class Colaborador():
	def __init__(self, nome, dtNasc, lab, funcao, ch, dtIngresso, status, cpf, senha, foto):
		self.nome = nome
		self.dtNasc = dtNasc
		self.lab = lab
		self.funcao = funcao
		self.ch = ch
		self.dtIngresso = dtIngresso
		self.status = status
		self.cpf = cpf
		self.senha = senha
		self.foto = foto

def retorna_datetime():
	now = datetime.now()
	
	dia = str(now.day)
	if len(dia)<2:
		dia = '0'+dia
	
	mes = str(now.month)
	if len(mes)<2:
		mes = '0'+mes
	
	ano = str(now.year)
	
	hora = str(now.hour)
	if len(hora)<2:
		hora = '0'+hora
	
	minutos = str(now.minute)
	if len(minutos)<2:
		minutos = '0'+minutos
	
	segundos = str(now.second)
	if len(segundos)<2:
		mes = '0'+segundos
	
	
	data_hora = ano+'/'+mes+'/'+dia+' '+hora+':'+minutos+':'+segundos
	return data_hora

def retorna_user(cpf):
	cursor = con.cursor
	cursor.execute("SELECT * FROM Colaborador WHERE cpf = '%s'"%cpf)
	lista = cursor.fetchall()
	tupla = lista[0]
	colab = Colaborador(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[7], tupla[8], tupla[11], tupla[9])
	return colab

def retorna_lista_cadastrados():
	cursor = con.cursor
	cursor.execute("SELECT cpf FROM Digital")
	lista = cursor.fetchall()
	l = []
	for i in range(len(lista)):
		l.append(lista[i][0])
	return l
	
def retorna_posicao():
	cursor = con.cursor
	cursor.execute("SELECT idDigital FROM IdDisponivel WHERE disponivel=0")
	lista = cursor.fetchall()
	try:
		return lista[0][0]
	except:
		pop_up("ERROR", "Banco cheio")




def pegar_digital(tela_anterior, cpf):
	conexao.reset_input_buffer()
	conexao.write(b'e\r\n')
	entrada = conexao.readline()
	if (entrada==b'Pronto para receber\r\n'):
		idDigital = retorna_posicao()
		conexao.write(str.encode(str(idDigital)+'\r\n'))
		entrada = conexao.readline()
		if(entrada==b'Mete o dedo\r\n'):
			if(conexao.readline()==b'Remove finger\r\n'):
				if(conexao.readline()==b"Place same finger again\r\n"):
					if(conexao.readline()==b'Stored\r\n'):
						cursor = con.cursor
						cursor.execute(''' UPDATE IdDisponivel 
							SET  disponivel = (?) WHERE idDigital=(?)''',(1, int(idDigital)))

						cursor.execute("INSERT INTO  Digital VALUES (?,?)",(cpf, int(idDigital)))

						con.conexao.commit()

						pop_up("SUCCESSFUL", "Digital cadastrada com sucesso")
						

					else:
						pop_up("ERROR", "Erro no armazenamento")

				else:
					pop_up("ERROR", "Erro desconhecido")
			else:
				pop_up("ERROR", "Erro desconhecido")
		else:
			pop_up("ERROR", "Erro desconhecido")
	else:
		pop_up("ERROR", "Erro desconhecido")		
	

	pre_tela_principal(tela_anterior)


def marcar_frequencia(idDigital):
	cursor = con.cursor
	cursor.execute("SELECT cpf FROM Digital WHERE idDigital='%d'"%idDigital)
	cpf = str(cursor.fetchall()[0][0])
	cursor.execute("SELECT count(cpf) FROM Frequencia  WHERE cpf='%s' and saida IS NULL"%cpf)
	num = cursor.fetchall()[0][0]
	if num==1:
		cursor.execute('''UPDATE Frequencia 
					SET saida=(?) WHERE cpf=(?) AND saida is null''', (retorna_datetime(), cpf))
	elif num==0:
		cursor.execute("INSERT INTO Frequencia VALUES (?, ?, ?)", (cpf, retorna_datetime(), None))
	con.conexao.commit()
		
	

def validar_digital(tela_anterior):
	conexao.reset_input_buffer()
	confianca = 0
	tempo_inicial = time.time()
	tempo_atual = time.time()
	detectou = False
	while(confianca<90 and (tempo_atual-tempo_inicial)<10):
		tempo_atual = time.time()
		entrada = conexao.readline()
		if(entrada == b"Invalido\r\n"):
			continue
		else:
			idDigital = int(entrada)
			confianca = int(conexao.readline())

	if tempo_atual-tempo_inicial < 10:
		detectou = True


	if detectou:
		try:
			cursor = con.cursor
			cursor.execute("SELECT cpf FROM Digital WHERE idDigital='%d'"%idDigital)
			cpf = str(cursor.fetchall()[0][0])
			tela_anterior.destroy()
			marcar_frequencia(idDigital)
			
			cursor = con.cursor
			cursor.execute("SELECT cpf FROM Digital WHERE idDigital='%d'"%idDigital)
			cpf = str(cursor.fetchall()[0][0])
			cursor.execute("SELECT count(cpf) FROM Frequencia  WHERE cpf='%s' and saida IS NULL"%cpf)
			num = cursor.fetchall()[0][0]

			if num==0:
				chamar_perfil_saida(cpf)
	
			elif num==1:
				chamar_perfil_entrada(cpf)

		except Exception as e:
			return False



def chamar_perfil_entrada(cpf):

	try:
		colab = retorna_user(cpf)

		tela_perfil = Tk()
		tela_perfil.attributes('-fullscreen', True)
		tela_perfil["bg"] = "white"
		tela_perfil.title("Perfil do colaborador")
		tela_perfil.resizable(0, 0)

		maxwidth = 150
		maxheight = 200
		
		label_title = Label(tela_perfil, bg="white", text="Entrada liberada", fg= "orange", font=["Verdana", 30]).pack(pady=100)

		if colab.foto != None:
			pic = Image.open(io.BytesIO(colab.foto))
			pic.thumbnail((maxwidth, maxheight), resample=3)
			pic.save('temp.png')
			pic.close()

			pic = ImageTk.PhotoImage(file="temp.png")

			label_foto = Label(tela_perfil, width=150, height=150, image = pic, bg="orange")
			label_foto.image =  pic
			label_foto.place(x=400, y =300)
		else:
			label_foto = Label(tela_perfil, width=20, height=10, bg="orange").place(x=400, y =300)

		label_nome = Label(tela_perfil, bg="white", text="Nome: "+colab.nome,   font=["Verdana", 13]).place(x=600, y=300)
		label_lab = Label(tela_perfil, bg="white", text="Laboratório: "+colab.lab,     font=["Verdana", 13]).place(x=600, y=340)
		label_func = Label(tela_perfil, bg="white", text="Função: "+colab.funcao, font=["Verdana", 13]).place(x=600, y=380)
		bt_confirma = Button(tela_perfil, bg="white", text = "Confirmar", width = 15, command = partial(pre_tela_principal, tela_perfil)).place(x=600, y=420)
		os.remove("temp.png")

		
	except Exception as e:
		return False

def chamar_perfil_saida(cpf):

	try:
		colab = retorna_user(cpf)

		tela_perfil = Tk()
		tela_perfil.attributes('-fullscreen', True)
		tela_perfil["bg"] = "white"
		tela_perfil.title("Perfil do colaborador")
		#tela_perfil.overridedirect(1)

		maxwidth = 150
		maxheight = 200
		
		label_title = Label(tela_perfil, bg="white", text="Saída Validada", fg= "orange", font=["Verdana", 30]).pack(pady=100)

		if colab.foto != None:
			pic = Image.open(io.BytesIO(colab.foto))
			pic.thumbnail((maxwidth, maxheight), resample=3)
			pic.save('temp.png')
			pic.close()

			pic = ImageTk.PhotoImage(file="temp.png")

			label_foto = Label(tela_perfil, width=150, height=150, image = pic, bg="orange")
			label_foto.image =  pic
			label_foto.place(x=400, y =300)
		else:
			label_foto = Label(tela_perfil, width=20, height=10, bg="orange").place(x=400, y =300)

		label_nome = Label(tela_perfil, bg="white", text="Nome: "+colab.nome,   font=["Verdana", 13]).place(x=600, y=300)
		label_lab = Label(tela_perfil, bg="white", text="Laboratório: "+colab.lab,     font=["Verdana", 13]).place(x=600, y=340)
		label_func = Label(tela_perfil, bg="white", text="Função: "+colab.funcao, font=["Verdana", 13]).place(x=600, y=380)
		bt_confirma = Button(tela_perfil, bg="white", text = "Confirmar", width = 15, command = partial(pre_tela_principal, tela_perfil)).place(x=600, y=420)
		os.remove("temp.png")

		
	except Exception as e:
		return False
	

def cadastrar_digital(login, senha, tela_anterior, event=None):
	if (login.get() != "") and (senha.get() != ""):
		try:
			colab = retorna_user(login.get())

			if (colab.senha == senha.get()) and (colab.status == "Ativo") and  (colab.cpf not in retorna_lista_cadastrados()):
				cadastrar_digital_2(tela_anterior, login.get())
			elif(colab.cpf in retorna_lista_cadastrados()):
				pop_up("ERROR", "Digital já cadastrada")
			else:
				pop_up("ERROR", "Login ou Senha Inválida")

		except Exception as e:
			print(e)
			pop_up("ERROR", "Login ou Senha Inválida")

	else:
		pop_up("ERROR", "Login ou Senha Inválida")


def cadastrar_digital_2(tela_anterior, login):
	tela_anterior.destroy()

	tela_login = Tk()
	tela_login["bg"]="white"
	tela_login.attributes('-fullscreen', True) 
	tela_login.title("Sistema de Controle de Frequência") 
	
	#Logo
	imagem = PhotoImage(file="imagens/hub2.png")
	lb_image = Label(tela_login, image = imagem, bg="white")
	lb_image.image = imagem
	lb_image.pack(pady=110)
	
	bt_iniciar = Button(tela_login, text="Inserir Digital", width=15, command=partial(pegar_digital, tela_login, login), bg ="white")
	bt_iniciar.pack()
	bt_voltar = Button(tela_login, width=10, text="Voltar", bg="white", command=partial(pre_tela_principal, tela_login)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	lb = Label(tela_login, font=['TkDefaultFont', 10], text="*Aperte o botão \'Inserir Digital\'\nEm seguida, insira sua digital enquanto \no led verde estiver ligado\nRetire quando o led vermelho ligar\nInsira novamente quando o led verde ligar", bg="white").pack(side=TOP, pady=20)




def chamar_tela_login(tela_anterior):
	tela_anterior.destroy()
	tela_login = Tk()
	tela_login["bg"]="white"
	tela_login.attributes('-fullscreen', True) #dimensoes da janela --> Largura x Altura + DistanciaDaMargemEsquerda + DistanciaDaMargemSuperior
	tela_login.title("Sistema de Controle de Frequência") #título da janela

	#Logo
	imagem = PhotoImage(file="imagens/hub2.png")
	lb_image = Label(tela_login, image = imagem, bg="white")
	lb_image.image = imagem
	lb_image.pack(pady=110)
	
	lb_login = Label(tela_login, text="CPF:", bg="white").place(x=560, y=357)
	entrada_login = Entry(tela_login, width=40, bg="white")
	entrada_login.pack(pady=2)
	
	lb_senha = Label(tela_login, text="Senha:", bg="white").place(x=560, y=398)
	entrada_senha = Entry(tela_login, width=40, bg="white", show="*")
	entrada_senha.pack(pady=18)

	tela_login.bind('<Return>', lambda event: cadastrar_digital(entrada_login, entrada_senha,tela_login, event))

	bt_logar = Button(tela_login, width=10, bg="white", text="Login", command=partial(cadastrar_digital, entrada_login, entrada_senha, tela_login)).place(x=723, y=450)
	bt_voltar = Button(tela_login, width=10, text="Voltar", bg="white", command=partial(pre_tela_principal, tela_login)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)

def pre_tela_principal(tela_anterior):
	tela_anterior.destroy()
	chamar_tela_principal() 

def chamar_tela_principal():
	tela_login = Tk()
	tela_login["bg"]="white"
	tela_login.attributes('-fullscreen', True) #dimensoes da janela --> Largura x Altura + DistanciaDaMargemEsquerda + DistanciaDaMargemSuperior
	tela_login.title("Sistema de Controle de Frequência") #título da janela

	imagem = PhotoImage(file="imagens/hub2.png")
	lb_image = Label(tela_login, image = imagem, bg="white")
	lb_image.image = imagem
	lb_image.pack(pady=110)
	
	bt_iniciar = Button(tela_login, text="Inserir Digital", width=15, command=partial(validar_digital,tela_login), bg ="white")
	bt_iniciar.pack(pady=2)

	bt_cadastrar = Button(tela_login, text="Primeiro acesso", width=15, command=partial(chamar_tela_login, tela_login), bg ="white")
	bt_cadastrar.pack(pady=2)

	
	tela_login.mainloop()

def pop_up(title, label):
	pop_up = Tk()
	pop_up["bg"]="white"
	pop_up.geometry("280x60+450+330")
	pop_up.title(title) 
	pop_up.resizable(0,0)
	lb = Label (pop_up, text=label, bg="white").pack(pady=20)
	


if linha == b'1\r\n':
	chamar_tela_principal()
	conexao.close()
