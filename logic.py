from collections import namedtuple
import json
from models import *
import numpy as np

def JSONdecoder(json):
    return namedtuple('X', json.keys())(*json.values())

class LoginManager:

    def __init__(self):
        self.jsonData = open("./data/data.json", 'r+').read()
        self.users = self.readUsers()
        self.userNum = len(self.users)
        self.session = []
        
    def writeJSON(self):
        data = [user.jsonify() for user in self.users]
        open("./data/data.json", 'w').write(json.dumps(data))
        
    def readUsers(self):
        content = open("./data/data.json", 'r+').read()
        if (len(content) == 0): return []
        content = json.loads(content,  object_hook = JSONdecoder)
        return [User(user.id, user.username, user.password) for user in content]
    
    def getUserById(self, id:int):
        return [user for user in self.users if user.id == id][0]
    
    def getUserByUsername(self, username:str):
        user =  [user for user in self.users if user.username == username]
        if(user) : return user[0]
        return RETURN_CODE.USER_NOT_EXIST
    
    def login(self, username:str, password:str):
        user = self.getUserByUsername(username)
        if(not user == RETURN_CODE.USER_NOT_EXIST):
            if(user in self.session): return RETURN_CODE.LOGIN_FAILURE_USER_LOGGED_IN
            if(user.password == password):
                self.session.append(user)
                return user.id
        return RETURN_CODE.LOGIN_FAILURE
    
    def logout(self, id:int):
        user = [user for user in self.session if user.id == id][0]
        self.session.remove(user)
        
    def register(self, username:str, password:str):
        if(not len(username) > 0 or not len(password) > 0): return RETURN_CODE.REGISTER_FAILURE_LENGTH
        
        if(self.getUserByUsername(username) == RETURN_CODE.USER_NOT_EXIST):
            self.userNum += 1
            self.users.append(User(self.userNum, username, password))
            self.writeJSON()
            return RETURN_CODE.REGISTER_SUCCESS
        
        return RETURN_CODE.REGISTER_FAILURE
    
    def removeUser(self, id:int):
        user = self.getUserById(id)
        if(type(user) is User):
            for i in range(len(self.users)):
                if(user.id == self.users[i].id):
                    self.users.pop(i)
                    return RETURN_CODE.DELETE_SUCCESS
        return RETURN_CODE.USER_NOT_EXIST
        if(self.users):
            return [user.username for user in self.users]
                
    
class GameManager:
    
    def __init__(self):
        self.board = []
        self.playersClassic = []
        self.onlineClassic = False
        self.lastClassic = None
        self.winnerClassic = None
        
    def createGame(self, ownerId:int):
        self.board = np.zeros(10)
        self.board[9] = ownerId
        self.onlineClassic = True
            
    def deleteGameAsUser(self, userId:int):
        if(userId == self.board[9]):
            if(len(self.playersClassic) == 0):
                self.onlineClassic = False
                self.playersClassic = []
                self.board = []
                self.winnerClassic = None
            
    def deleteGame(self):
        if(len(self.playersClassic) == 0):
            self.onlineClassic = False
            self.playersClassic = []
            self.board = []
            self.winnerClassic = None
            
    def joinGame(self, userId:int, loginManager:LoginManager):
        self.playersClassic.append(loginManager.getUserById(userId))
        
    def leaveGame(self, userId:int):
        user = [user for user in self.playersClassic if user.id == userId][0]
        self.playersClassic.remove(user)
        if(len(self.playersClassic) == 0): self.deleteGame()

    def checkTile(self, tile:str, userId:int):
        if(self.lastClassic == None or self.lastClassic == self.playersClassic[1].id):
            if(userId == self.playersClassic[0].id):
                self.board[int(tile)] = userId
                winner = self.winCheck()
                self.lastClassic = userId
                if(winner): self.winnerClassic
        elif(self.lastClassic == self.playersClassic[0].id):
            if(userId == self.playersClassic[1].id):
                self.board[int(tile)] = userId
                winner = self.winCheck()
                self.lastClassic = userId
                if(winner):
                    self.winnerClassic = winner
        
    def winCheck(self):
        rows = self.checkRows()
        if(rows): return rows 
        cols = self.checkColumns()
        if(cols): return cols
        diags = self.checkDiagonals()
        if(diags): return diags
        return
    
    def checkRows(self):
        rows = 3
        for i in range(rows):
            p1 = True
            p2 = True
            for j in range(rows):
                if (not self.board[j + rows*i] == self.playersClassic[0].id): p1 = False
                if (not self.board[j + rows*i] == self.playersClassic[1].id): p2 = False
                if (not p1 and not p2): break
            if(p1) : return self.playersClassic[0].id
            if(p2) : return self.playersClassic[1].id
                
        return
    
    def checkColumns(self):
        cols = 3
        for i in range(cols):
            p1 = True
            p2 = True
            for j in range(cols):
                if(not self.board[j*cols + i] == self.playersClassic[0].id): p1 = False
                if(not self.board[j*cols + i] == self.playersClassic[1].id): p2 = False
                if(not p1 and not p2): break
            if(p1) : return self.playersClassic[0].id
            if(p2) : return self.playersClassic[1].id
                
        return
        
    def checkDiagonals(self):
        rows = 3
        p1 = True
        p2 = True
        for i in range(rows):
            if(not self.board[rows*(i+1)-i-1] == self.playersClassic[0].id): p1 = False
            if(not self.board[rows*(i+1)-i-1] == self.playersClassic[1].id): p2 = False
            if(not p1 and not p2): break
        if(p1) : return self.playersClassic[0].id
        if(p2) : return self.playersClassic[1].id
            
        p1 = True
        p2 = True
        for i in range(rows):
            if(not self.board[2*i*(rows-1)] == self.playersClassic[0].id): p1 = False
            if(not self.board[2*i*(rows-1)] == self.playersClassic[1].id): p2 = False
        
        if(p1) : return self.playersClassic[0].id
        if(p2) : return self.playersClassic[1].id 
          
        return
        
    def getPlayers(self):
        return self.playersClassic
    
    def getBoard(self):
        return self.board