from app import db, game_data
from app.models import Stats


class GlobalStats():
    def __init__(self):
        pass

    def update_stats(self):
        # Update statistics - run every game/user creation
        pass

    def get_stats(self):
        # Get statistics
        pass


class UserStats():
    def __init__(self, User):
        self.user = User
        self.user_stats = User.stats

    def update_stats(self):
        # Should be called whenever there is a change in the stats - New games atm
        games = game_data.loadUser(self.user.id)['games']
        games_played = len(games)
        games_won = total_points = total_points_against = 0
        for game_id in games:
            game = game_data.loadGame(game_id)
            if int(game['winner']) == self.user.id:
                games_won += 1
            if int(game['player1']['id']) == self.user.id:
                # If player is P1
                total_points += game['player1']['score']
                total_points_against += game['player2']['score']

            if int(game['player2']['id']) == self.user.id:
                # If player is P2
                total_points += game['player2']['score']
                total_points_against += game['player1']['score']
        # compute averages
        avg_points = total_points / games_played
        avg_points_against = total_points_against / games_played

        # Save to db
        if self.user.stats:
            self.user.stats.games_played = games_played
            self.user.stats.games_won = games_won
            self.user.stats.total_points = total_points
            self.user.stats.total_points_against = total_points_against
            self.user.stats.avg_points = avg_points
            self.user.stats.avg_points_against = avg_points_against
        else:
            user_stats = Stats(
                user_id=self.user.id,
                games_played=games_played,
                games_won=games_won,
                total_points=total_points,
                total_points_against=total_points_against,
                avg_points=avg_points,
                avg_points_against=avg_points_against
            )
            db.session.add(user_stats)
        db.session.commit()
