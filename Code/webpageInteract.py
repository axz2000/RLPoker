from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from card import Card
import numpy as np
from treys import Evaluator

preFlopRanks = np.load('preFlopRank.pickle',allow_pickle=True)
evaluator = Evaluator()

def evalCardSet(board,hand):
    global preFlopRanks,evaluator
    
    if len(board)==0:
        a,b,c = str(hand[0]._numLet), str(hand[1]._numLet), 1 if hand[0]._suit==hand[1]._suit else 0
        try: return preFlopRanks[a,b,c]
        except: return preFlopRanks[b,a,c]
    else:
        board,hand = [i.toInt() for i in board],[i.toInt() for i in hand]
        return evaluator.evaluate(board, hand)
        
def _genGameFeatures(hand, board, prevFeats, stack):
    
    gameFeatures = 5*[0]

    holeCards = sorted(hand)
    tableCards = sorted(board)

    if len(tableCards)==0:
        gameFeatures[0] = evalCardSet([],holeCards)
        prevFeats = [gameFeatures[0]]
    elif len(tableCards)==3:
        gameFeatures[0:2] = [prevFeats[0],evalCardSet(tableCards,holeCards)]
        prevFeats = [gameFeatures[0],gameFeatures[1]]
    elif len(tableCards)==4:
        gameFeatures[0:3] = [prevFeats[0],prevFeats[1],evalCardSet(tableCards,holeCards)]
        prevFeats = [gameFeatures[0],gameFeatures[1],gameFeatures[2]]
    elif len(tableCards)==5:
        gameFeatures[0:4] = [prevFeats[0],prevFeats[1],prevFeats[2],evalCardSet(tableCards,holeCards)]
        prevFeats = [gameFeatures[0],gameFeatures[1],gameFeatures[2],gameFeatures[3]]

    gameFeatures[-1] = stack
    
    return gameFeatures, prevFeats


    #0 fold, 1 check, 2 call, 3 bet
def allActions(options,stack,choices,roundBets,handBets,minBet=1,maxBet=200):
    actions = []
    if options[0]==1:
        actions.append(('fold',))
    if options[1]==1:
        actions.append(('check',))
    if options[2]==1:
        actions.append(('call',))
    if options[3]==1:
        for val in choices:
            amt = int(stack*val)
            if amt+roundBets[1] > max(roundBets)+minBet and amt+roundBets[1]+handBets[1]<=maxBet:
                actions.append(('bet',amt))
    return actions
        
    
def _genActionFeatures(action, roundBets, handBets):

    """ This method generates a set of features from a player action. """

    #create binary encoding for action type
    actionFeatures = 7 * [0]

    if action[0] == 'check': actionFeatures[0] = 1
    elif action[0] == 'fold': actionFeatures[1] = 1
    elif action[0] == 'call': actionFeatures[2] = 1
    elif action[0] == 'raise' or action[0] == 'bet':
        actionFeatures[3] = 1
        actionFeatures[4] = action[1]    #raise to amount
        actionFeatures[5] = action[1] - max(roundBets)    #raise by amount
        actionFeatures[6] = actionFeatures[5] / (sum(roundBets) + sum(handBets))    #proportion of raise by to pot size
    else: raise Exception('Invalid action.')

    return actionFeatures    


def strToCard(s):
    r,s = s[0],s[1]
    if not r.isalpha():
        r = int(r)
    return Card(r,s)
def processBoard(s):
    ret = [s[i:i+2] for i in range(0, len(s), 2)]
    ret = [strToCard(i) for i in ret]
    return ret

def processActionStr(s):
    if s=='':
        return []
    final=[]
    idxs=[]
    for i in range(len(s)):
        if s[i].isalpha() or s[i]=='/':
            idxs.append(i)
    for i in range(len(idxs)-1):
        final.append(s[idxs[i]:idxs[i+1]])
    final.append(s[idxs[-1]:])
    return final

def getActions(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'action0')))
    s = driver.find_elements_by_xpath('/html/body/div[1]/div[1]/table[2]/tbody/tr/td[3]/table')
    tds = s[0].find_elements_by_tag_name('td')
    actions = [td.text for td in tds]
    actions = [i for i in actions if i] #remove empty strs
    return actions
