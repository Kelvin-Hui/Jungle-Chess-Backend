from flask import Flask , jsonify ,request
from flask_cors import CORS
from flask_socketio import SocketIO,send,join_room,leave_room,emit,close_room,rooms,disconnect
import random
from board import Board,notation_index


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '1'

socketIo = SocketIO(app, cors_allowed_origins="*")


Sid_UserName = {}
Sid_roomId = {}

Rooms = {}
Game = {}


@socketIo.on("connect")
def handleconnect():
    sid = request.sid

    Sid_UserName[sid] = ''
    Sid_roomId[sid] = ''

    if len(Sid_UserName) == 11:
        disconnect()

    print(f"\n [Log] User : {sid} Connected. \n")
    print(f"\n [Active User] : {list(Sid_UserName.keys())} \n")
    
    
@socketIo.on("disconnect")
def handledisconnect():
    sid = request.sid
    
    player = Rooms.get(Sid_roomId[sid],[])
    if len(player)== 2:

        roomId = Sid_roomId[sid]
        winnermsg = "Oppoent Left! You Won!"
        socketIo.emit('infoServerMsg',winnermsg , room=roomId)
        socketIo.emit('get_log',{'logmsg': f"{Sid_UserName[sid]} left!"},room=roomId)
        socketIo.emit('get_log',{'logmsg': winnermsg},room=roomId)
        socketIo.emit('gameEnd',True,room=roomId)

        player.remove(Sid_UserName[sid])


    elif len(player)== 1:
        Rooms.pop(Sid_roomId[sid])
        Game.pop(Sid_roomId[sid])
    else:
        print(f"\n This Player Didnt Join any Room... \n")

    Sid_UserName.pop(sid)
    Sid_roomId.pop(sid)


    # close_room(sid)
    # if (len(Sid_UserName) == 0):
    #     Rooms.clear()
    #     Game.clear()
    #     for i in Rooms.keys():
    #         close_room(i)
        
    print(f"\n [Log] User : {sid} Disconnected. \n")
    print(f"\n [Log] ... Cleaning everything for this user ...")
    print(f"\n [Active User] : {list(Sid_UserName.keys())} \n")
    print(f"\n [Active Room] : {Rooms} \n")
    print(f"\n [Active Game] : {Game} \n")
   
    


@socketIo.on("create")
def handlecreate(data):
    userName = data['userName']
    sid = request.sid
    roomId = data['roomId']

    Sid_UserName[sid] = userName

    if (roomId in Rooms):
        print(f"\n [User Input Error] Room : {roomId} Already Exist \n")
        print(f"\n [User Input Error] Redirecting User to Another Room \n")
        roomId = str(random.randint(20,10000))

    Rooms[roomId] = [userName]
   

    Sid_roomId[sid] = roomId

    Game[roomId] = Board()
 
    join_room(roomId)
    print(f"\n [Log] UserName : {userName} Created Room : {roomId} \n")
    print(f"\n [Log] UserName : {userName} Joined Room : {roomId} \n")
    print(f"\n [Log] {list(Sid_UserName.items())}")
    print(f"\n [Active Room] : {Rooms} \n")
    print(f"[Active Room] : {Sid_roomId}")


    socketIo.emit('getRoomId_create', {'roomId' : roomId} , room=roomId)
    

@socketIo.on("join")
def handlejoin(data):
    userName = data['userName']
    sid = request.sid
    roomId = data['roomId']

    Sid_UserName[sid] = userName

    print(f"\n [Log] Checking Is the Room Joinable... \n")
    player = Rooms.get(roomId,[])
    if (len(player) == 2):
        print(f"\n [User Input Error] Room is Full, Cant Join! Redirecting Another Room...\n")
        roomId = str(random.randint(20,10000))
        Rooms[roomId] = [userName]
    elif (len(player) == 1):
        print(f"\n [Log] Room has spot! Joining the room! \n")
        player.append(userName)
    else:
        print(f"\n [Log] Wrong Room ID! Creating the Room instead ...\n")
        Rooms[roomId] = [userName]
        Game[roomId] = Board()

        

    Sid_roomId[sid] = roomId

    join_room(roomId)

    print(f"\n [Log] UserName : {userName} Joined Room : {roomId} \n")
    print(f"\n [Log] {list(Sid_UserName.items())}")
    print(f"\n [Active Room] : {Rooms} \n")
    print(f"[Active Room] : {Sid_roomId}")

    socketIo.emit('getRoomId_join', {'roomId' : roomId} , room=roomId)
    socketIo.emit('getOppoent', {'Oppoent': player} ,room =roomId)


