import requests
import json
import random

token = '76332e8b65c176da5e469809c1e21e9b9a37cafd9c195778dd126e855786c686'
tokenFile = 'token.txt'
userName = ''
userNameFile = 'userName.txt'

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

def postMessage(msg):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token
    head = {'Content-Type': 'application/json'}
    data = json.dumps({'msgtype': 'text','text': {'content': msg}})
    r = requests.post(url, headers=head, data=data)
    print(r.json())

def rollDice(diceSideCount, diceCount = 1):
    msg = '骰子哥 - '
    if len(userName) > 0:
        msg = msg + userName + ' - '
    msg = msg + '%dD%d: ' % (diceCount, diceSideCount)
    if diceCount == 1:
        randNum = random.randint(1,diceSideCount)
        msg = msg + '[%d]' % randNum
    else:
        sum = 0
        for i in range(diceCount):
            if i != 0:
                msg = msg + ' + '
            randNum = random.randint(1,diceSideCount)
            sum += randNum
            msg = msg + '[%d]' % randNum
        msg = msg + ' = [%d]' % sum
    
    print(msg)
    postMessage(msg)

def help():
    print('''
    尝试摇骰子输入: xDx 
        例如: 1D20

    尝试控制台指令请参考:
        -h : help
        -t : token  [token]
        -n : name   [name]
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

def reset():
    os.remove(tokenFile)
    os.remove(userNameFile)

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

lastRoll = 'D20'
def roll():
    inputStr = input('roll: ')
    if len(inputStr) >= 2 and inputStr[0] == '-':
        control(inputStr)
    elif len(inputStr) == 0 or 'D' in inputStr: 
        global lastRoll
        if len(inputStr) == 0:
            inputStr = lastRoll
        else: 
            lastRoll = inputStr
        
        DIdx = inputStr.find('D')
        diceSideCount = int(inputStr[DIdx + 1:])
        diceCountStr = inputStr[:DIdx]

        if len(diceCountStr) == 0: 
            rollDice(diceSideCount)
        else:
            diceCount = int(diceCountStr)
            rollDice(diceSideCount, diceCount)
    else:
        help()

setUp()
while(1):
    roll()