def subtractStrs(a,b):
    if b in a:
        return a[a.find(b)+len(b):]
    return a

def waitUntilUpdate(driver, prev):
    mustend = time.time() + 5
    while time.time() < mustend:
        a = getActionStr(driver)
        if a!=prev:
            return a
        time.sleep(0.05)
    return False
    
def getActionStr(driver):
    return  driver.find_element_by_xpath('/html/body/div[1]/div[1]/table[3]/tbody/tr/td[2]').text
def getOutcome(driver):
    return driver.find_element_by_xpath('/html/body/div[1]/div[1]/table[4]/tbody/tr[1]/td[2]').text
def getPic(driver):
    return driver.find_element_by_xpath('/html/body/div[1]/div[1]/table[2]/tbody/tr/td[2]/canvas')
def hasHandEnded(driver):
    return getOutcome(driver)!=''
    
def parseOutcome(driver):
    outcome = getOutcome(driver)
    
    #0 if we lose, 1 if we won, -1 if chopped
    
    winner = 1 if outcome[0]=='Y' else 0
    if winner==1:
        winner = -1 if outcome.split(' ')[1][0]=='c' else 1
    try:
        if outcome[0]!='Y' and outcome[0]!='S':
            1/0
        return winner
    except:
        for i in range(10): print(outcome)
        quit()
        
def getActiveButtons(driver):
    ret = [0,0,0,0]
    #0 fold, 1 check, 2 call, 3 bet
    ret[0] = 1 if driver.find_element_by_id("fold").is_enabled() else 0
    ret[1] = 1 if driver.find_element_by_id("check").is_enabled() else 0
    ret[2] = 1 if driver.find_element_by_id("call").is_enabled() else 0
    ret[3] = 1 if driver.find_element_by_id("minbet").is_enabled() else 0
    return ret


def play():
    p = np.load('NewFiles/test5d15.pickle',allow_pickle=True)[0]
    choices = p._rChoices
    
    driver = webdriver.Chrome(executable_path='/Users/alexpaskov/chromedriver')
    
    
    driver.get('http://www.slumbot.com/')

    try:
        prev = ''
        stacks = [20000,20000]  #slumbot, us 
        stacks,prev = oppStart(driver,stacks,prev,p,choices)
        stacks,prev = ourStart(driver,stacks,prev,p,choices)
        
        return (stacks[1]-20000,2)
    except:
        return (0,0)
    

    #driver.close()        
    
    
