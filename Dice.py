import requests
import json
import random

token = '76332e8b65c176da5e469809c1e21e9b9a37cafd9c195778dd126e855786c686'
tokenFile = 'token.txt'
userName = ''
userNameFile = 'userName.txt'
versionNumber = 'v2.1'

def setUp():
    global token
    fo = open(tokenFile, "a+")
    fo.seek(0, 0)
    fileContent = fo.read()
    if len(fileContent):
        token = fileContent
    fo.close()

    global userName
    fo = open(userNameFile, "a+")
    fo.seek(0, 0)
    userName = fo.read()
    fo.close()

    print('混元风暴骰子哥 Version: ' + versionNumber)
    print('当前用户 : ' + userName)
    print('当前token: ' + token)
    help()

def reset():
    os.remove(tokenFile)
    os.remove(userNameFile)

def postMessage(msg):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token
    head = {'Content-Type': 'application/json'}
    data = json.dumps({'msgtype': 'text','text': {'content': msg}})
    r = requests.post(url, headers=head, data=data)
    print(r.json())

def help():
    print('''
    尝试摇骰子输入: nDn
        例如: D20+3D6
        空敲回车可以重复上次的投掷（默认为D20）

    尝试控制台指令请参考:
        -h : help
        -t : token | [token]
        -n : name  | [name]
        -q : quit
        -r : reset config

    尝试提需求请联系火鸡好哥哥 
        we-chat: zczl1994
    ''')

def setUserName(newUserName):
    print('设置用户名: ' + newUserName)

    global userName
    userName = newUserName
    fo = open(userNameFile, "w")
    fo.write(userName)
    fo.close()

def setToken(newToken):
    print('设置token: ' + newToken)

    global token
    token = newToken
    fo = open(tokenFile, "w")
    fo.write(token)
    fo.close()

def control(inputStr):
    item = inputStr[1]
    if item == 'h':
        help()
    elif item == 't':
        setToken(inputStr[3:])
    elif item == 'n':
        setUserName(inputStr[3:])
    elif item == 'r':
        reset()
    elif item == 'q':
        quit()

def runloop():
    inputStr = input('roll: ')
    if len(inputStr) >= 2 and inputStr[0] == '-':
        control(inputStr)
    elif len(inputStr) == 0 or 'D' in inputStr: 
        roll(inputStr)
    else:
        help()

#Roll
lastRoll = 'D20'
def roll(inputStr):
    global lastRoll
    if len(inputStr) == 0:
        inputStr = lastRoll
    else: 
        lastRoll = inputStr
    
    rollItem = RollItem(inputStr)
    rollItem.roll()
   
    msg = '骰子哥 - '
    if len(userName) > 0:
        msg = msg + userName + ' - '
    msg += inputStr + ': '
    msg += rollItem.resultStr
    print(msg)
    postMessage(msg)

class DiceItem:
    def __init__(self, originStr):
        self.originStr = originStr

        strList = originStr.split("D")
        if len(strList) != 2:
            return

        if len(strList[0]) == 0:
            self.diceSideCount = int(strList[1])
            self.diceCount = 1
        else:
            self.diceSideCount = int(strList[1])
            self.diceCount = int(strList[0])

    def roll(self):
        self.resultList = []
        self.resultSum = 0
        self.resultStr = ''
        for i in range(self.diceCount):
            randNum = random.randint(1,self.diceSideCount)
            self.resultList.append(randNum)
            self.resultSum += randNum
            if i > 0:
                self.resultStr += ' + '
            self.resultStr += '[%d]' % randNum
            

    def descript(self):
        return '[%dD%d]' % (self.diceCount, self.diceSideCount)
    

class RollItem:
    def __init__(self, originStr):
        print('RollItem' + originStr)
        self.originStr = originStr 

        diceStrList = self.originStr.split("+")
        diceList = []
        for diceStr in diceStrList:
            diceList.append(DiceItem(diceStr))
        self.diceList = diceList
    
    def roll(self):
        self.resultList = []
        self.resultSum = 0
        self.resultStr = ''

        if len(self.diceList) == 1 and self.diceList[0].diceCount == 1:
            diceItem = self.diceList[0]
            diceItem.roll()
            self.resultList.append(diceItem)
            self.resultSum = diceItem.resultSum
            self.resultStr += '[%d]' % self.resultSum
            return

        for diceItem in self.diceList:
            diceItem.roll()
            self.resultList.append(diceItem)
            self.resultSum += diceItem.resultSum
            if self.diceList.index(diceItem) > 0:
                self.resultStr += ' + '
            self.resultStr += diceItem.resultStr

        self.resultStr += ' = [%d]' % self.resultSum

#Runloop
setUp()
while(1):
    runloop()