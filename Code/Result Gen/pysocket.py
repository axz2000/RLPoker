import socket
import sys
from Matchstate2Action import M2A

class MySocket:
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
		self.sock.settimeout(5)

	def connect(self, host, port):
		self.sock.connect((host, port))

	def mysend(self, msg):
		totalsent = 0
		MSGLEN = len(msg)
		while totalsent < MSGLEN:
			#sent = self.sock.send(msg[totalsent:].encode())
			sent = self.sock.send(bytes(msg[totalsent:],'utf-8'))
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent
	def readline(self):
		line = ''
		while True:
			part = self.sock.recv(1)
			part = part.decode('utf-8')
			if part != '\n':
				line+=part
			elif part=='\n':
				break
		return line
	def myreceive(self):
		chunks = []
		MSGLEN = 500
		bytes_recd = 0
		while bytes_recd < MSGLEN:
			chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return b''.join(chunks)

def isOurTurn(x):
	x = x.strip()
	actStr = x.split(":")[3]
	areweSB = True if x[x.find("|")-1]==':' else False
	
	rounds = actStr.split('/')
	r = rounds[-1]
		
	charLocs = []
	for i,c in enumerate(r):
		if c.isalpha(): charLocs.append(i)
	
	if (len(rounds)==1 and len(charLocs)%2==1) or (len(rounds)>1 and len(charLocs)%2==0):
		return False if areweSB else True
	elif (len(rounds)==1 and len(charLocs)%2==0) or (len(rounds)>1 and len(charLocs)%2==1):
		return True if areweSB else False
	else: return True
#player = M2A('XGB2_4.pickle','XGB5_7.pickle','XGB6_5.pickle','XGB7_10.pickle')
player = M2A('CART2_15.pickle','CART5_16.pickle','CART6_16.pickle','CART7_16.pickle')
print('Player Formed',flush=True)
s = MySocket()
#arg 1 = hostname, arg 2 = port
s.connect(sys.argv[1],int(sys.argv[2]))
s.mysend("VERSION:2.0.0\r\n")

count = 0
while True:
	line = s.readline()			
	line = line.strip()
	if line[0]=='#' or line[0] ==';': continue
	
	if not isOurTurn(line) or '///' in line: continue

	line += ':'

	line += player.retMoveStr(line[:-1])	

	line += '\r\n'
	s.mysend(line)
	count+=1
		