def oppStart(driver,stacks,prev,p,choices):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'nexthand')))
    element.click()
    
    prevActionStr = ''
    
    startWith = [stacks[0],stacks[1]]
    turn = 0 #0 if slumbot, 1 if us
    prevFeats = []
    roundBets = [50,100]
    stacks[0]-=roundBets[0]
    stacks[1]-=roundBets[1]
    handBets = [0,0]
    
    prev = waitUntilUpdate(driver, prev)
    
    c1,c2 = driver.execute_script("return ourhi;"),driver.execute_script("return ourlo;")
    hand = [strToCard(c1),strToCard(c2)]
    board=[]
    
    while True:
        prevActionStr = subtractStrs(getActionStr(driver),prevActionStr)
        s = processActionStr(prevActionStr)
        for act in s:
            if act[0]=='b':
                bet = int(act[1:])
                stacks[turn] = stacks[turn]-bet+roundBets[turn]
                roundBets[turn] = bet
                turn = int(not turn)
            elif act[0]=='k':
                turn = int(not turn)
            elif act[0]=='c':
                bet = roundBets[int(not turn)]
                stacks[turn] = stacks[turn]-bet+roundBets[turn]
                roundBets[turn] = bet
                turn = int(not turn)
            elif act[0]=='f':
                break
            else:
                handBets[0] += roundBets[0]
                handBets[1] += roundBets[1]
                roundBets = [0,0]
                turn = 1 if s[-1]=='/' else 0
                temp = driver.execute_script("return board;")
                board += processBoard(temp)
        if hasHandEnded(driver):
            break

        buttons = getActiveButtons(driver)
        
        allActs = allActions(buttons,stacks[1]//100,choices,[i//100 for i in roundBets],[i//100 for i in handBets])[1:]
        gameFeats,prevFeats = _genGameFeatures(hand,board,prevFeats,stacks[1]//100)

        allFeatures = []
        for a in allActs: allFeatures.append(gameFeats + _genActionFeatures(a,[i//100 for i in roundBets],[i//100 for i in handBets]))
        pReturn = p._reg.predict(allFeatures)
        action = allActs[np.argmax(pReturn)]
        
        if action[0]=='fold':
            driver.find_element_by_id("fold").click()
        elif action[0]=='check':
            driver.find_element_by_id("check").click()
        elif action[0]=='call':
            driver.find_element_by_id("call").click()
        else:
            amt = action[1]*100
            driver.find_element_by_id("betsize").send_keys(str(amt))
            driver.find_element_by_id("arbbet").click()
        
        prev = waitUntilUpdate(driver, prev)
        if hasHandEnded(driver):
            break
    
    winner = parseOutcome(driver)
    if winner==-1:
        move = 0
    elif winner==0:
        move = startWith[0] - (stacks[0] + sum(roundBets) + sum(handBets))
    else:
        move = (stacks[1] + sum(roundBets) + sum(handBets)) - startWith[1]
    
    return [startWith[0]-move,startWith[0]+move],prev


def ourStart(driver,stacks,prev,p,choices):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'nexthand')))
    element.click()
    
    prevActionStr = ''
    
    startWith = [stacks[0],stacks[1]]
    turn = 1 #0 if slumbot, 1 if us
    prevFeats = []
    roundBets = [100,50]
    stacks[0]-=roundBets[0]
    stacks[1]-=roundBets[1]
    handBets = [0,0]
    
    prev = waitUntilUpdate(driver, prev)
    
    c1,c2 = driver.execute_script("return ourhi;"),driver.execute_script("return ourlo;")
    hand = [strToCard(c1),strToCard(c2)]
    board=[]
    
    while True:
        prevActionStr = subtractStrs(getActionStr(driver),prevActionStr)
        s = processActionStr(prevActionStr)
        for act in s:
            if act[0]=='b':
                bet = int(act[1:])
                stacks[turn] = stacks[turn]-bet+roundBets[turn]
                roundBets[turn] = bet
                turn = int(not turn)
            elif act[0]=='k':
                turn = int(not turn)
            elif act[0]=='c':
                bet = roundBets[int(not turn)]
                stacks[turn] = stacks[turn]-bet+roundBets[turn]
                roundBets[turn] = bet
                turn = int(not turn)
            elif act[0]=='f':
                break
            else:
                handBets[0] += roundBets[0]
                handBets[1] += roundBets[1]
                roundBets = [0,0]
                turn = 1 if s[-1]=='/' else 0
                temp = driver.execute_script("return board;")
                board += processBoard(temp)
        if hasHandEnded(driver):
            break
        
        buttons = getActiveButtons(driver)
        
        allActs = allActions(buttons,stacks[1]//100,choices,[i//100 for i in roundBets],[i//100 for i in handBets])[1:]
        gameFeats,prevFeats = _genGameFeatures(hand,board,prevFeats,stacks[1]//100)
        
        allFeatures = []
        for a in allActs: allFeatures.append(gameFeats + _genActionFeatures(a,[i//100 for i in roundBets],[i//100 for i in handBets]))
        pReturn = p._reg.predict(allFeatures)
        action = allActs[np.argmax(pReturn)]
        
        if action[0]=='fold':
            driver.find_element_by_id("fold").click()
        elif action[0]=='check':
            driver.find_element_by_id("check").click()
        elif action[0]=='call':
            driver.find_element_by_id("call").click()
        else:
            amt = action[1]*100
            driver.find_element_by_id("betsize").send_keys(str(amt))
            driver.find_element_by_id("arbbet").click()
        
        prev = waitUntilUpdate(driver, prev)
        if hasHandEnded(driver):
            break
    
    winner = parseOutcome(driver)
    if winner==-1:
        move = 0
    elif winner==0:
        move = startWith[0] - (stacks[0] + sum(roundBets) + sum(handBets))
    else:
        move = (stacks[1] + sum(roundBets) + sum(handBets)) - startWith[1]
        
    
    return [startWith[0]-move,startWith[1]+move],prev    
    





numGames,change = 0,0

for i in range(300):
    c,g = play()
    numGames += g
    change += c
    print(change/numGames*100/200, (change,numGames))






