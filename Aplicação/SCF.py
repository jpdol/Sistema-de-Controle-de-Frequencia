import SCF_interface as interface
import sqlite3
import SCF_backend as back

if __name__ == "__main__":
	back.criar_conexao()
	app = interface.SCFapp()
	app.mainloop()
