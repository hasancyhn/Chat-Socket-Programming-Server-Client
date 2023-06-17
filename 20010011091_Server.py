from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}        # Baglanan kullanicilari listeliyoruz.
addresses = {}      # Baglanan kullanicilarin IP adreslerini listeliyoruz.

HOST = '127.0.0.1'  # Localhost IP adresimiz.
PORT = 12345
BUFFERSIZE = 2048   # Paket boyutunu 2048 olarak belirledik.
ADDR = (HOST, PORT) # Adresimiz

SERVER = socket(AF_INET, SOCK_STREAM)   # Server baglantisi kuruluyor.
SERVER.bind(ADDR)                       # Server'in HOST ve PORT ile olan baglantisi gerceklestiriliyor.

def gelenMesajFonksiyonu():
    while True:
        client, clientAddress = SERVER.accept()
        print("%s  :  %s baglandi."% clientAddress)
        client.send(bytes("Kullanici Adinizi Girdikten Sonra Mesajlasmaya Baslayabilirsiniz: ", "utf8"))
        addresses[client] = clientAddress   # Gelen bilgiyi ekliyoruz.
        Thread(target=baglan_client, args=(client,)).start()

def baglan_client(client):
    isim = client.recv(BUFFERSIZE).decode("utf8")
    hosgeldin = 'Hosgeldin %s.   Cikmak icin "cikis" yazabilirsin ya da "Cikis" butonuna tiklayabilirsin.' %isim

    client.send(bytes(hosgeldin, "utf8"))
    msg = "%s multiClient Chat Programina baglandi!" %isim
    yayin(bytes(msg, "utf8"))
    clients[client] = isim

    while True:
        msg = client.recv(BUFFERSIZE)
        if msg != bytes("cikis", "utf8"):
            yayin(msg, isim+": ")
        else:
            client.send(bytes("cikis", "utf8"))
            client.close()
            del clients[client]
            yayin(bytes("%s Kanaldan cikis yapti." %isim, "utf8"))
            break

def yayin(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(71)       # Maximum 71 baglantiya izin verir!
    print("Client'in baglanmasi bekleniyor...")
    ACCEPT_THREAD = Thread(target=gelenMesajFonksiyonu)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()