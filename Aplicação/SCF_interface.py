from SCF_backend import *
import SCF_backend
from functools import partial
import tkinter.font as tkFont
import tkinter.ttk as ttk


def chamar_tela_cadastro(tela_anterior):
	tela_cadastro = Tk()
	tela_cadastro["bg"] = "white"
	tela_cadastro.geometry("500x300+300+200")
	tela_cadastro.title("Cadastro") 
	tela_cadastro.resizable(0,0)

	lb = Label (tela_cadastro, text="O que você deseja cadastrar?", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

	bt_cadastrar_colaborador = Button (tela_cadastro, width=20, text="Colaborador", bg="white", command=partial(chamar_tela_cadastro_colaborador, tela_cadastro)).pack(pady=3)
	bt_cadastrar_laboratorio = Button (tela_cadastro, width=20, text="Laboratório", bg="white", command=partial(chamar_tela_cadastro_laboratorio,tela_cadastro)).pack(pady=3)
		
	bt_voltar = Button (tela_cadastro, width=10, text="Voltar", bg="white", command=partial(chamar_tela_inicial, tela_cadastro)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	tela_anterior.destroy()

def chamar_tela_cadastro_colaborador(tela_anterior):
	tela_anterior.destroy()
	tela_cadastro_colaborador = Tk()
	tela_cadastro_colaborador["bg"] = "white"
	tela_cadastro_colaborador.geometry("500x680+300+10")
	tela_cadastro_colaborador.title("Cadastro") 
	tela_cadastro_colaborador.resizable(0,0)
	lb = Label(tela_cadastro_colaborador, text="Informe os dados do colaborador", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=30)
	
	dis_x = 110
	dis_y_inicial = 70

	#Nome:
	lb_nome = Label(tela_cadastro_colaborador, text="Nome:", bg="white")
	lb_nome.place(x=dis_x, y=dis_y_inicial)
	entrada_nome = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_nome.place(x=dis_x, y=dis_y_inicial+20)
	#Data de Nascimento
	lb_dt_nasc = Label(tela_cadastro_colaborador, text="Data de Nascimento:", bg="white")
	lb_dt_nasc.place(x=dis_x, y=dis_y_inicial+50)

	dt_format_nasc = StringVar()
	dt_format_nasc.set("DD/MM/AAAA")

	dt_format_entrada = StringVar()
	dt_format_entrada.set("DD/MM/AAAA")

	placeholder = lambda texto, event: texto.set("")

	entrada_dt_nasc = Entry(tela_cadastro_colaborador, width=40, bg="white", textvariable=dt_format_nasc)
	entrada_dt_nasc.bind('<Button-1>', lambda event:placeholder(dt_format_nasc,event))
	entrada_dt_nasc.place(x=dis_x, y=dis_y_inicial+70)

	#Laboratório
	lb_lab = Label(tela_cadastro_colaborador, text="Laboratório:", bg="white")
	lb_lab.place(x=dis_x, y=dis_y_inicial+100)

	if SCF_backend.user.funcao in ['ADM', 'Coordenador Geral']:	
		lista_lab = retorna_lista_lab()
		lista_lab.insert(0, "*Selecione o laboratório*")
		lista_func = ['Pesquisador', 'Gestor', 'Coordenador', 'ADM', 'Coordenador Geral']

	else:
		lista_func = ['Pesquisador', 'Gestor', 'Coordenador']
		lista_lab = [SCF_backend.user.lab]

	entrada_lab = ttk.Combobox(tela_cadastro_colaborador, width=37, state="readonly")
	entrada_lab.place(x=dis_x, y=dis_y_inicial+120)	
	entrada_lab['values'] = lista_lab
	entrada_lab.current(0)
	#Função
	lb_func = Label(tela_cadastro_colaborador, text="Função:", bg="white")
	lb_func.place(x=dis_x, y=dis_y_inicial+150)
	entrada_func = ttk.Combobox(tela_cadastro_colaborador, width=37, values=lista_func, state="readonly")
	entrada_func.place(x=dis_x, y=dis_y_inicial+170)	
	entrada_func.current(0)		
	#Carga Horária
	lb_CH = Label(tela_cadastro_colaborador, text="Carga Horária semanal:", bg="white")
	lb_CH.place(x=dis_x, y=dis_y_inicial+200)
	entrada_CH = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_CH.place(x=dis_x, y=dis_y_inicial+220)	
	#Data de Ingresso
	lb_dt_ing = Label(tela_cadastro_colaborador, text="Data de Ingresso:", bg="white")
	lb_dt_ing.place(x=dis_x, y=dis_y_inicial+250)
	entrada_dt_ing = Entry(tela_cadastro_colaborador, width=40, bg="white", textvariable=dt_format_entrada)
	entrada_dt_ing.bind('<Button-1>', lambda event:placeholder(dt_format_entrada,event))
	entrada_dt_ing.place(x=dis_x, y=dis_y_inicial+270)
	#Status
	lb_status = Label(tela_cadastro_colaborador, text="Status:", bg="white")
	lb_status.place(x=dis_x, y=dis_y_inicial+300)
	lista_status = ['Ativo', 'Não Ativo', 'Afastado']
	entrada_status = ttk.Combobox(tela_cadastro_colaborador, width=37, state="readonly")
	entrada_status.place(x=dis_x, y=dis_y_inicial+320)	
	entrada_status['values'] = lista_status
	entrada_status.current(0)
	#CPF
	lb_cpf = Label(tela_cadastro_colaborador, text="CPF:", bg="white")
	lb_cpf.place(x=dis_x, y=dis_y_inicial+350)
	entrada_cpf = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_cpf.place(x=dis_x, y=dis_y_inicial+370)

	#Upload Foto
	line_path = StringVar()
	lb_foto = Label(tela_cadastro_colaborador, text="Insira a foto do colaborador", bg="white").place(x=dis_x, y=dis_y_inicial+400)
	entrada_foto = Entry(tela_cadastro_colaborador, width=40, bg="white", textvariable= line_path)
	entrada_foto.place(x=dis_x, y=dis_y_inicial+420)

	bt_browser = Button(tela_cadastro_colaborador, text="Browser", bg="white", font=['TkDefaultFont', 7], command=partial(ImageMethods.get_path, line_path))
	bt_browser.place(x=dis_x+250, y=dis_y_inicial+420)
	label_info = Label(tela_cadastro_colaborador, text="*Campo não obrigatório!", font=['TkDefaultFont', 7], bg="white")
	label_info.place(x=dis_x, y=dis_y_inicial+440)

	#Senha
	lb_senha = Label(tela_cadastro_colaborador, text="Senha:", bg="white").place(x=dis_x, y=dis_y_inicial+460)
	entrada_senha = Entry(tela_cadastro_colaborador, width=40, bg="white", show="*")
	entrada_senha.place(x=dis_x, y=dis_y_inicial+480)
	#Confirme sua Senha
	lb_confirma_senha = Label(tela_cadastro_colaborador, text="Confirme sua Senha:", bg="white").place(x=dis_x, y=dis_y_inicial+510)
	entrada_confirma_senha = Entry(tela_cadastro_colaborador, width=40, bg="white", show="*")
	entrada_confirma_senha.place(x=dis_x, y=dis_y_inicial+530)

	tela_cadastro_colaborador.bind('<Return>', lambda event: cadastrar_colaborador(tela_cadastro_colaborador, entrada_nome, entrada_dt_nasc,
																					entrada_lab, entrada_func, entrada_CH, entrada_dt_ing, entrada_status, entrada_cpf,
																					entrada_senha, entrada_confirma_senha, entrada_foto, event))

	bt_ok = Button(tela_cadastro_colaborador, width=10, text="Cadastrar", bg="white", command=partial(cadastrar_colaborador, tela_cadastro_colaborador, entrada_nome, entrada_dt_nasc,
																									  entrada_lab, entrada_func, entrada_CH, entrada_dt_ing, entrada_status, entrada_cpf,
																									  entrada_senha, entrada_confirma_senha, entrada_foto)).place(x=275, y=625)
	if SCF_backend.user.funcao in ['ADM', 'Coordenador Geral']:
		bt_voltar = Button(tela_cadastro_colaborador, width=10, text="Voltar", bg="white", command=partial(chamar_tela_cadastro, tela_cadastro_colaborador)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	else:
		bt_voltar = Button(tela_cadastro_colaborador, width=10, text="Voltar", bg="white", command=partial(chamar_tela_inicial, tela_cadastro_colaborador)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
		
	

def chamar_tela_cadastro_laboratorio(tela_anterior):
	tela_anterior.destroy()
	tela_cadastro_laboratorio = Tk()
	tela_cadastro_laboratorio["bg"]="white"
	tela_cadastro_laboratorio.geometry("500x300+300+200")
	tela_cadastro_laboratorio.title("Cadastro") 
	tela_cadastro_laboratorio.resizable(0,0)
	lb = Label(tela_cadastro_laboratorio, text="Informe os dados do laboratório", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=20)
	
	#Nome:
	lb_nome = Label(tela_cadastro_laboratorio, text="Nome:", bg="white").place(x=110, y=80)
	entrada_nome = Entry(tela_cadastro_laboratorio, width=40, bg="white")
	entrada_nome.place(x=110, y=100)
	#Sigla:
	lb_sigla = Label(tela_cadastro_laboratorio, text="Sigla:", bg="white").place(x=110, y=130)
	entrada_sigla = Entry(tela_cadastro_laboratorio, width=40, bg="white")
	entrada_sigla.place(x=110, y=150)

	#Upload logo
		#Label e entry
	lb_logo = Label(tela_cadastro_laboratorio, text='Insira o logo do laboratório', bg='white').place(x=110, y=180)
	line_path = StringVar()
	entrada_logo = Entry(tela_cadastro_laboratorio, width=40, bg='white', textvariable = line_path)
	entrada_logo.place(x=110, y=200)
		#button
	bt_browser = Button(tela_cadastro_laboratorio, text='Browser', font=['TkDefaultFont', 7], bg='white', command = partial(ImageMethods.get_path, line_path))
	bt_browser.place(x=360, y=200)

	label_info = Label(tela_cadastro_laboratorio, text="*Campo não obrigatório!", font=['TkDefaultFont', 7], bg="white")
	label_info.place(x=110, y=220)

	tela_cadastro_laboratorio.bind('<Return>', lambda event:cadastrar_laboratorio(tela_cadastro_laboratorio, entrada_nome, entrada_sigla, entrada_logo, event))

	bt_voltar = Button (tela_cadastro_laboratorio, width=10, text="Voltar", bg="white", command=partial(chamar_tela_cadastro, tela_cadastro_laboratorio)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	bt_ok = Button(tela_cadastro_laboratorio, width=10, text="Cadastrar", bg="white", command=partial(cadastrar_laboratorio, tela_cadastro_laboratorio, entrada_nome, entrada_sigla, entrada_logo)).place(x=275, y=250)

def chamar_tela_dados_lab(tela_anterior, lab):
	tela_anterior.destroy()

	dados_lab = retorna_dados_lab(lab)

	tela_dados_lab = Tk()
	tela_dados_lab["bg"]="white"
	tela_dados_lab.geometry("500x300+300+200")
	tela_dados_lab.title("Dados laboratório: "+lab) 
	tela_dados_lab.resizable(0,0)
	lb = Label(tela_dados_lab, text="Dados do laboratório", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=20)
	
	#Nome:
	lb_nome = Label(tela_dados_lab, text="Nome:", bg="white").place(x=110, y=80)
	entrada_nome = Entry(tela_dados_lab, width=40, bg="white")
	entrada_nome.insert(0,dados_lab[0])
	entrada_nome.configure(state='readonly')
	entrada_nome.place(x=110, y=100)

	#Sigla:
	lb_sigla = Label(tela_dados_lab, text="Sigla:", bg="white").place(x=110, y=130)
	entrada_sigla = Entry(tela_dados_lab, width=40, bg="white")
	entrada_sigla.insert(0,dados_lab[1])
	entrada_sigla.configure(state='readonly')
	entrada_sigla.place(x=110, y=150)

	#Upload logo
		#Label e entry
	lb_logo = Label(tela_dados_lab, text='Insira o logo do laboratório', bg='white').place(x=110, y=180)
	line_path = StringVar()
	entrada_logo = Entry(tela_dados_lab, width=40, bg='white', textvariable = line_path)
	entrada_logo.place(x=110, y=200)
		#button
	bt_browser = Button(tela_dados_lab, text='Browser', font=['TkDefaultFont', 7], bg='white', command = partial(ImageMethods.get_path, line_path))
	bt_browser.place(x=360, y=200)

	label_info = Label(tela_dados_lab, text="*Campo não obrigatório!", font=['TkDefaultFont', 7], bg="white")
	label_info.place(x=110, y=220)

	tela_dados_lab.bind('<Return>', lambda event:atualizar_cadastro_laboratorio(tela_dados_lab, entrada_nome, entrada_sigla, entrada_logo, event))

	bt_voltar = Button (tela_dados_lab, width=10, text="Voltar", bg="white", command=partial(chamar_tela_consulta_2, tela_dados_lab, lab)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	bt_remover = Button(tela_dados_lab, width=20, text="Excluir laboratório", bg="white", command=partial(excluir_lab, tela_dados_lab, dados_lab[0], dados_lab[1])).pack(side=RIGHT, anchor = SE, pady=0, padx=4)
	bt_ok = Button(tela_dados_lab, width=10, text="Atualizar", bg="white", command=partial(atualizar_cadastro_laboratorio, tela_dados_lab, entrada_nome, entrada_sigla, entrada_logo)).place(x=275, y=240)


	
def pop_up(title, label):
	pop_up = Tk()
	pop_up["bg"]="white"
	pop_up.geometry("280x60+450+330")
	pop_up.title(title) 
	pop_up.resizable(0,0)
	lb = Label (pop_up, text=label, bg="white").pack(pady=20)


def chamar_tela_consulta(tela_anterior):
	tela_consulta = Tk()
	tela_consulta["bg"]="white"
	tela_consulta.geometry("500x300+300+200")
	tela_consulta.title("Consulta")
	tela_consulta.resizable(0,0) 
	lb = Label (tela_consulta, text="Consultar", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

	#lab
	lb_lab = Label(tela_consulta, text="Laboratório:", bg="white")
	lb_lab.place(x=110, y=130)
	lista_lab = retorna_lista_lab()
	lista_lab.insert(0,"*Selecione o laboratório*")

	entrada_lab = ttk.Combobox(tela_consulta, width=37, state="readonly")
	entrada_lab.place(x=110, y=150)	
	entrada_lab['values'] = lista_lab
	entrada_lab.current(0)

	tela_consulta.bind('<Return>',lambda event:validar_consulta(tela_consulta, entrada_lab, event))

	bt_ok = Button(tela_consulta, width=10, text="Avançar", bg="white", command=partial(validar_consulta, tela_consulta, entrada_lab)).place(x=275, y=177)
	bt_voltar = Button (tela_consulta, width=10, text="Voltar", bg="white", command=partial(chamar_tela_inicial, tela_consulta)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	tela_anterior.destroy()


def chamar_tela_consulta_2(tela_anterior, lab):

	tela_consulta = Tk()
	tela_consulta["bg"]="white"
	tela_consulta.geometry("500x300+300+200")
	tela_consulta.title("Consultar > Laboratório: "+lab) 
	tela_consulta.resizable(0,0)
	lb = Label (tela_consulta, text="Consultar", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

	#colaborador
	lb_colab = Label(tela_consulta, text="Colaborador:", bg="white")
	lb_colab.place(x=110, y=130)

	lista_colab = retorna_lista_colab(lab)
	lista_colab.insert(0,"*Selecione o colaborador*")

	entrada_colab = ttk.Combobox(tela_consulta, width=37, state="readonly")
	entrada_colab.place(x=110, y=150)	
	entrada_colab['values'] = lista_colab
	entrada_colab.current(0)

	tela_consulta.bind('<Return>', lambda event:validar_consulta_2(tela_consulta, entrada_colab, lab, event))	

	bt_ok = Button(tela_consulta, width=10, text="Avançar", bg="white", command = partial(validar_consulta_2, tela_consulta, entrada_colab, lab)).place(x=275, y=177)
	bt_consulta_lab = Button(tela_consulta, width=20, text="Consultar laboratório", bg="white", command=partial(chamar_tela_dados_lab, tela_consulta, lab)).pack(side=RIGHT, anchor = SE, pady=4, padx=4)

	if SCF_backend.user.funcao in ['ADM', 'Coordenador Geral']:
		bt_voltar = Button (tela_consulta, width=10, text="Voltar", bg="white", command=partial(chamar_tela_consulta, tela_consulta)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	else:
		bt_voltar = Button (tela_consulta, width=10, text="Voltar", bg="white", command=partial(chamar_tela_inicial, tela_consulta)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	tela_anterior.destroy()

def chamar_tela_dados_colaborador(tela_anterior, nome_colab, lab):
	colab = retorna_colab(nome_colab, lab)
	tela_anterior.destroy()
	tela_cadastro_colaborador = Tk()
	tela_cadastro_colaborador["bg"] = "white"
	tela_cadastro_colaborador.geometry("500x680+300+10")
	tela_cadastro_colaborador.title("Dados Cadastrais") 
	tela_cadastro_colaborador.resizable(0,0)
	lb = Label(tela_cadastro_colaborador, text="Dados Cadastrais", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=30)
	
	dis_x = 110
	dis_y_inicial = 70

	#Nome:
	lb_nome = Label(tela_cadastro_colaborador, text="Nome:", bg="white")
	lb_nome.place(x=dis_x, y=dis_y_inicial)
	entrada_nome = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_nome.place(x=dis_x, y=dis_y_inicial+20)
	entrada_nome.insert(0, colab.nome)
	#Data de Nascimento
	lb_dt_nasc = Label(tela_cadastro_colaborador, text="Data de Nascimento:", bg="white")
	lb_dt_nasc.place(x=dis_x, y=dis_y_inicial+50)
	entrada_dt_nasc = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_dt_nasc.place(x=dis_x, y=dis_y_inicial+70)
	entrada_dt_nasc.insert(0, colab.dtNasc)
	#Laboratório
	lb_lab = Label(tela_cadastro_colaborador, text="Laboratório:", bg="white")
	lb_lab.place(x=dis_x, y=dis_y_inicial+100)

	lista_lab = retorna_lista_lab()
	entrada_lab = ttk.Combobox(tela_cadastro_colaborador, width=37, state="readonly")
	entrada_lab.place(x=dis_x, y=dis_y_inicial+120)	
	entrada_lab['values'] = lista_lab
	entrada_lab.current(lista_lab.index(colab.lab))
	#Função
	lb_func = Label(tela_cadastro_colaborador, text="Função:", bg="white")
	lb_func.place(x=dis_x, y=dis_y_inicial+150)
	lista_func = ['Pesquisador', 'Gestor', 'Coordenador', 'ADM', 'Coordenador Geral']
	entrada_func = ttk.Combobox(tela_cadastro_colaborador, width=37, values=lista_func, state="readonly")
	entrada_func.place(x=dis_x, y=dis_y_inicial+170)
	entrada_func.current(lista_func.index(colab.funcao))		
	#Carga Horária
	lb_CH = Label(tela_cadastro_colaborador, text="Carga Horária semanal:", bg="white")
	lb_CH.place(x=dis_x, y=dis_y_inicial+200)
	entrada_CH = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_CH.place(x=dis_x, y=dis_y_inicial+220)	
	entrada_CH.insert(0, colab.ch)
	#Data de Ingresso
	lb_dt_ing = Label(tela_cadastro_colaborador, text="Data de Ingresso:", bg="white")
	lb_dt_ing.place(x=dis_x, y=dis_y_inicial+250)
	entrada_dt_ing = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_dt_ing.place(x=dis_x, y=dis_y_inicial+270)
	entrada_dt_ing.insert(0, colab.dtIngresso)
	#Status
	lb_status = Label(tela_cadastro_colaborador, text="Status:", bg="white")
	lb_status.place(x=dis_x, y=dis_y_inicial+300)
	lista_status = ['Ativo', 'Não Ativo', 'Afastado']
	entrada_status = ttk.Combobox(tela_cadastro_colaborador, width=37, state="readonly")
	entrada_status.place(x=dis_x, y=dis_y_inicial+320)	
	entrada_status['values'] = lista_status
	entrada_status.current(lista_status.index(colab.status))

	#Upload Foto
	line_path = StringVar()
	lb_foto = Label(tela_cadastro_colaborador, text="Insira a foto do colaborador", bg="white").place(x=dis_x, y=dis_y_inicial+350)
	entrada_foto = Entry(tela_cadastro_colaborador, width=40, bg="white", textvariable= line_path)
	entrada_foto.place(x=dis_x, y=dis_y_inicial+370)

	
	bt_browser = Button(tela_cadastro_colaborador, text="Browser", bg="white", font=['TkDefaultFont', 7], command=partial(ImageMethods.get_path, line_path))
	bt_browser.place(x=dis_x+250, y=dis_y_inicial+370)
	label_info = Label(tela_cadastro_colaborador, text="*Campo não obrigatório!", font=['TkDefaultFont', 7], bg="white")
	label_info.place(x=dis_x, y=dis_y_inicial+390)

	
	lb_senha = Label(tela_cadastro_colaborador, text="Senha:", bg="white").place(x=dis_x, y=dis_y_inicial+410)
	entrada_senha = Entry(tela_cadastro_colaborador, width=40, bg="white", show="*")
	entrada_senha.place(x=dis_x, y=dis_y_inicial+430)
	entrada_senha.insert(0, colab.senha)

	
	#Confirme sua Senha
	lb_confirma_senha = Label(tela_cadastro_colaborador, text="Confirme sua Senha:", bg="white").place(x=dis_x, y=dis_y_inicial+460)
	entrada_confirma_senha = Entry(tela_cadastro_colaborador, width=40, bg="white", show="*")
	entrada_confirma_senha.place(x=dis_x, y=dis_y_inicial+480)
	entrada_confirma_senha.insert(0, colab.senha)

	tela_cadastro_colaborador.bind('<Return>', lambda event:atualizar_cadastro_colaborador(tela_cadastro_colaborador, entrada_nome, entrada_dt_nasc,
																							entrada_lab, entrada_func, entrada_CH, entrada_dt_ing, entrada_status,
																							entrada_senha, entrada_confirma_senha, entrada_foto, nome_colab, colab.cpf, event))

	bt_ok = Button(tela_cadastro_colaborador, width=10, text="Atualizar", bg="white", command=partial(atualizar_cadastro_colaborador, tela_cadastro_colaborador, entrada_nome, entrada_dt_nasc,
																									  entrada_lab, entrada_func, entrada_CH, entrada_dt_ing, entrada_status,
																							  entrada_senha, entrada_confirma_senha, entrada_foto, nome_colab, colab.cpf)).place(x=275, y=600)

	bt_remover = Button(tela_cadastro_colaborador, width=20, text="Excluir colaborador", bg="white", command=partial(excluir_colaborador, tela_cadastro_colaborador, colab.cpf, colab.lab)).pack(side=RIGHT, anchor = SE, pady=4, padx=4)

	bt_voltar = Button(tela_cadastro_colaborador, width=10, text="Voltar", bg="white", command=partial(chamar_tela_consulta_2, tela_cadastro_colaborador, colab.lab)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	

def chamar_historico(tela_anterior):
	tela_hist = Tk()
	tela_hist["bg"]="white"
	tela_hist.geometry("500x300+300+200")
	tela_hist.title("Consultar Histórico")
	tela_hist.resizable(0,0) 
	lb = Label (tela_hist, text="Consultar Histórico", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)

	#lab
	lb_lab = Label(tela_hist, text="Laboratório:", bg="white").place(x=110, y=100)
	lb_mes = Label(tela_hist, text="Mês:", bg="white").place(x=110,y=145)
	lb_ano = Label(tela_hist, text="Ano:", bg="white").place(x=250,y=145)

	lista_lab = retorna_lista_lab()
	lista_lab.insert(0,"*Selecione o laboratório*")

	lista_mes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
	lista_ano = ["2018","2019","2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"]

	entrada_lab = ttk.Combobox(tela_hist, width=37, state="readonly")
	entrada_lab.place(x=110, y=120)	
	entrada_lab['values'] = lista_lab
	entrada_lab.current(0)

	entrada_mes = ttk.Combobox(tela_hist, width=12, state="readonly")
	entrada_mes.place(x=110, y=165)	
	entrada_mes['values'] = lista_mes
	entrada_mes.current(0)

	entrada_ano = ttk.Combobox(tela_hist, width=5, state="readonly")
	entrada_ano.place(x=250, y=165)	
	entrada_ano['values'] = lista_ano
	entrada_ano.current(0)

	tela_hist.bind('<Return>', lambda event: validar_chamada_historico(tela_anterior=tela_hist, lab=entrada_lab, mes=entrada_mes, ano=entrada_ano, tipo='r', event=event))

	bt_hist_resumido = Button(tela_hist, width=10, text="Resumido", bg="white", command=partial(validar_chamada_historico, tela_hist, entrada_lab, entrada_mes, entrada_ano,'r')).place(x=180, y=200)
	bt_hist_detalhado = Button(tela_hist, width=10, text="Detalhado", bg="white", command=partial(validar_chamada_historico, tela_hist, entrada_lab, entrada_mes, entrada_ano,'d')).place(x=275, y=200)
	bt_voltar = Button (tela_hist, width=10, text="Voltar", bg="white", command=partial(chamar_tela_inicial, tela_hist)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	tela_anterior.destroy()



def chamar_historico_2(tela_anterior, lista_tuplas, lab, mes, ano, tipo):

	if tipo == 'r':
		header = ['Nome', 'Horas Acumuladas']
	else:
		header = ['Nome', 'Entrada', 'Saida']

	titulo = "Histórico - "+lab.get()+" - "+mes+" - "+ano
	
	tela_anterior.destroy()

	tela_hist = Tk()
	tela_hist["bg"] = "white"
	lb = Label (tela_hist, text="Histórico", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=20)
	bt_voltar = Button(tela_hist, text="Voltar", bg="white", command = partial(chamar_historico, tela_hist)).pack(side=TOP, anchor=NW, pady=4, padx=4)
	tela_hist.geometry("500x300+300+200")
	tela_hist.resizable(0, 0)
	tela_hist.wm_title(titulo)
	tela_hist = McListBox(header, lista_tuplas)



def chamar_tela_login():
	tela_login = Tk()
	tela_login["bg"]="white"
	tela_login.geometry("500x350+300+200") #dimensoes da janela --> Largura x Altura + DistanciaDaMargemEsquerda + DistanciaDaMargemSuperior
	tela_login.title("Sistema de Controle de Frequência") #título da janela
	tela_login.resizable(0,0)

	#Logo
	imagem = PhotoImage(file="imagens/hub.png")
	lb_image = Label(tela_login, image = imagem, bg="white")
	lb_image.image = imagem
	lb_image.pack(pady=30)
	lb_login = Label(tela_login, text="CPF:", bg="white").place(x=120, y=150)
	entrada_login = Entry(tela_login, width=40, bg="white")
	entrada_login.place(x=120, y=170)
	
	lb_senha = Label(tela_login, text="Senha:", bg="white").place(x=120, y=200)
	entrada_senha = Entry(tela_login, width=40, bg="white", show="*")
	entrada_senha.place(x=120, y=220)

	enter_logar = lambda event:validar_login(event=event, tela_anterior=tela_login, login=entrada_login, senha=entrada_senha)

	bt_logar = Button(tela_login, width=10, bg="white", text="Login", command=partial(validar_login, tela_login, entrada_login, entrada_senha)).place(x=285, y=250)
	tela_login.bind('<Return>', enter_logar)
	tela_login.mainloop()

	
def chamar_tela_inicial(tela_anterior):
	tela_inicial = Tk() #criacao de uma janela - instancia de Tk
	tela_inicial.geometry("500x300+300+200") #dimensoes da janela --> Largura x Altura + DistanciaDaMargemEsquerda + DistanciaDaMargemSuperior
	tela_inicial.title("HUB - Tecnologia e Inovação") #título da janela
	tela_inicial["bg"]="white"
	tela_inicial.resizable(0,0)
	lb_inicial = Label (tela_inicial, text="Sistema de Controle de Frequência", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50) #criando rótulo

	if SCF_backend.user.funcao in ['ADM', 'Coordenador Geral']:
		bt_cadastrar = Button (tela_inicial, width=20, text="Cadastrar", command = partial(chamar_tela_cadastro, tela_inicial), bg="white").pack(pady=3) #criando botao "cadastrar"
		bt_consultar = Button (tela_inicial, width=20, text="Consultar", command = partial(chamar_tela_consulta, tela_inicial), bg="white").pack(pady=3) #criando botao "Consultar" 
	else:
		bt_cadastrar = Button (tela_inicial, width=20, text="Cadastrar colaborador", command = partial(chamar_tela_cadastro_colaborador, tela_inicial), bg="white").pack(pady=3) #criando botao "cadastrar"
		bt_consultar = Button (tela_inicial, width=20, text="Consultar", command = partial(chamar_tela_consulta_2, tela_inicial, SCF_backend.user.lab), bg="white").pack(pady=3)

	bt_hist = Button (tela_inicial, width=20, text="Histórico", bg="white", command = partial(chamar_historico, tela_inicial)).pack(pady=3) #criando botao "Histórico"
	

	bt_sair = Button (tela_inicial, width=10, text="Sair", bg="white", command=partial(deslogar, tela_inicial)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	tela_anterior.destroy()
