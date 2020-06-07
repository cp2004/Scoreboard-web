from app.data.data import DataManager


"""
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
[users]id.json
    {
        games = [ids of games user is in]
    }
index.json
    {
        games: [ids of game]
    }
[users]index.json
    {
        users: [list of users]
    }
"""


class GameData():
    """Managing game saving and indexing"""

    def __init__(self, app=None):
        """Initialise

        Args:
            app (Flask, optional): Passed to DataManager for config. Defaults to None.
        """
        if app:
            self.data_manager = DataManager(app)
            self.checkIndex()

    def init_app(self, app):
        """
        Add app instance and generate manager. Must have a datamanger for rest of functions.

        Args:
            app ([type]): [description]
        """
        self.data_manager = DataManager(app)
        self.checkIndex()

    def checkIndex(self):
        """Checks if indexes exist, if not create them."""

        if self.data_manager.file_exists('index'):
            self.index = self.data_manager.readFile('index')
        else:
            empty_index = {
                'games': []
            }
            self.data_manager.writeFile('index', empty_index)
            self.index = empty_index

        if self.data_manager.file_exists('index', dir='users'):
            self.users = self.data_manager.readFile('index', dir='users')
        else:
            empty_users = {
                'users': []
            }
            self.data_manager.writeFile('index', empty_users, dir='users')
            self.users = empty_users

    #################
    # Index methods #
    #################

    def getIndex(self):
        """
        Method to return game index

        Returns:
            dict: Index of all games
        """
        return self.index

    def getLast_Index(self):
        """
        Find last index in dict

        Returns:
            str: id of last game
        """
        if self.index['games']:
            return self.index['games'][-1]
        else:
            return 0

    def addIndex(self, id_to_add):
        """
        Add an id to the index

        Args:
            id_to_add (int/str): Id to add to the list
        """
        self.index['games'].append(id_to_add)
        self.saveIndex()

    def removeIndex(self, id_to_remove):
        """
        Remove an id from the index

        Args:
            id_to_remove (int/str): Id to remove from list
        """
        self.index['games'].remove(int(id_to_remove))
        self.saveIndex()

    def saveIndex(self):
        """Save index to disk"""
        self.data_manager.writeFile('index', self.index)

    def addIndex_user(self, id_to_add):
        """
        Add a user to the index

        Args:
            id_to_add (int/str): Id to add to users index
        """
        self.users['users'].append(id_to_add)
        self.data_manager.writeFile('index', self.users, dir='users')

    def removeIndex_user(self, id_to_remove):
        """
        Remove a user from index

        Args:
            id_to_remove (int/str): Id to remove from users index
        """
        self.users['users'].remove(int(id_to_remove))
        self.saveIndex()

    def saveIndex_users(self):
        """Write users index to file"""
        self.data_manager.writeFile('users', self.users, dir='users')

    ################
    # Game methods #
    ################

    def saveGame(self, id, player1_id, player2_id, player1_score, player2_score):
        """
        Save a game to disk

        Args:
            id (int): id of game
            player1_id (int): Id of player 1
            player2_id (int): Id of player 2
            player1_score (int): Score of player 1
            player2_score (int): Score of player 2
        """
        game = {
            'id': id,
            'player1': {
                'id': player1_id,
                'score': player1_score
            },
            'player2': {
                'id': player2_id,
                'score': player2_score
            },
            'winner': None
        }
        if player1_score > player2_score:
            game['winner'] = player1_id
        else:
            game['winner'] = player2_id
        self.data_manager.writeFile(id, game, dir='games')
        self.addGame_user(player1_id, id)
        self.addGame_user(player2_id, id)
        self.addIndex(id)

    def addGame_user(self, user_id, game_id):
        """
        Add game to user's file

        Args:
            user_id (int): Id of user
            game_id (int): Id of game to add
        """
        user = self.data_manager.readFile(user_id, dir='users')
        user['games'].append(game_id)
        self.data_manager.writeFile(user_id, user, dir='users')

    def loadGame(self, id):
        """
        Load a game from the disk

        Args:
            id (int): Id of game to load

        Returns:
            dict: Data of game (Score, players, winner)
        """
        return self.data_manager.readFile(id, dir='games')

    def deletegame(self, id):
        """
        Removes a game from disk, and indexes

        Args:
            id (int): Id of game to remove
        """
        game = self.loadGame(id)

        # remove game from users
        player1 = self.loadUser(game['player1']['id'])
        player1['games'].remove(int(id))
        self.data_manager.writeFile(player1['id'], player1, dir='users')
        player2 = self.loadUser(game['player2']['id'])
        player2['games'].remove(int(id))
        self.data_manager.writeFile(player2['id'], player2, dir='users')

        # remove game from index
        self.removeIndex(id)

        # remove game file
        self.data_manager.deleteFile(id, dir='games')

    ################
    # User methods #
    ################

    def newUser(self, user_id):
        """
        Add a new user to the index

        Args:
            user_id (int): Id of user (Should link with sql db)
        """
        user = {
            'id': user_id,
            'games': []
        }
        self.data_manager.writeFile(user_id, user, dir='users')
        self.addIndex_user(user_id)

    def loadUser(self, id):
        """
        Loads a users file from disk

        Args:
            id (int): Id of user

        Returns:
            dict: data of user
        """
        return self.data_manager.readFile(id, dir='users')
