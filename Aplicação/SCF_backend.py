from tkinter import *
import SCF_interface as inter

def cadastrar_colaborador(tela_anterior):
	pass

def cadastrar_laboratorio(tela_anterior):
	pass



def escolhe_tela(tela_anterior, login):
	if login.get() == "admin":
		inter.chamar_tela_inicial(tela_anterior)
	
