from SCF_backend import *
import SCF_backend
from functools import partial
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk


class SCFapp(tk.Tk):
	def __init__(self, *args, **kwargs):
		self.user = Colaborador()
		tk.Tk.__init__(self, *args, **kwargs)
	
		self.container = tk.Frame(self)
		self.container.pack(side="top", fill="both", expand=True)

		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (TelaLogin, TelaInicialAdm, TelaCadastro, TelaInicialGestor, TelaCadastroColaborador, TelaCadastroLaboratorio, TelaConsulta, TelaConsulta2, TelaDadosColaborador, TelaDadosLaboratorio, TelaConsultaHistorico, TelaHistorico):
			frame = F(self.container,self)
			self.frames[F] = frame
			frame['bg'] = "white"
			frame.grid(row=0,column=0,sticky="nsew")
			frame.grid_propagate(0)

		self.mostrar_frame(TelaLogin)

	def mostrar_frame(self, cont, lista_tela_historico = None):
		try:
			if cont != TelaHistorico:
				frame = self.frames[cont]
				self.geometry(frame.tamanho)
				frame.update()
				self.title(frame.titulo)
				frame.focus_set()
				frame.tkraise()
				
			else:
				frame = cont(self.container, self)
				self.frames[cont] = frame
				frame['bg'] = "white"
				frame.grid(row=0,column=0,sticky="nsew")
				frame.grid_propagate(0)
				frame.setTuplas(lista_tela_historico[0])
				frame.setLab(lista_tela_historico[1])
				frame.setAno(lista_tela_historico[2])
				frame.setMes(lista_tela_historico[3])
				frame.setTipo(lista_tela_historico[4])
				frame.update()

				self.geometry(frame.tamanho)
				self.title(frame.titulo)
				frame.focus_set()
				frame.tkraise()

		except Exception as e:
			pass

	def setUser(self, user):
		self.user = user

	def deslogar(self):
		self.user = None
		self.mostrar_frame(TelaLogin)

class TelaLogin(tk.Frame):
	def __init__(self, parent, controller):
		self.tamanho = "500x350"
		self.titulo = "Sistema de Controle de Frequência"
		self.controller = controller

		tk.Frame.__init__(self, parent, width=500, height=350)
		controller.resizable(0,0)
		
		#Logo
		imagem = tk.PhotoImage(file=r"\\LSEHOST\Documents\SCF\imagens\hub.png")
		lb_image = tk.Label(self, image = imagem, bg="white")
		lb_image.image = imagem
		lb_image.pack(pady=30)

		lb_login = tk.Label(self, text="Login:", bg="white").place(x=120, y=150)
		self.login_string = StringVar()
		entrada_login = tk.Entry(self, width=40, bg="white", textvariable=self.login_string)
		entrada_login.place(x=120, y=170)
		
		lb_senha = tk.Label(self, text="Senha:", bg="white").place(x=120, y=200)
		self.senha_string = StringVar()
		entrada_senha = tk.Entry(self, width=40, bg="white", show="*", textvariable = self.senha_string)
		entrada_senha.bind('<Return>', lambda event:self.login(entrada_login, entrada_senha, event))
		entrada_senha.place(x=120, y=220)


		self.bind('<Return>', lambda event:self.login(entrada_login, entrada_senha, event))


		bt_logar = tk.Button(self, width=10, bg="white", text="Login", command= lambda:self.login(entrada_login, entrada_senha)).place(x=285, y=250)

	def login(self, entrada_login, entrada_senha, event=None):
		user = validar_login(entrada_login, entrada_senha)
		if user != None:
			self.controller.setUser(user)

			if self.controller.user.funcao in ['ADM', 'Coordenador Geral']:
				self.controller.mostrar_frame(TelaInicialAdm)
			else:
				self.controller.mostrar_frame(TelaInicialGestor)

	def update(self):
		self.login_string.set("")
		self.senha_string.set("")

class TelaInicialAdm(tk.Frame):
	def __init__(self, parent, controller):
		self.tamanho = "500x350"
		self.titulo = "HUB - Tecnologia e Inovação"
		tk.Frame.__init__(self, parent, width=500, height=350)

		lb_inicial = Label (self, text="Sistema de Controle de Frequência", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)
		bt_cadastrar = Button (self, width=20, text="Cadastrar", command = lambda:controller.mostrar_frame(TelaCadastro), bg="white").pack(pady=3)
		bt_consultar = Button (self, width=20, text="Consultar", command = lambda:controller.mostrar_frame(TelaConsulta), bg="white").pack(pady=3)

		bt_hist = Button (self, width=20, text="Histórico", bg="white", command = lambda:controller.mostrar_frame(TelaConsultaHistorico)).pack(pady=3)
		
		bt_sair = Button (self, width=10, text="Sair", bg="white", command = lambda:controller.deslogar()).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)

	def update(self):
		pass

