import unittest
from app import create_app, session
from app.game.game import Game
from config import Config


class TestConfig(Config):
    TESTING = True


class GameControlCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_game_creation(self):
        newgame = Game(1, 2)
        self.assertEqual(newgame.player1.user, 1)
        self.assertEqual(newgame.player2.user, 2)
        self.assertEqual(newgame.pointsServed, 0)

    def test_serve_setting(self):
        newgame = Game(1, 2)
        newgame.setServe(newgame.player1)
        self.assertEqual(newgame.getServe(), 1)
        self.assertNotEqual(newgame.getServe(), 2)

    def test_points_adding(self):
        newgame = Game(1, 2)
        newgame.setServe(newgame.player1)

        self.add_score(newgame, newgame.player1, 5)
        self.assertEqual(newgame.getScore(newgame.player1), 5)

        self.add_score(newgame, newgame.player2, 5)
        self.assertEqual(newgame.getScore(newgame.player2), 5)

    def test_points_subtracting(self):
        newgame = Game(1, 2)
        newgame.setServe(newgame.player1)

        self.add_score(newgame, newgame.player1, 5)
        self.subtract_score(newgame, newgame.player1, 3)
        self.assertEqual(newgame.getScore(newgame.player1), 2)

        self.add_score(newgame, newgame.player2, 5)
        self.subtract_score(newgame, newgame.player2, 3)
        self.assertEqual(newgame.getScore(newgame.player2), 2)

    def test_serving_adding(self):
        newgame = Game(1, 2)
        newgame.setServe(newgame.player1)

        self.add_score(newgame, newgame.player1, 5)
        # Player1 should be serving
        self.assertEqual(newgame.getServe(), 1)

        self.add_score(newgame, newgame.player2, 5)
        # Player2 should be serving
        self.assertEqual(newgame.getServe(), 2)

    def test_serving_subtracting(self):
        newgame = Game(1, 2)
        newgame.setServe(newgame.player1)
        self.add_score(newgame, newgame.player1, 5)  # (5)-0
        self.add_score(newgame, newgame.player2, 5)  # 5-(5)

        self.subtract_score(newgame, newgame.player1, 3)  # 2-(5)
        self.assertEqual(newgame.getServe(), 2)

        self.subtract_score(newgame, newgame.player2, 3)  # (2)-2
        self.assertEqual(newgame.getServe(), 1)

    def test_tiebreak_serving(self):
        newgame = Game(1, 2)
        newgame.setServe(newgame.player1)
        self.add_score(newgame, newgame.player1, 10)  # 10-(0)
        self.add_score(newgame, newgame.player1, 10)  # (10)-10
        self.assertEqual(newgame.getServe(), 1)

        self.add_score(newgame, newgame.player1, 1)
        self.assertEqual(newgame.getServe(), 2)
        self.add_score(newgame, newgame.player1, 1)
        self.assertEqual(newgame.getServe(), 1)

        self.add_score(newgame, newgame.player1, 1)
        self.assertEqual(newgame.getServe(), 2)
        self.add_score(newgame, newgame.player1, 1)
        self.assertEqual(newgame.getServe(), 1)

    def add_score(self, game, player, points):
        count = 1
        while count <= points:
            game.Score(player)
            count += 1

    def subtract_score(self, game, player, points):
        count = 1
        while count <= points:
            game.subtract(player)
            count += 1


class GameWinCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_standard_win(self):
        game1 = Game(1, 2)
        game1.setServe(game1.player1)
        self.assertFalse(game1.getWinner())
        self.add_score(game1, game1.player1, 11)
        self.assertTrue(game1.getWinner())
        self.assertEqual(game1.getWinner(), game1.player1)

        game2 = Game(1, 2)
        game2.setServe(game2.player2)
        self.assertFalse(game2.getWinner())
        self.add_score(game2, game2.player2, 11)
        self.assertTrue(game2.getWinner())
        self.assertEqual(game2.getWinner(), game2.player2)

    def test_tiebreak_win(self):
        game1 = Game(1, 2)
        game1.setServe(game1.player1)
        self.add_score(game1, game1.player1, 10)
        self.add_score(game1, game1.player2, 11)
        self.add_score(game1, game1.player1, 1)
        self.assertFalse(game1.getWinner())

        self.add_score(game1, game1.player2, 2)
        self.assertTrue(game1.getWinner())
        self.assertEqual(game1.getWinner(), game1.player2)

    def add_score(self, game, player, points):
        count = 1
        while count <= points:
            game.Score(player)
            count += 1

    def subtract_score(self, game, player, points):
        count = 1
        while count <= points:
            game.subtract(player)
            count += 1


class SessionManagerCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_session_create(self):
        game = Game(1, 2)
        session.setSession(game)
        self.assertEqual(session.getSession(), game)

    def test_session_end(self):
        game = Game(1, 2)
        session.setSession(game)
        session.endSession()
        self.assertFalse(session.getSession())

    def test_session_id(self):
        game = Game(1, 2)
        session.setSessionId(5)
        session.setSession(game)
        self.assertEqual(session.getSessionId(), 6)
