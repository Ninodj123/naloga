from enum import Enum


class User:
    def __init__(self, id, username, password):
        self.id  = id
        self.username = username
        self.password = password
    
    def hello(self):
        return "hello"
        
    def jsonify(self):
        return {
            "id" : self.id,
            "username" : self.username,
            "password" : self.password
            } 

class RETURN_CODE(Enum):
    LOGIN_SUCCESS = 10
    LOGIN_FAILURE = 11
    LOGIN_FAILURE_USER_LOGGED_IN = 12
    LOGOUT_SUCCESS = 20
    LOGOUT_FAILURE = 21
    REGISTER_SUCCESS = 30
    REGISTER_FAILURE = 31
    REGISTER_FAILURE_LENGTH = 32
    DELETE_SUCCESS = 40
    USER_NOT_EXIST = 50
    BOARD_FULL = 60
    GAME_DELETE_SUCCESS = 70
    NOT_OWNER = 71
    ROOM_FULL = 72
    JOIN_SUCCESS = 73
    JOIN_FAILURE = 74
    ROOM_EXIST = 75
    
class GAME_MODE(Enum):
    MODE_CLASSIC = 1
    
    