class TelaInicialGestor(tk.Frame):
	def __init__(self, parent, controller):
		self.tamanho = "500x350"
		self.titulo = "HUB - Tecnologia e Inovação"
		tk.Frame.__init__(self, parent, width=500, height=350)

		lb_inicial = Label (self, text="Sistema de Controle de Frequência", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

		bt_cadastrar = Button (self, width=20, text="Cadastrar colaborador", command = lambda:controller.mostrar_frame(TelaCadastroColaborador), bg="white").pack(pady=3)
		bt_consultar = Button (self, width=20, text="Consultar", command = lambda:controller.mostrar_frame(TelaConsulta2), bg="white").pack(pady=3)

		bt_hist = Button (self, width=20, text="Histórico", bg="white", command = lambda:controller.mostrar_frame(TelaConsultaHistorico)).pack(pady=3)
		
		bt_sair = Button (self, width=10, text="Sair", bg="white", command= lambda:controller.deslogar()).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)

	def update(self):
		pass


class TelaCadastro(tk.Frame):

	def __init__(self, parent, controller):
		self.tamanho = "500x350"
		self.titulo = "Cadastro"
		tk.Frame.__init__(self, parent, width=500, height=350)

		controller.resizable(0,0)

		lb = Label (self, text="O que você deseja cadastrar?", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

		bt_cadastrar_colaborador = Button (self, width=20, text="Colaborador", bg="white", command=lambda:controller.mostrar_frame(TelaCadastroColaborador)).pack(pady=3)
		bt_cadastrar_laboratorio = Button (self, width=20, text="Laboratório", bg="white", command=lambda:controller.mostrar_frame(TelaCadastroLaboratorio)).pack(pady=3)
			
		bt_voltar = Button (self, width=10, text="Voltar", bg="white", command= lambda:controller.mostrar_frame(TelaInicialAdm)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)

	def update(self):
		pass
		
class TelaCadastroColaborador(tk.Frame):

	def __init__(self, parent, controller):
		self.tamanho = "500x680"
		self.titulo = "Cadastrar Colaborador"
		self.controller = controller
		tk.Frame.__init__(self, parent, width=500, height=350)
		controller.resizable(0,0)

		
		lb = Label(self, text="Informe os dados do colaborador", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=30)
		
		dis_x = 110
		dis_y_inicial = 70
		self.nome = StringVar()
		self.ch = StringVar()
		self.cpf = StringVar()
		self.senha = StringVar()
		self.confirma_senha = StringVar()
		self.dt_format_nasc = StringVar()
		self.dt_format_entrada = StringVar()
		self.line_path = StringVar()
		#Nome:

		lb_nome = Label(self, text="Nome:", bg="white")
		lb_nome.place(x=dis_x, y=dis_y_inicial)
		entrada_nome = Entry(self, width=40, bg="white", textvariable = self.nome)
		entrada_nome.place(x=dis_x, y=dis_y_inicial+20)
		#Data de Nascimento
		lb_dt_nasc = Label(self, text="Data de Nascimento:", bg="white")
		lb_dt_nasc.place(x=dis_x, y=dis_y_inicial+50)

		placeholder = lambda texto, event: texto.set("")

		entrada_dt_nasc = Entry(self, width=40, bg="white", textvariable = self.dt_format_nasc)
		entrada_dt_nasc.bind('<Button-1>', lambda event:placeholder(self.dt_format_nasc,event))
		entrada_dt_nasc.place(x=dis_x, y=dis_y_inicial+70)

		#Laboratório
		lb_lab = Label(self, text="Laboratório:", bg="white")
		lb_lab.place(x=dis_x, y=dis_y_inicial+100)

		self.entrada_lab = ttk.Combobox(self, width=37, state="readonly")
		self.entrada_lab.place(x=dis_x, y=dis_y_inicial+120)	
		#Função
		lb_func = Label(self, text="Função:", bg="white")
		lb_func.place(x=dis_x, y=dis_y_inicial+150)

		self.entrada_func = ttk.Combobox(self, width=37, state="readonly")
		self.entrada_func.place(x=dis_x, y=dis_y_inicial+170)	
			
		#Carga Horária
		lb_CH = Label(self, text="Carga Horária semanal:", bg="white")
		lb_CH.place(x=dis_x, y=dis_y_inicial+200)
		entrada_CH = Entry(self, width=40, bg="white", textvariable = self.ch)
		entrada_CH.place(x=dis_x, y=dis_y_inicial+220)	
		#Data de Ingresso
		lb_dt_ing = Label(self, text="Data de Ingresso:", bg="white")
		lb_dt_ing.place(x=dis_x, y=dis_y_inicial+250)
		entrada_dt_ing = Entry(self, width=40, bg="white", textvariable=self.dt_format_entrada)
		entrada_dt_ing.bind('<Button-1>', lambda event:placeholder(self.dt_format_entrada,event))
		entrada_dt_ing.place(x=dis_x, y=dis_y_inicial+270)
		#Status
		lb_status = Label(self, text="Status:", bg="white")
		lb_status.place(x=dis_x, y=dis_y_inicial+300)
		lista_status = ['Ativo', 'Afastado']
		entrada_status = ttk.Combobox(self, width=37, state="readonly")
		entrada_status.place(x=dis_x, y=dis_y_inicial+320)	
		entrada_status['values'] = lista_status
		entrada_status.current(0)
		#CPF
		lb_cpf = Label(self, text="CPF:", bg="white")
		lb_cpf.place(x=dis_x, y=dis_y_inicial+350)
		entrada_cpf = Entry(self, width=40, bg="white", textvariable = self.cpf)
		entrada_cpf.place(x=dis_x, y=dis_y_inicial+370)

		#Upload Foto
		lb_foto = Label(self, text="Insira a foto do colaborador", bg="white").place(x=dis_x, y=dis_y_inicial+400)
		entrada_foto = Entry(self, width=40, bg="white", textvariable= self.line_path)
		entrada_foto.place(x=dis_x, y=dis_y_inicial+420)

		bt_browser = Button(self, text="Browser", bg="white", font=['TkDefaultFont', 7], command=lambda:ImageMethods.get_path(self.line_path))
		bt_browser.place(x=dis_x+250, y=dis_y_inicial+420)
		label_info = Label(self, text="*Campo não obrigatório!", font=['TkDefaultFont', 7], bg="white")
		label_info.place(x=dis_x, y=dis_y_inicial+440)

		#Senha
		lb_senha = Label(self, text="Senha:", bg="white").place(x=dis_x, y=dis_y_inicial+460)
		entrada_senha = Entry(self, width=40, bg="white", show="*", textvariable = self.senha)
		entrada_senha.place(x=dis_x, y=dis_y_inicial+480)
		#Confirme sua Senha
		lb_confirma_senha = Label(self, text="Confirme sua Senha:", bg="white").place(x=dis_x, y=dis_y_inicial+510)
		entrada_confirma_senha = Entry(self, width=40, bg="white", show="*", textvariable = self.confirma_senha)
		entrada_confirma_senha.place(x=dis_x, y=dis_y_inicial+530)

		self.voltar = lambda: False

		bt_voltar = Button(self, width=10, text="Voltar", bg="white", command=lambda:self.voltar()).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)

		entrada_confirma_senha.bind('<Return>', lambda event: self.cadastrar(entrada_nome, entrada_dt_nasc, self.entrada_lab, self.entrada_func, 
		entrada_CH, entrada_dt_ing, entrada_status, entrada_cpf, entrada_senha, entrada_confirma_senha, entrada_foto, event))

		self.bind('<Return>', lambda event: self.cadastrar(entrada_nome, entrada_dt_nasc, self.entrada_lab, self.entrada_func, 
		entrada_CH, entrada_dt_ing, entrada_status, entrada_cpf, entrada_senha, entrada_confirma_senha, entrada_foto, event))

		bt_ok = Button(self, width=10, text="Cadastrar", bg="white", command=partial(self.cadastrar, entrada_nome, entrada_dt_nasc,
																					self.entrada_lab, self.entrada_func, entrada_CH, entrada_dt_ing, entrada_status, entrada_cpf,
																					entrada_senha, entrada_confirma_senha, entrada_foto)).place(x=275, y=625)


	def update(self):
		if self.controller.user.funcao in ['ADM', 'Coordenador Geral']:
			lista_lab = retorna_lista_lab()
			lista_lab.insert(0, "*Selecione o laboratório*")
			self.entrada_lab['values'] = lista_lab

			self.entrada_func['values'] = ['Pesquisador', 'Gestor', 'Coordenador', 'ADM', 'Coordenador Geral']
			self.entrada_func.current(0)	
			self.entrada_lab.current(0)	
			self.voltar = lambda: self.controller.mostrar_frame(TelaCadastro)
			
		else:
			self.entrada_func['values'] = ['Pesquisador', 'Gestor', 'Coordenador']
			self.entrada_lab['values'] = [self.controller.user.lab]
			self.entrada_func.current(0)	
			self.entrada_lab.current(0)
			self.voltar = lambda: self.controller.mostrar_frame(TelaInicialGestor)

		self.nome.set("")
		self.ch.set("")
		self.cpf.set("")
		self.senha.set("")
		self.confirma_senha.set("")
		self.dt_format_nasc.set("DD/MM/AAAA")
		self.dt_format_entrada.set("DD/MM/AAAA")
		self.line_path.set("")

	def cadastrar(self, entrada_nome, entrada_dt_nasc, entrada_lab, entrada_func, entrada_CH, entrada_dt_ing, entrada_status, entrada_cpf, entrada_senha, entrada_confirma_senha, entrada_foto, event=None):
		cadastrado = cadastrar_colaborador(entrada_nome, entrada_dt_nasc, entrada_lab, 
					entrada_func, entrada_CH, entrada_dt_ing, entrada_status, entrada_cpf,
					entrada_senha, entrada_confirma_senha, entrada_foto)
		if cadastrado:
			self.controller.mostrar_frame(TelaCadastro)
			pop_up("SUCCESSFUL", "Cadastro Realizado com Sucesso")
		else:
			pass

