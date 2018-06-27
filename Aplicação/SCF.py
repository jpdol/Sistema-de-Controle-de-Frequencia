import SCF_interface as inter
import sqlite3
import SCF_backend as back

if __name__ == "__main__":
	back.criar_conexao()
	inter.chamar_tela_login()