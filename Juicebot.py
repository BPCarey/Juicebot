# no encyption=6667, running on ipv4
 
import socket, sys, subprocess
 
network = "irc.rizon.net"
port = 6667
channel = "#Rizon"
username = "juicebot"
irc = socket.socket (socket.AF_INET, socket.SOCK_STREAM) #create socket
irc.connect((network, port)) #connect with the server

def recv_txt(sender_nick):
    """
    Receives text from a user on the following command: `<bot nick> write to file`
    """
    irc.send ('PRIVMSG ' + sender_nick + ' :Hello, ' + sender_nick + '! Please send your file and type #END# when you are done.\r\n')
    result = ""
    while True:
        data = irc.recv (4096)
        if data.startswith(':'+sender_nick) and data.find ("PRIVMSG " + username + " :") != -1: #listening to PMs from the current sender only
            buf = data.split("PRIVMSG " + username + " :")[1]
            if buf != '#END#\r\n':
                result+=buf
            else:
                irc.send ('PRIVMSG ' + sender_nick + ' :Thank you, ' + sender_nick + '! Your file has been received.\r\n')
                return result

print irc.recv (4096)
irc.send ('NICK ' + username + '\r\n')
irc.send ('USER ' + username + ' ' + username + ' ' + username + ' :Python IRC\r\n' )
irc.send ('JOIN ' + channel + '\r\n')
irc.send ('PRIVMSG ' + channel + ' :Hello.\r\n')
while True:
        data = irc.recv (4096)
        if data.find ('PING') != -1:
                irc.send ('PONG ' + data.split() [1] + '\r\n')
        if data.find (username + ' go away') !=-1: #Remote quit
                irc.send ('PRIVMSG ' + channel + ' :Fine, if you do not want me\r\n')
                irc.send ( 'QUIT\r\n')
                irc.close()
                sys.exit()
        if data.find ('hi ' + username) != -1:
                irc.send ('PRIVMSG ' + channel + ' :Hey!\r\n')
        if data.find ('KICK') != -1: #auto log in after getting kicked
                irc.send ('JOIN ' + channel + '\r\n')
        if data.find (username + ' write to file') != -1:
                sender_nick = data.split("!")[0][1:] #TODO: It would be better to use regular expressions for extracting data
                irc.send ('PRIVMSG ' + channel + ' :Thanks for your request, ' + sender_nick + ', I\'m sending you a PM!\r\n')
                received = recv_txt(sender_nick)
                print received
                f = open('file.py', 'r+')
                f.write(received)
                f.close
                subprocess.call(['python', 'file.py'])
 
        print data