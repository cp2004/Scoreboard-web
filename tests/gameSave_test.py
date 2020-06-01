import unittest
from app import create_app, db, game_data
from app.models import User
from appconfig import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    DATA_DIRECTORY = 'TestData'

class GameSaveCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_newUser(self):
        game_data.newUser(1)
        game_data.newUser(2)

        self.assertTrue(1 in game_data.users['users'])
        self.assertTrue(2 in game_data.users['users'])
        
    def test_game_save(self):
        game_data.newUser(1)
        game_data.newUser(2)

        game_data.saveGame(1, 1, 2, 11, 5)
        index = game_data.getIndex()
        self.assertIn(1, index['games'])

        game = game_data.loadGame(1)
        self.assertIsNotNone(game)

        fake_game = game_data.loadGame(1000)
        self.assertIsNone(fake_game)