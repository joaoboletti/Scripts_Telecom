from tkinter import *
import os



def chama_script():
    comando = "python desbloqueio.py "+input1.get()+" "+input2.get()+" "+input3.get()
    os.system(comando)


janela = Tk()
janela.title("Desbloqueio OLT Fiberhome")


sair = Button(janela)
sair["text"] = "Sair"
sair["font"] = ("Calibri", "10")
sair["width"] = 5
sair["command"] = janela.quit
sair.pack()



fontePadrao = ("Arial", "10")

nomeLabel = Label(janela, text="IP OLT", font=fontePadrao)
nomeLabel.pack(side=LEFT)
input1 = Entry(janela)
input1["width"] = 30
input1["font"] = fontePadrao
input1.pack(side=LEFT)

nomeLabel = Label(janela, text="Usuario", font=fontePadrao)
nomeLabel.pack(side=LEFT)
input2 = Entry(janela)
input2["width"] = 20
input2["font"] = fontePadrao
input2.pack(side=LEFT)

nomeLabel = Label(janela, text="Senha", font=fontePadrao)
nomeLabel.pack(side=LEFT)
input3 = Entry(janela)
input3["width"] = 20
input3["font"] = fontePadrao
input3.pack(side=LEFT)

desbloquear = Button(janela)
desbloquear["text"] = "Desbloquear"
desbloquear["font"] = ("Calibri", "8")
desbloquear["width"] = 12
desbloquear["command"] = chama_script
desbloquear.pack(side=RIGHT)



janela.mainloop()
