from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def gelenMesajFonksiyonu():
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            mesajListesi.insert(tkinter.END, msg)
        except OSError:
            break # Eger kullanici cikis yaparsa

def gonder(event=None):
    msg = mesajim.get()     # Gonderilen mesaj aliniyor.
    mesajim.set("")         # Gonderilen mesaj bosaltiliyor
    client_socket.send(bytes(msg, "utf8"))
    if msg == "cikis":
        client_socket.close()
        app.quit()

def cikisFonksiyonu(event=None):
    mesajim.set("cikis")
    gonder()

app = tkinter.Tk()
app.title("multiClient Chat Programi ") # Programin basligini belirledim.

mesajKismi = tkinter.Frame(app)
mesajim = tkinter.StringVar()
mesajim.set("Buraya yazin.")    # Kullanicinin mesaji buraya yazmasi gerektigini gosterdim.

scrollbar = tkinter.Scrollbar(mesajKismi)
mesajListesi = tkinter.Listbox(mesajKismi, height=20, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

mesajListesi.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
mesajListesi.see("end")
mesajListesi.pack()
mesajKismi.pack()

girisLabeli = tkinter.Entry(app, textvariable=mesajim, foreground="Blue")
girisLabeli.bind("<Return>", gonder)    # Enter tusuyla gonderme imkanini sagladim.
girisLabeli.pack()

gondermeButonu = tkinter.Button(app, text="Gonder", command=gonder, foreground="Red")
gondermeButonu.pack()

cikisButonu = tkinter.Button(app, text="Cikis", command=cikisFonksiyonu)
cikisButonu.pack()


app.protocol("WM_DELETE_WINDOW", cikisFonksiyonu)

HOST = '127.0.0.1'
PORT = 12345
BUFFERSIZE = 2048
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=gelenMesajFonksiyonu)
receive_thread.start()
tkinter.mainloop()