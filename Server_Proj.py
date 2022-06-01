import socket
import random
import smtplib
import select
import time
from cryptography.fernet import Fernet
import mysql.connector
import requests

class Server:

    def send_request_to_client(self,request ,socket):
        """Send the request to the server. First the length of the request (2 digits), then the request itself
        Example: '04EXIT'
        Example: '12DIR c:\cyber'
        """

        length = str(len(request.encode('utf-8')))
        zfill_length = length.zfill(2)
        message = zfill_length + request

        socket.send(message.encode('utf-8'))

    def who_paints(self,client_sockets):
        rand=random.randint(0,len(client_sockets)-1)
        paint=client_sockets[rand]
        return paint

    def recive_request_from_client(self,current_socket):
        length = current_socket.recv(2).decode()
        data = current_socket.recv(int(length)).decode()
        return data

    def paints_now(self,paint,unPainted_list,client_sockets):
        unPainted_list.remove(paint)
        for i in client_sockets:
            if (i != paint):
                self.send_request_to_client('Not painter', i)
        self.send_request_to_client('Painter', paint)

    def chosen_words(self,paintedwords):
        rand1 = random.randint(1, 30)
        rand2 = random.randint(1, 30)
        for i in paintedwords:
            if (i[1] == rand1):
                word1 = i[0]
            if (i[1] == rand2):
                word2 = i[0]
        return word1, word2

    def getFromDB(self,mycursor,fernet,pw):
        print(pw)

        for x in mycursor:
            print(x)
            if fernet.decrypt(x[1].encode()).decode()==pw:
                return x
        return None


