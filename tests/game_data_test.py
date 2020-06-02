import unittest
from app import create_app, db, game_data
from config import Config


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
        game_data.data_manager.remove_all(testing=True)
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_new_user(self):
        self.create_users(2)

        self.assertTrue(1 in game_data.users['users'])
        self.assertTrue(2 in game_data.users['users'])

    def test_game_save(self):
        self.create_users(2)

        game_data.saveGame(1, 1, 2, 11, 5)
        index = game_data.getIndex()
        self.assertIn(1, index['games'])

        game = game_data.loadGame(1)
        self.assertIsNotNone(game)

        fake_game = game_data.loadGame(1000)
        self.assertIsNone(fake_game)

    def test_user_index(self):
        self.create_users(2)

        u_index = game_data.users
        self.assertIn(1, u_index['users'])
        self.assertIn(2, u_index['users'])

    def test_game_winner(self):
        self.create_users(2)

        game_data.saveGame(5, 1, 2, 11, 5)
        game = game_data.loadGame(5)
        self.assertEqual(game['winner'], 1)

        game_data.saveGame(6, 1, 2, 5, 11)
        game = game_data.loadGame(6)
        self.assertEqual(game['winner'], 2)

        game_data.saveGame(7, 2, 1, 3, 11)
        game = game_data.loadGame(7)
        self.assertEqual(game['winner'], 1)

    def create_users(self, num_users):
        for user in range(1, num_users + 1):
            game_data.newUser(user)