class TelaCadastroLaboratorio(tk.Frame):

	def __init__(self, parent, controller):
		self.tamanho = "500x350"
		self.titulo = "Cadastrar Laboratório"
		self.controller = controller
		tk.Frame.__init__(self, parent, width=500, height=350)
		controller.resizable(0,0)

		self.nome = StringVar()
		self.sigla = StringVar()
		self.line_path = StringVar()

		lb = Label(self, text="Informe os dados do laboratório", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=20)
		
		#Nome:
		lb_nome = Label(self, text="Nome:", bg="white").place(x=110, y=80)
		entrada_nome = Entry(self, width=40, bg="white", textvariable=self.nome)
		entrada_nome.place(x=110, y=100)
		#Sigla:
		lb_sigla = Label(self, text="Sigla:", bg="white").place(x=110, y=130)
		entrada_sigla = Entry(self, width=40, bg="white", textvariable=self.sigla)
		entrada_sigla.place(x=110, y=150)

		#Upload logo
			#Label e entry
		lb_logo = Label(self, text='Insira o logo do laboratório', bg='white').place(x=110, y=180)
		
		entrada_logo = Entry(self, width=40, bg='white', textvariable = self.line_path)
		entrada_logo.place(x=110, y=200)
			#button
		bt_browser = Button(self, text='Browser', font=['TkDefaultFont', 7], bg='white', command = lambda:ImageMethods.get_path(self.line_path))
		bt_browser.place(x=360, y=200)

		label_info = Label(self, text="*Campo não obrigatório!", font=['TkDefaultFont', 7], bg="white")
		label_info.place(x=110, y=220)

		self.bind('<Return>', lambda event:self.cadastrar(entrada_nome, entrada_sigla, entrada_logo, event))
		entrada_sigla.bind('<Return>', lambda event:self.cadastrar(entrada_nome, entrada_sigla, entrada_logo, event))


		bt_voltar = Button (self, width=10, text="Voltar", bg="white", command=lambda:controller.mostrar_frame(TelaCadastro)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
		bt_ok = Button(self, width=10, text="Cadastrar", bg="white", command=lambda:self.cadastrar(entrada_nome, entrada_sigla, entrada_logo)).place(x=275, y=250)

	def update(self):
		self.nome.set("")
		self.sigla.set("")
		self.line_path.set("")

	def cadastrar(self, entrada_nome, entrada_sigla, entrada_logo, event=None):
		cadastrado = cadastrar_laboratorio(entrada_nome, entrada_sigla, entrada_logo)
		if cadastrado:
			inter.pop_up("SUCCESSFUL", "Cadastro Realizado com Sucesso")
		else:
			pass

class TelaConsulta(tk.Frame):

	def __init__(self, parent, controller):
		self.tamanho = "500x350"
		self.titulo = "Consulta"
		self.controller = controller
		tk.Frame.__init__(self, parent, width=500, height=350)
		controller.resizable(0,0) 

		lb = Label (self, text="Consultar", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

		#lab
		lb_lab = Label(self, text="Laboratório:", bg="white")
		lb_lab.place(x=110, y=130)
		
		self.entrada_lab = ttk.Combobox(self, width=37, state="readonly")
		self.entrada_lab.place(x=110, y=150)	

		self.bind('<Return>',lambda event:self.validar(self.entrada_lab, event))
		self.entrada_lab.bind('<Return>',lambda event:self.validar(self.entrada_lab, event))

		bt_ok = Button(self, width=10, text="Avançar", bg="white", command=lambda:self.validar(self.entrada_lab)).place(x=275, y=177)
		bt_voltar = Button (self, width=10, text="Voltar", bg="white", command=lambda:controller.mostrar_frame(TelaInicialAdm)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)

	def update(self):
		lista_lab = retorna_lista_lab()
		lista_lab.insert(0,"*Selecione o laboratório*")
		self.entrada_lab['values'] = lista_lab + ['Não Ativos']
		self.entrada_lab.current(0)

	def validar(self, entrada_lab, event=None):
		if  entrada_lab.get() == 'Não Ativos':
			self.controller.frames[TelaConsulta2].setLab(entrada_lab.get())
			self.controller.mostrar_frame(TelaConsulta2)
		else:
			valido = validar_consulta(entrada_lab)
			if valido:
				self.controller.frames[TelaConsulta2].setLab(entrada_lab.get())
				self.controller.mostrar_frame(TelaConsulta2)
			else:
				pass

class TelaConsulta2(tk.Frame):

	def __init__(self, parent, controller):
		self.lab = ""
		self.tamanho = "500x350"
		self.controller = controller
		self.titulo = "Consultar > Laboratório: "+ self.lab
		tk.Frame.__init__(self, parent, width=500, height=350)
		controller.resizable(0,0)

		lb = Label (self, text="Consultar", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

		#colaborador
		lb_colab = Label(self, text="Colaborador:", bg="white")
		lb_colab.place(x=110, y=130)	

		self.entrada_colab = ttk.Combobox(self, width=37, state="readonly")
		self.entrada_colab.place(x=110, y=150)

		self.voltar = lambda:False	

		self.bind('<Return>', lambda event:self.validar(self.entrada_colab, event))	

		bt_ok = Button(self, width=10, text="Avançar", bg="white", command = lambda:self.validar(self.entrada_colab)).place(x=275, y=177)
		
		bt_consulta_lab = Button(self, width=20, text="Consultar laboratório", bg="white", command=lambda:self.consultar_lab()).pack(side=RIGHT, anchor = SE, pady=4, padx=4)

		
		bt_voltar = Button (self, width=10, text="Voltar", bg="white", command= lambda:self.voltar()).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
		
	def update(self):
		if self.controller.user.funcao in ['ADM', 'Coordenador Geral']:
			self.titulo = "Consultar > Laboratório: "+ self.lab
			lista_colab = retorna_lista_colab(self.lab)
			self.voltar = lambda:self.controller.mostrar_frame(TelaConsulta)
		else:
			self.lab = self.controller.user.lab
			lista_colab = retorna_lista_colab(self.lab)
			self.voltar = lambda:self.controller.mostrar_frame(TelaInicialGestor)
		
		lista_colab.insert(0,"*Selecione o colaborador*")
		self.entrada_colab['values'] = lista_colab
		self.entrada_colab.current(0)

	def setLab(self, lab):
		self.lab = lab

	def validar(self, entrada_colab, event=None):
		if self.lab == 'Não Ativos':
			
			colab = retorna_colab(entrada_colab, self.lab)
			self.controller.frames[TelaDadosColaborador].setColab(colab)
			self.controller.mostrar_frame(TelaDadosColaborador)
			
		else:	
			valido = validar_consulta_2(entrada_colab, self.lab)		
			if valido:
				colab = retorna_colab(entrada_colab, self.lab)
				self.controller.frames[TelaDadosColaborador].setColab(colab)
				self.controller.mostrar_frame(TelaDadosColaborador)
			else:
				pass

	def consultar_lab(self):
		if self.lab == 'Não Ativos':
			pop_up('ERROR', 'Opção Inválida')
		else:
			dados_lab = retorna_dados_lab(self.lab)
			self.controller.frames[TelaDadosLaboratorio].setLab(dados_lab)
			self.controller.mostrar_frame(TelaDadosLaboratorio)

class TelaDadosColaborador(tk.Frame):

	def __init__(self, parent, controller):
		self.tamanho = "500x680"
		self.titulo = "Dados Cadastrais Colaborador"
		self.controller = controller
		self.colab = Colaborador()
		tk.Frame.__init__(self, parent, width=500, height=680) 
		controller.resizable(0,0)

		self.nome = StringVar()
		self.ch = StringVar()
		self.dt_nac = StringVar()
		self.dt_ent = StringVar()
		self.line_path = StringVar()
		self.senha = StringVar()
		self.confirmar_senha = StringVar()

		lb = Label(self, text="Dados Cadastrais", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=30)
		
		dis_x = 110
		dis_y_inicial = 70

		#Nome:
		lb_nome = Label(self, text="Nome:", bg="white")
		lb_nome.place(x=dis_x, y=dis_y_inicial)
		entrada_nome = Entry(self, width=40, bg="white", textvariable=self.nome)
		entrada_nome.place(x=dis_x, y=dis_y_inicial+20)

		#Data de Nascimento
		lb_dt_nasc = Label(self, text="Data de Nascimento:", bg="white")
		lb_dt_nasc.place(x=dis_x, y=dis_y_inicial+50)
		entrada_dt_nasc = Entry(self, width=40, bg="white", textvariable=self.dt_nac)
		entrada_dt_nasc.place(x=dis_x, y=dis_y_inicial+70)

		#Laboratório
		lb_lab = Label(self, text="Laboratório:", bg="white")
		lb_lab.place(x=dis_x, y=dis_y_inicial+100)

		self.entrada_lab = ttk.Combobox(self, width=37, state="readonly")
		self.entrada_lab.place(x=dis_x, y=dis_y_inicial+120)	
		
		#Função
		lb_func = Label(self, text="Função:", bg="white")
		lb_func.place(x=dis_x, y=dis_y_inicial+150)

		
		self.entrada_func = ttk.Combobox(self, width=37, state="readonly")
		self.entrada_func.place(x=dis_x, y=dis_y_inicial+170)
			
		#Carga Horária
		lb_CH = Label(self, text="Carga Horária semanal:", bg="white")
		lb_CH.place(x=dis_x, y=dis_y_inicial+200)
		entrada_CH = Entry(self, width=40, bg="white", textvariable=self.ch)
		entrada_CH.place(x=dis_x, y=dis_y_inicial+220)	

		#Data de Ingresso
		lb_dt_ing = Label(self, text="Data de Ingresso:", bg="white")
		lb_dt_ing.place(x=dis_x, y=dis_y_inicial+250)
		entrada_dt_ing = Entry(self, width=40, bg="white", textvariable=self.dt_ent)
		entrada_dt_ing.place(x=dis_x, y=dis_y_inicial+270)

		#Status
		lb_status = Label(self, text="Status:", bg="white")
		lb_status.place(x=dis_x, y=dis_y_inicial+300)
		
		self.entrada_status = ttk.Combobox(self, width=37, state="readonly")
		self.entrada_status.place(x=dis_x, y=dis_y_inicial+320)	

		#Upload Foto	
		lb_foto = Label(self, text="Insira a foto do colaborador", bg="white").place(x=dis_x, y=dis_y_inicial+350)
		entrada_foto = Entry(self, width=40, bg="white", textvariable= self.line_path)
		entrada_foto.place(x=dis_x, y=dis_y_inicial+370)

		bt_browser = Button(self, text="Browser", bg="white", font=['TkDefaultFont', 7], command=lambda:ImageMethods.get_path(self.line_path))
		bt_browser.place(x=dis_x+250, y=dis_y_inicial+370)
		label_info = Label(self, text="*Campo não obrigatório!", font=['TkDefaultFont', 7], bg="white")
		label_info.place(x=dis_x, y=dis_y_inicial+390)

		lb_senha = Label(self, text="Senha:", bg="white").place(x=dis_x, y=dis_y_inicial+410)
		entrada_senha = Entry(self, width=40, bg="white", show="*", textvariable=self.senha)
		entrada_senha.place(x=dis_x, y=dis_y_inicial+430)

		#Confirme sua Senha
		lb_confirma_senha = Label(self, text="Confirme sua Senha:", bg="white").place(x=dis_x, y=dis_y_inicial+460)
		entrada_confirma_senha = Entry(self, width=40, bg="white", show="*", textvariable=self.confirmar_senha)
		entrada_confirma_senha.place(x=dis_x, y=dis_y_inicial+480)


		self.bind('<Return>', lambda event:self.atualizar_colab(entrada_nome, entrada_dt_nasc, self.entrada_lab, self.entrada_func, entrada_CH, entrada_dt_ing, self.entrada_status,
		entrada_senha, entrada_confirma_senha, entrada_foto, self.colab.cpf, event))

		bt_ok = Button(self, width=10, text="Atualizar", bg="white", command=lambda:self.atualizar_colab(entrada_nome, entrada_dt_nasc, self.entrada_lab, self.entrada_func, entrada_CH, 
		entrada_dt_ing, self.entrada_status, entrada_senha, entrada_confirma_senha, entrada_foto, self.colab.cpf)).place(x=275, y=600)

		bt_remover = Button(self, width=20, text="Excluir colaborador", bg="white", command=lambda:self.remover_colab()).pack(side=RIGHT, anchor = SE, pady=4, padx=4)
		bt_voltar = Button(self, width=10, text="Voltar", bg="white", command=lambda:controller.mostrar_frame(TelaConsulta2)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)

	def update(self):
		if self.controller.user.funcao in ['ADM', 'Coordenador Geral']:
			lista_lab = retorna_lista_lab()
			self.entrada_lab['values'] = lista_lab
			self.entrada_lab.current(lista_lab.index(self.colab.lab))

			lista_func = ['Pesquisador', 'Gestor', 'Coordenador', 'ADM', 'Coordenador Geral']
			self.entrada_func['values'] = lista_func
			self.entrada_func.current(lista_func.index(self.colab.funcao))

		else:
			lista_lab = self.colab.lab
			self.entrada_lab['values'] = lista_lab
			self.entrada_lab.current(lista_lab.index(self.colab.lab))

			lista_func = ['Pesquisador', 'Gestor', 'Coordenador']
			self.entrada_func['values'] = lista_func
			self.entrada_func.current(lista_func.index(self.colab.funcao))

		lista_status = ['Ativo', 'Afastado']
		if self.colab.status == 'Não Ativo':
			lista_status.append('Não Ativo')
		self.entrada_status['values'] = lista_status
		self.nome.set(self.colab.nome)
		self.ch.set(self.colab.ch)
		self.line_path.set("")
		self.dt_nac.set(self.colab.dtNasc)
		self.dt_ent.set(self.colab.dtIngresso)
		self.senha.set(self.colab.senha)
		self.confirmar_senha.set(self.colab.senha)
		self.entrada_status.current(lista_status.index(self.colab.status))

	def setColab(self, colab):
		self.colab = colab

	def remover_colab(self):
		if self.colab.cpf != self.controller.user.cpf:
			excluiu = excluir_colaborador(self.colab.cpf, self.colab.lab)
			if excluiu:
				self.controller.mostrar_frame(TelaConsulta2)
				pop_up("SUCCESSFUL", "Usuário removido com sucessso.")
			else:
				pass
		else:
			inter.pop_up("ERROR", "Não é permitido excluir o próprio usuário.")

	def atualizar_colab(self, entrada_nome, entrada_dt_nasc,entrada_lab, entrada_func, entrada_CH, entrada_dt_ing, entrada_status,
		entrada_senha, entrada_confirma_senha, entrada_foto, cpf, event=None):
		atualizou = atualizar_cadastro_colaborador(entrada_nome, entrada_dt_nasc,entrada_lab, entrada_func, entrada_CH, entrada_dt_ing, entrada_status,
		entrada_senha, entrada_confirma_senha, entrada_foto, cpf)

		if atualizou:
			pop_up("SUCCESSFUL", "Cadastro Atualizado com Sucesso")
			self.controller.mostrar_frame(TelaConsulta2)
		else:
			pass

class TelaDadosLaboratorio(tk.Frame):

	def __init__(self, parent, controller):
		self.tamanho = "500x350"
		self.lab = None
		self.controller = controller
		tk.Frame.__init__(self, parent, width=500, height=350)
		self.controller.resizable(0,0)

		self.nome = StringVar()
		self.sigla = StringVar()
		self.line_path = StringVar()

		lb = Label(self, text="Dados do laboratório", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=20)
		
		#Nome:
		lb_nome = Label(self, text="Nome:", bg="white").place(x=110, y=80)
		entrada_nome = Entry(self, width=40, bg="white", state='readonly', textvariable = self.nome)
		entrada_nome.place(x=110, y=100)

		#Sigla:
		lb_sigla = Label(self, text="Sigla:", bg="white").place(x=110, y=130)
		entrada_sigla = Entry(self, width=40, bg="white", state='readonly', textvariable=self.sigla)
		entrada_sigla.place(x=110, y=150)

		#Upload logo
			#Label e entry
		lb_logo = Label(self, text='Insira o logo do laboratório', bg='white').place(x=110, y=180)
		
		entrada_logo = Entry(self, width=40, bg='white', textvariable = self.line_path)
		entrada_logo.place(x=110, y=200)
			#button
		bt_browser = Button(self, text='Browser', font=['TkDefaultFont', 7], bg='white', command = lambda:ImageMethods.get_path(self.line_path))
		bt_browser.place(x=360, y=200)

		label_info = Label(self, text="*Campo não obrigatório!", font=['TkDefaultFont', 7], bg="white")
		label_info.place(x=110, y=220)

		self.bind('<Return>', lambda event:self.atualizar_lab(entrada_nome, entrada_sigla, entrada_logo, event))

		bt_voltar = Button (self, width=10, text="Voltar", bg="white", command=lambda:controller.mostrar_frame(TelaConsulta2)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
		bt_remover = Button(self, width=20, text="Excluir laboratório", bg="white", command=lambda:self.remover_lab()).place(x = 345, y= 320)
		bt_ok = Button(self, width=10, text="Atualizar", bg="white", command=lambda:self.atualizar_lab(entrada_nome, entrada_sigla, entrada_logo)).place(x=275, y=240)

	def update(self):
		self.titulo = "Dados laboratório: " + self.lab[0]
		self.nome.set(self.lab[0])
		self.sigla.set(self.lab[1])
		self.line_path.set("")

	def setLab(self, lab):
		self.lab=lab

	def remover_lab(self):
		excluido = excluir_lab(self.lab[0], self.lab[1])
		if excluido:
			self.controller.mostrar_frame(TelaConsulta)
			inter.pop_up("Sucesso", "Laboratório excluido com sucesso")
		else:
			pass

	def atualizar_lab(self, entrada_nome, entrada_sigla, entrada_logo, event=None):
		atualizado = atualizar_cadastro_laboratorio(entrada_nome, entrada_sigla, entrada_logo)
		if atualizado:
			self.controller.mostrar_frame(TelaConsulta2)
		else:
			pass

class TelaConsultaHistorico(tk.Frame):

	def __init__(self, parent, controller):
		self.tamanho = "500x350"
		self.controller = controller
		self.titulo = "Consultar Histórico"
		tk.Frame.__init__(self, parent, width=500, height=350)
		self.controller.resizable(0,0)

		lb = Label (self, text="Consultar Histórico", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

		#lab
		lb_lab = Label(self, text="Laboratório:", bg="white").place(x=110, y=100)
		lb_mes = Label(self, text="Mês:", bg="white").place(x=110,y=145)
		lb_ano = Label(self, text="Ano:", bg="white").place(x=250,y=145)

		lista_mes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
		lista_ano = ["2018","2019","2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"]

		self.entrada_lab = ttk.Combobox(self, width=37, state="readonly")
		self.entrada_lab.place(x=110, y=120)	
		
		entrada_mes = ttk.Combobox(self, width=12, state="readonly")
		entrada_mes.place(x=110, y=165)	
		entrada_mes['values'] = lista_mes
		entrada_mes.current(0)

		entrada_ano = ttk.Combobox(self, width=5, state="readonly")
		entrada_ano.place(x=250, y=165)	
		entrada_ano['values'] = lista_ano
		entrada_ano.current(0)

		self.voltar = lambda:False

		self.bind('<Return>', lambda event: self.historico(lab=entrada_lab, mes=entrada_mes, ano=entrada_ano, tipo='r', event=event))

		bt_hist_resumido = Button(self, width=10, text="Resumido", bg="white", command=lambda:self.historico(self.entrada_lab, entrada_mes, entrada_ano,'r')).place(x=180, y=200)
		bt_hist_detalhado = Button(self, width=10, text="Detalhado", bg="white", command=lambda:self.historico(self.entrada_lab, entrada_mes, entrada_ano,'d')).place(x=275, y=200)
		bt_voltar = Button (self, width=10, text="Voltar", bg="white", command=lambda:self.voltar()).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)

	def update(self):
		if self.controller.user.funcao in ['ADM', 'Coordenador Geral']:
			self.voltar = lambda:self.controller.mostrar_frame(TelaInicialAdm)
		else:
			self.voltar = lambda:self.controller.mostrar_frame(TelaInicialGestor)
		lista_lab = retorna_lista_lab() + ['Não Ativos']
		lista_lab.insert(0,"*Selecione o laboratório*")

		self.entrada_lab['values'] = lista_lab
		self.entrada_lab.current(0)

	def historico(self, lab, mes, ano, tipo, event=None):
		lista_tuplas = validar_chamada_historico(lab, mes, ano, tipo)
		if lista_tuplas:
			tupla_tela_hist = (lista_tuplas, lab.get(), ano.get(),mes.get(), tipo)
			self.controller.mostrar_frame(TelaHistorico, tupla_tela_hist)
		else:
			pop_up("Atenção", "Não há frequências na data selecionada.")
			pass


class TelaHistorico(tk.Frame):

	def __init__(self, parent, controller):
		self.tamanho = "550x600"

		self.lab = ""
		self.mes = ""
		self.ano = ""
		self.tipo = ''
		self.tuplas = ()
		self.header = []
		self.controller = controller
		tk.Frame.__init__(self, parent, width=500, height=350)
		self.controller.resizable(0,0)

		lb = Label (self, text="Histórico", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=20)
		bt_voltar = Button(self, text="Voltar", bg="white", command = lambda:self.voltar()).pack(side=TOP, anchor=NW, pady=4, padx=4)


	def update(self):
		self.titulo = "Histórico - "+self.lab + " - "+ self.mes +" - " + self.ano

		if self.tipo == 'r':
			self.header = ['Nome', 'Horas Acumuladas']
		else:
			self.header = ['Nome', 'Entrada', 'Saida']

		self = McListBox(self, self.header, self.tuplas)

	def voltar(self):
		self.controller.frames[TelaHistorico].destroy()
		self.controller.mostrar_frame(TelaConsultaHistorico)
		

	def setTuplas(self, tuplas):
		self.tuplas = tuplas

	def setMes(self, mes):
		self.mes = mes	

	def setAno(self, ano):
		self.ano = ano

	def setLab(self, lab):
		self.lab = lab

	def setTipo(self, tipo):
		self.tipo = tipo

def pop_up(title, label):
	pop_up = Tk()
	pop_up["bg"]="white"
	pop_up.geometry("280x60+450+330")
	pop_up.title(title) 
	pop_up.resizable(0,0)
	lb = Label (pop_up, text=label, bg="white").pack(pady=20)
	pop_up.focus_force()
	pop_up.bind('<Return>', lambda event:pop_up.destroy())
	pop_up.mainloop()