def main():
    s=Server()
    with open('datas.txt', 'r') as f:
        data_list = []
        for line in f:
            print(line)
            data_list.append(line.split(' ')[1][:-1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_PORT = int(data_list[1])
    SERVER_IP = "0.0.0.0"
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    client_sockets = []

    unPainted_list=[]
    countTimeOver=0
    numClients=0
    maxClients=int(data_list[2])

    EMAIL_ADDRESS = "draw.idf.io@gmail.com"
    EMAIL_PASSWORD = "a1234567!"

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = "Registered successfully to DRAWIO"
    body = "You have successfully logged in to DRAWIO game, welcome!!"
    msg = f'Subject: {subject}\n\n{body}'

    print("Server is up and running")
    mydb = mysql.connector.connect(host="localhost", user="Yoav Kerem", password="yoavkay25", database="wordsdb")
    mycursor = mydb.cursor()
    paintedWords = []
    guess_points=5
    paint=0
    guessWord=''
    pw_list=[]

    mycursor.execute("SELECT * FROM PaintedWords")
    for x in mycursor:
        paintedWords.append(x)
    word1, word2 = s.chosen_words(paintedWords)
    # 2gsTN-tzEllR1IdyV4KxCpdhi_qh2kCW5DDrUMSTZtk=
    key = '2gsTN-tzEllR1IdyV4KxCpdhi_qh2kCW5DDrUMSTZtk='.encode()
    # Instance the Fernet class with the key
    fernet = Fernet(key)

    while True:
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, [], [])
        for current_socket in rlist:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
            else:
                data=s.recive_request_from_client(current_socket)
                if data[0]=='L':
                    informs = data[1:]
                    informs=informs.split(' ')
                    result = s.getFromDB(mycursor,fernet,informs[1])
                    if result:
                        pw_list.append((current_socket,informs[1],0))
                        s.send_request_to_client('suitability',current_socket)
                    else:
                        s.send_request_to_client('unsuitability',current_socket)
                elif data=="logged in":
                    numClients+=1
                elif data[0]=='N':
                    informs=data[1:]
                    informs=informs.split(' ')
                    response = requests.get("https://isitarealemail.com/api/email/validate",params={'email': informs[2]})
                    status = response.json()['status']
                    print(informs[2])
                    if status == "valid":
                        smtp.sendmail(EMAIL_ADDRESS, informs[2], msg)
                        cryptPw = fernet.encrypt(informs[1].encode())
                        mycursor.execute(
                        "insert into PlayerInfor values ('" + informs[0] + "','" + cryptPw.decode() + "','" +
                        informs[2] + "',0,0,0)")
                        mydb.commit()
                        print('ok')

                        s.send_request_to_client("valid",current_socket)
                    else:
                        s.send_request_to_client("unvalid",current_socket)

                elif data == "":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    current_socket.close()
                elif data[0]=='w':
                    guessWord=data[1:]
                elif data.split(' ')[0]=='end':
                    data=data.split(' ')

                    for i in range(len(pw_list)):
                        if current_socket==pw_list[i][0]:
                            x=list(pw_list[i])
                            x[2]=int(data[1])
                            pw_list[i]=tuple(x)
                            mycursor.execute("SELECT * FROM PlayerInfor")
                            result = s.getFromDB(mycursor, fernet, pw_list[i][1])
                            print(result)
                            games = result[5]
                            sql = "UPDATE PlayerInfor SET games = %s WHERE games = %s"
                            val = (games + 1, games)
                            mycursor.execute(sql, val)
                            mydb.commit()

                    countTimeOver += 1
                    if countTimeOver==maxClients:
                        max = pw_list[0]
                        for i in pw_list:
                            if int(i[2]) > int(max[2]):
                                max = i
                        mycursor.execute("SELECT * FROM PlayerInfor")
                        result = s.getFromDB(mycursor, fernet, max[1])
                        wins = result[4]
                        sql = "UPDATE PlayerInfor SET wins = %s WHERE wins = %s"
                        val = (wins + 1, wins)
                        mycursor.execute(sql, val)
                        mydb.commit()

                        for j in client_sockets:
                            for i in pw_list:
                                result = s.getFromDB(mycursor, fernet, i[1])
                                s.send_request_to_client(result[0]+' '+str(i[2]),j)
                                print('sent')
                        for i in pw_list:
                            result = s.getFromDB(mycursor, fernet, i[1])
                            s.send_request_to_client(str(result[3])+' '+str(result[4])+' '+str(result[5]),i[0])

                elif data=="Time over":
                    countTimeOver+=1
                    if countTimeOver==maxClients:
                        guess_points = 5
                        countTimeOver=0
                        guess_players = len(client_sockets) - 1
                        paint = s.who_paints(unPainted_list)
                        s.paints_now(paint,unPainted_list,client_sockets)
                        word1, word2 = s.chosen_words(paintedWords)
                        s.send_request_to_client(word1 + '&' + word2, paint)
                else:
                    if current_socket == paint:
                        for i in client_sockets:
                            if i!=paint:
                                s.send_request_to_client(data,i)
                    else:
                        if data == guessWord:
                            for i in pw_list:
                                if i[0]==current_socket:
                                    mycursor.execute("SELECT * FROM PlayerInfor")
                                    result = s.getFromDB(mycursor, fernet, i[1])
                            pts=result[3]
                            new_pts=result[3]+guess_points
                            sql = "UPDATE Player SET points = %s WHERE points = %s"
                            val = (new_pts, pts)
                            mycursor.execute(sql, val)
                            mydb.commit()

                            guess_players -= 1
                            s.send_request_to_client('true ' + str(guess_points), current_socket)
                            guess_points -= 1
                            if guess_players == 0:
                                for i in client_sockets:
                                    s.send_request_to_client("done", i)
                                guess_players = 1
                        else:
                            s.send_request_to_client("wrong", current_socket)
                if numClients==maxClients:
                    numClients = 0
                    for i in client_sockets:
                        s.send_request_to_client("start "+str(maxClients),i)
                    guess_players= len(client_sockets)-1

                    paint=s.who_paints(client_sockets)
                    for i in client_sockets:
                        if i!=paint:
                            s.send_request_to_client('Not painter',i)
                            unPainted_list.append(i)
                    s.send_request_to_client('Painter',paint)

                    s.send_request_to_client(word1 + '&' + word2, paint)


if __name__=='__main__':
    main()