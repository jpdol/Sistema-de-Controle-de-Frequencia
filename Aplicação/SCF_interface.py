from SCF_backend import *
from functools import partial

def chamar_tela_cadastro(tela_anterior):
	tela_cadastro = Tk()
	tela_cadastro["bg"] = "white"
	tela_cadastro.geometry("500x300+300+200")
	tela_cadastro.title("Cadastro") 
	lb = Label (tela_cadastro, text="O que você deseja cadastrar?", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)
	bt_cadastrar_colaborador = Button (tela_cadastro, width=20, text="Colaborador", bg="white", command=partial(chamar_tela_cadastro_colaborador, tela_cadastro)).pack(pady=3)
	bt_cadastrar_laboratorio = Button (tela_cadastro, width=20, text="Laboratório", bg="white", command=partial(chamar_tela_cadastro_laboratorio,tela_cadastro)).pack(pady=3)
	bt_voltar = Button (tela_cadastro, width=10, text="Voltar", bg="white", command=partial(chamar_tela_inicial, tela_cadastro)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	tela_anterior.destroy()

def chamar_tela_cadastro_colaborador(tela_anterior):
	tela_cadastro_colaborador = Tk()
	tela_cadastro_colaborador["bg"] = "white"
	tela_cadastro_colaborador.geometry("500x650+300+40")
	tela_cadastro_colaborador.title("Cadastro") 
	lb = Label(tela_cadastro_colaborador, text="Informe os dados do colaborador", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=30)
	
	#Nome:
	lb_nome = Label(tela_cadastro_colaborador, text="Nome:", bg="white")
	lb_nome.place(x=110, y=100)
	entrada_nome = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_nome.place(x=110, y=120)
	#Data de Nascimento
	lb_dt_nasc = Label(tela_cadastro_colaborador, text="Data de Nascimento:", bg="white")
	lb_dt_nasc.place(x=110, y=150)
	entrada_dt_nasc = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_dt_nasc.place(x=110, y=170)
	#Laboratório
	lb_lab = Label(tela_cadastro_colaborador, text="Laboratório:", bg="white")
	lb_lab.place(x=110, y=200)
	entrada_lab = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_lab.place(x=110, y=220)	
	#Função
	lb_func = Label(tela_cadastro_colaborador, text="Função:", bg="white")
	lb_func.place(x=110, y=250)
	entrada_func = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_func.place(x=110, y=270)			
	#Carga Horária
	lb_CH = Label(tela_cadastro_colaborador, text="Carga Horária semanal:", bg="white")
	lb_CH.place(x=110, y=300)
	entrada_CH = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_CH.place(x=110, y=320)	
	#Data de Ingresso
	lb_dt_ing = Label(tela_cadastro_colaborador, text="Data de Ingresso:", bg="white")
	lb_dt_ing.place(x=110, y=350)
	entrada_dt_ing = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_dt_ing.place(x=110, y=370)
	#Status
	lb_status = Label(tela_cadastro_colaborador, text="Status:", bg="white")
	lb_status.place(x=110, y=400)
	entrada_status = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_status.place(x=110, y=420)
	#Senha
	lb_status = Label(tela_cadastro_colaborador, text="Senha:", bg="white")
	lb_status.place(x=110, y=450)
	entrada_status = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_status.place(x=110, y=470)
	#Confirme sua Senha
	lb_status = Label(tela_cadastro_colaborador, text="Confirme sua Senha:", bg="white")
	lb_status.place(x=110, y=500)
	entrada_status = Entry(tela_cadastro_colaborador, width=40, bg="white")
	entrada_status.place(x=110, y=520)


	bt_voltar = Button(tela_cadastro_colaborador, width=10, text="Voltar", bg="white", command=partial(chamar_tela_cadastro, tela_cadastro_colaborador)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	bt_ok = Button(tela_cadastro_colaborador, width=10, text="Cadastrar", bg="white", command=partial(cadastrar_colaborador, tela_cadastro_colaborador)).place(x=275, y=550)
	tela_anterior.destroy()

def chamar_tela_cadastro_laboratorio(tela_anterior):
	tela_cadastro_laboratorio = Tk()
	tela_cadastro_laboratorio["bg"]="white"
	tela_cadastro_laboratorio.geometry("500x300+300+200")
	tela_cadastro_laboratorio.title("Cadastro") 
	lb = Label(tela_cadastro_laboratorio, text="Informe os dados do laboratório", fg="orange", bg="white", font=["Verdana", 16]).pack(pady=50)
	
	#Nome:
	lb_nome = Label(tela_cadastro_laboratorio, text="Nome:", bg="white").place(x=110, y=130)
	entrada_nome = Entry(tela_cadastro_laboratorio, width=40, bg="white").place(x=110, y=150)
	#Sigla:
	lb_sigla = Label(tela_cadastro_laboratorio, text="Sigla:", bg="white").place(x=110, y=180)
	entrada_sigla = Entry(tela_cadastro_laboratorio, width=40, bg="white").place(x=110, y=200)

	bt_voltar = Button (tela_cadastro_laboratorio, width=10, text="Voltar", bg="white", command=partial(chamar_tela_cadastro, tela_cadastro_laboratorio)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	bt_ok = Button(tela_cadastro_laboratorio, width=10, text="Cadastrar", bg="white", command=partial(cadastrar_laboratorio, tela_cadastro_laboratorio)).place(x=275, y=230)
	tela_anterior.destroy()

def chamar_tela_consulta(tela_anterior):
	tela_consulta = Tk()
	tela_consulta["bg"]="white"
	tela_consulta.geometry("500x300+300+200")
	tela_consulta.title("Consulta") 
	lb = Label (tela_consulta, text="O que você deseja consultar?", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50)
	bt_consultar_colaborador = Button (tela_consulta, width=20, text="Colaborador", bg="white").pack(pady=3) 
	bt_consultar_laboratorio = Button (tela_consulta, width=20, text="Laboratório", bg="white").pack(pady=3)
	bt_voltar = Button (tela_consulta, width=10, text="Voltar", bg="white", command=partial(chamar_tela_inicial, tela_consulta)).pack(side=BOTTOM, anchor=SW, pady=4, padx=4)
	tela_anterior.destroy()

def chamar_tela_login():
	tela_login = Tk() 
	tela_login["bg"]="white"
	tela_login.geometry("500x300+300+200") #dimensoes da janela --> Largura x Altura + DistanciaDaMargemEsquerda + DistanciaDaMargemSuperior
	tela_login.title("HUB - Tecnologia e Inovação") #título da janela
	lb_inicial = Label (tela_login, text="Sistema de Controle de Frequência", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50) #criando rótulo
	lb_login = Label(tela_login, text="Login:", bg="white").place(x=110, y=130)
	entrada_login = Entry(tela_login, width=40, bg="white")
	entrada_login.place(x=110, y=150)
	lb_senha = Label(tela_login, text="Senha:", bg="white").place(x=110, y=180)
	entrada_senha = Entry(tela_login, width=40, bg="white")
	entrada_senha.place(x=110, y=200)
	bt_logar = Button(tela_login, width=10, bg="white", text="Login", command=partial(escolhe_tela, tela_login, entrada_login)).place(x=275, y=230)
	tela_login.mainloop()

	
def chamar_tela_inicial(tela_anterior):
	tela_inicial = Tk() #criacao de uma janela - instancia de Tk
	tela_inicial.geometry("500x300+300+200") #dimensoes da janela --> Largura x Altura + DistanciaDaMargemEsquerda + DistanciaDaMargemSuperior
	tela_inicial.title("HUB - Tecnologia e Inovação") #título da janela
	tela_inicial["bg"]="white"
	lb_inicial = Label (tela_inicial, text="Sistema de Controle de Frequência", fg= "orange", bg="white", font=["Verdana", 16]).pack(pady=50) #criando rótulo
	bt_cadastrar = Button (tela_inicial, width=20, text="Cadastrar", command = partial(chamar_tela_cadastro, tela_inicial), bg="white").pack(pady=3) #criando botao "cadastrar"
	bt_consultar = Button (tela_inicial, width=20, text="Consultar", command = partial(chamar_tela_consulta, tela_inicial), bg="white").pack(pady=3) #criando botao "Consultar" 	
	tela_anterior.destroy()
