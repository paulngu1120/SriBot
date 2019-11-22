#!/usr/bin/python3
import socket, requests, json

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "kukki.asuscomm.com" # Server
channel = "#general" # Channel
botnick = "SrirachaBot" # Your bots nick.
adminname = "pauly" #Your IRC nickname. 
exitcode = botnick + "Cha" #end life
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # user information
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot

def joinchan(chan): # join channel(s).
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8")) 
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1: 
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping(): # respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel): # sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ channel +" :"+ msg +"\n", "UTF-8"))

def help(topic):
    message = ''
    if not topic:
        #if there is no argument display a help menu to guide users
        message = "SrirachaBot \'!help\' with topics" 
        sendmsg(message, channel)
    if topic == 'weather':
        message = 'Use \'!weather <zipcode>\' for detailed forecast in that area'
        sendmsg(message, channel)
    else:
        message = "Feature not implemented yet. Use \'!help\'"
        print(topic)
        sendmsg(message, channel)

def weather(zipcode):
    #rapidapi
    url = "https://us-weather-by-zip-code.p.rapidapi.com/getweatherzipcode"
    querystring = {"zip":zipcode}
    headers = {
            'x-rapidapi-host':"us-weather-by-zip-code.p.rapidapi.com",
            'x-rapidapi-key':"d4d64d1a1emsh3a0702a55e170d5p1a2c02jsnaed2eceb8b88"
            }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #to parse json file into python dict
    message = json.loads(response.text) 
    sendmsg('The weather in ' + message['City'] + ' ' + message['State'] + ' is ' + message['Weather'] + ' at ' + message['TempF'] + ' degrees.')


def main():
    joinchan(channel)
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
            if message[:5] == '!help':
                help(message[6:])
            if message[:8] == '!weather':
                weather(message[9:])
            if len(name) < 17:
                if message.find('Hi ' + botnick) != -1:
                    sendmsg("Hello " + name + "!")
                if message.find('Bye ' + botnick) != -1:
                    sendmsg("Bye " + name + "!")
            if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                sendmsg("Heroes Never Die!")
                ircsock.send(bytes("QUIT \n", "UTF-8"))
                return
    else:
        if ircmsg.find("PING :") != -1:
            ping()


if __name__ == "__main__":
    main()
 