@socketIo.on('leave')
def handleleave(data):
    sid = request.sid
    userName = data['userName']
    roomId = Sid_roomId[sid]
   

    leave_room(roomId)
    print(f"\n [Log] UserName : {userName} left Room : {roomId} \n")


    player = Rooms.get(roomId,[])
    if len(player)== 2:
        player.remove(Sid_UserName[sid])

        winnermsg = "Oppoent Left! You Won!"
        socketIo.emit('get_log',{'logmsg': f"{userName} left!"},room=roomId)
        socketIo.emit('get_log',{'logmsg': winnermsg},room=roomId)
        socketIo.emit('infoServerMsg',winnermsg , room=roomId)
        socketIo.emit('gameEnd',True,room=roomId)

    else:
        Rooms.pop(Sid_roomId[sid])
        Game.pop(Sid_roomId[sid])



@socketIo.on("move")
def handlemove(data):
    sid = request.sid
    
    oppoent = data['oppoent']
    turn = data['turn']
    move = data['move']
    team = data['team']
    score = data['score']
    
    
    oppoent_sid = {user:sid for sid,user in Sid_UserName.items()}[oppoent]

    player = notation_index(data['move'][0])
    target = notation_index(data['move'][1])

    roomId = Sid_roomId[sid]

    board = Game[roomId]

    logmsg = f"{Sid_UserName[sid]} : ({move[0]}) {board.getName(player[0],player[1])} => {move[1]}"
   
    if board.checkTeam(player[0],player[1],team):
        if board.move(player[0],player[1],target[0],target[1]):
            print(f"\n [Room : {roomId}][Board Movement by {Sid_UserName[sid]}] {move} Successful \n")
            print(board.display())
            socketIo.emit('update_array',{'array' : board.to2Darray()},room=roomId)
            socketIo.emit('get_log',{'logmsg': logmsg},room=roomId)
            print(f"\n [Room : {roomId}][Received Log] {logmsg} \n")
            socketIo.emit('update_turn', turn , room =oppoent_sid)
            socketIo.emit('update_turn', not turn, room = sid)
            gameover = board.checkGameover()
            if gameover[0]:
                winner = Sid_UserName[sid] if gameover[1] == team else Sid_UserName[oppoent_sid]
                winnermsg = f"{winner} Won!"
                score[gameover[1]]+=1
                updatedScore = score
                socketIo.emit('update_score',updatedScore,room = roomId)
                socketIo.emit('infoServerMsg',winnermsg , room=roomId)
                socketIo.emit('get_log',{'logmsg': winnermsg},room=roomId)
                socketIo.emit('gameEnd',True,room=roomId)
        else:
            print(f"\n [Room : {roomId}][Board Movement by {Sid_UserName[sid]}] {move} Invalid \n")
            socketIo.emit('errorServerMsg',"Invalid Move!" , room=sid)
    else:
        socketIo.emit('errorServerMsg',"Not Your Piece",room=sid)


@socketIo.on('rematch')
def handlerematch(data):
    sid = request.sid

    oppoent = data['oppoent']
    oppoent_sid = {user:sid for sid,user in Sid_UserName.items()}[oppoent]

    socketIo.emit('rematch_request',{'msg':f"{Sid_UserName[sid]} want a rematch! Agree?"},room=oppoent_sid)


@socketIo.on('response')
def handlerematchresponse(data):
    sid=request.sid
    oppoent = data['oppoent']
    oppoent_sid = {user:sid for sid,user in Sid_UserName.items()}[oppoent]
    roomId = Sid_roomId[sid]
    res = data['res']
    if (res):
        board = Game.get(roomId)
        socketIo.emit('infoServerMsg',"Resetting Everything" , room=roomId)
        board.reset()

        socketIo.emit('update_array',{'array' : board.to2Darray()},room=roomId)
        socketIo.emit('gameEnd',False,room=sid)
        socketIo.emit('gameEnd',True,room=oppoent_sid)
    else:
        socketIo.emit('infoServerMsg',f"Seem like {Sid_UserName[sid]} doesn't want a rematch" , room=oppoent_sid)


@socketIo.on("getboard")
def handlegetboard(data):
    sid = request.sid
    roomId = Sid_roomId[sid]

    board = Game.get(roomId,0)
    if (board== 0):
        print(f"\n [KeyError] Room doesn't Exist Yet!\n")
        Game[roomId] = Board()
        print(f"\n [Log] We will create it for him. \n")
        
    socketIo.emit('get_board',{'array':Game[roomId].to2Darray()},room=roomId)
    print(f"\n [Room : {roomId}][Get Board by {Sid_UserName[sid]} ]\n")
    

@socketIo.on("chat")
def handlechat(data):
    sid = request.sid

    userName = Sid_UserName[sid]
    roomId = Sid_roomId[sid]

    msg = userName +" : " +data['msg']
    print(f"\n [Room : {roomId}][Message Received From Player ({userName})] {data['msg']} \n ")
    socketIo.emit('get_msg',{'msg' : msg},room=roomId)



if __name__ == '__main__':
    socketIo.run(app,debug=True)