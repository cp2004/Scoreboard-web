from app.data.data import DataManager


'''
DATA STRUCTURE
data
    --storage
        --games
            [id].json : see game save file below
        --users
            index.json : list of users (Needed? - in SQL db)
            [id].json : user with list of game ids
        index.json : List of all game ids

game save file:
[id].json
    game = {
        'id':id,
        'player1':{
            'id':player1_id,
            'score':player1_score
        },
        'player2':{
            'id':player2_id,
            'score':player2_score
        },
        'winner':None
    }

index.json
    {
        games: [ids of game]
    }
[users]index.json
    {
        users: [list of users]
    }
'''

class GameData():
    def __init__(self):
        self.data_manager = DataManager()
        if self.data_manager.file_exists('index'):
            self.index = self.data_manager.readFile('index')
        else:
            empty_index = {
                'games':[]
            }
            self.data_manager.writeFile('index', empty_index)
            self.index = empty_index

        if self.data_manager.file_exists('index', dir='users'):
            self.users = self.data_manager.readFile('index', dir='users')
        else:
            empty_users = {
                'users':[]
            }
            self.data_manager.writeFile('index', empty_users, dir='users')
            self.users = empty_users

    ###################
    ## Index methods ##
    ###################

    def getIndex(self):
        return self.index

    def getLast_Index(self):
        if self.index['games']:
            return self.index['games'][-1]
        else:
            return 0

    def addIndex(self, id_to_add):
        self.index['games'].append(id_to_add)
        self.saveIndex()
    
    def removeIndex(self, id_to_remove):
        self.index['games'].remove(id_to_remove)
        self.saveIndex()

    def saveIndex(self):
        self.data_manager.writeFile('index', self.index)

    def addIndex_user(self, id_to_add):
        self.users['users'].append(id_to_add)
        self.data_manager.writeFile('index', self.users, dir='users')

    def removeIndex_user(self, id_to_remove):
        self.users['users'].remove(id_to_remove)
        self.saveIndex()
    
    def saveIndex_users(self):
        self.data_manager.writeFile('users', self.users, dir='users')

    ##################
    ## Game methods ##
    ##################
    
    def saveGame(self, id, player1_id, player2_id, player1_score, player2_score):
        game = {
            'id':id,
            'player1':{
                'id':player1_id,
                'score':player1_score
            },
            'player2':{
                'id':player2_id,
                'score':player2_score
            },
            'winner':None
        }
        if player1_score > player2_score:
            game['winner'] = player1_id
        else:
            game['winner'] = player1_id
        self.data_manager.writeFile(id, game, dir='games')
        self.addGame_user(player1_id, id)
        self.addGame_user(player2_id, id)
        self.addIndex(id)

    def addGame_user(self, user_id, game_id):
        user = self.data_manager.readFile(user_id, dir='users')
        user['games'].append(game_id)
        self.data_manager.writeFile(user_id, user, dir='users')

    def loadGame(self, id):
        return self.data_manager.readFile(id, dir='games')
    
    def deletegame(self, id):
        game = self.loadGame(id)

        #remove game from users
        player1 = self.loadUser(game['player1']['id'])
        player1['games'].remove(id)
        self.data_manager.writeFile(player1['id'], player1, dir='users')
        player2 = self.loadUser(game['player2']['id'])
        player2['games'].remove(id)
        self.data_manager.writeFile(player2['id'], player2, dir='users')

        #remove game from index
        self.removeIndex(id)

        #remove game file
        self.data_manager.deleteFile(id, dir='games')

    ##################
    ## User methods ##
    ##################

    def newUser(self, user_id):
        user = {
            'id':user_id,
            'games':[]
        }
        self.data_manager.writeFile(user_id, user, dir='users')
        self.addIndex_user(user_id)

    def loadUser(self, id):
        return self.data_manager.readFile(id, dir='users')