from bottle import *
from logic import *
from models import *

def __main__():

    loginManager = LoginManager()
    gameManager = GameManager()
    
    @route('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root='./static')
    
    @route('/')
    @route('/login')
    @view('login')
    def loginPage():
        if(request.get_cookie("id")):
            redirect('home')
        return dict(msg = "")
    
    @post('/')
    @post('/login')
    @view('login')
    def login():
        login = loginManager.login(request.forms.get("username"), request.forms.get("password"))
        msg = ""
        if(not login == RETURN_CODE.LOGIN_FAILURE and not login == RETURN_CODE.LOGIN_FAILURE_USER_LOGGED_IN):
            response.set_cookie("id", str(login))
            response.set_cookie("username", str(loginManager.getUserById(login).username))
            redirect('/home')
        elif(login == RETURN_CODE.LOGIN_FAILURE_USER_LOGGED_IN): msg = "User already logged in!"
        elif(login == RETURN_CODE.LOGIN_FAILURE): msg = "Invalid login info!"
        return dict(msg = msg)
        
        
            
    
    @route('/home')
    @view('home')
    def homePage():
        if(not request.get_cookie("id")):
            redirect('login')
        return dict(username = request.get_cookie("username"),
                    mode1 = gameManager.onlineClassic,
                    active1 = len(gameManager.playersClassic),
                    )
    
    @post('/home')
    @view('home')
    def postManager():
        logout = request.forms.get("logout")
        create = request.forms.get("create")
        join = request.forms.get('join')
        delete = request.forms.get('delete')
        if(logout):
            loginManager.logout(int(request.get_cookie('id')))
            response.delete_cookie("id")
            response.delete_cookie("username")
            redirect('login')
        elif(create):
            create = int(create)
            if(create == 1): gameManager.createGame(int(request.get_cookie('id')))
            redirect('home')
        elif(join):
            join = int(join)
            if(join == 1):
                gameManager.joinGame(int(request.get_cookie('id')), loginManager)
                redirect('classic')
            elif(join == 2): redirect('game4x4')
            elif(join == 3): redirect('game3x3x3')
        elif(delete):
            if(int(delete) == 1): gameManager.deleteGame(int(request.get_cookie('id')))
            redirect('home')
            
              
    @route('/register')
    @view('register')
    def registerPage():
        if(request.get_cookie("id")):
            redirect('home')
        return dict(msg = "")
    
    @post('/register')
    @view('register')
    def register():
        user = loginManager.register(request.forms.get("username"), request.forms.get("password"))
        
        if(user == RETURN_CODE.REGISTER_SUCCESS):
            redirect('/login')
        elif(user == RETURN_CODE.REGISTER_FAILURE_LENGTH):
            return dict(msg = "Field cannot be empty!")
        else:
            return dict(msg = "Username taken!")   
    
    @route('/classic')
    @view('classic')
    def pageClassic():
        if(not request.get_cookie("id")):
            redirect('login')
            
        winner = gameManager.winnerClassic
       
        return dict(username = request.get_cookie("username"), players = gameManager.playersClassic, board = gameManager.board, winner = winner)
    
    @post('/classic')
    @view('classic')
    def updateGame():
        logout = request.forms.get("logout")
        leave = request.forms.get("leave")
        tile = request.forms.get("tile")
        if(leave):
            gameManager.leaveGame(int(request.get_cookie('id')))
            redirect('home')
        if(tile):
            gameManager.checkTile(tile, int(request.get_cookie('id')))
            redirect('classic')
        if(logout):
            userId = int(request.get_cookie('id'))
            gameManager.leaveGame(userId)
            loginManager.logout(userId)
            response.delete_cookie("id")
            response.delete_cookie("username")
            redirect('login')
        
            
        
    run(host='192.168.1.31', port= 8080)
    
__main__()