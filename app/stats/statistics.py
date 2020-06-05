from collections import Counter
from app import db, game_data
from app.models import Stats


class UserStats():
    def __init__(self, User):
        self.user = User
        self.user_stats = User.stats

    def update_stats(self):
        # Should be called whenever there is a change in the stats - New games atm
        games = game_data.loadUser(self.user.id)['games']
        games_played = len(games)
        games_won = total_points = total_points_against = 0
        users_played = []
        for game_id in games:
            game = game_data.loadGame(game_id)
            if int(game['winner']) == self.user.id:
                games_won += 1
            if int(game['player1']['id']) == self.user.id:
                # If player is P1
                total_points += game['player1']['score']
                total_points_against += game['player2']['score']
                users_played.append(int(game['player2']['id']))

            if int(game['player2']['id']) == self.user.id:
                # If player is P2
                total_points += game['player2']['score']
                total_points_against += game['player1']['score']
                users_played.append(int(game['player1']['id']))

        counted = Counter(users_played).most_common(1)
        if counted:
            most_played, games_against_most_played = counted[0]
        else:
            most_played = None
            games_against_most_played = 0

        # compute averages
        if games_played:  # Don't compute if no games (ZeroDivisionError)
            avg_points = round(total_points / games_played, 1)
            avg_points_against = round(total_points_against / games_played, 1)
            win_ratio = round(games_won / games_played, 2)
        else:
            avg_points = avg_points_against = win_ratio = 0

        # Save to db
        if self.user.stats:
            self.user.stats.games_played = games_played
            self.user.stats.games_won = games_won
            self.user.stats.total_points = total_points
            self.user.stats.total_points_against = total_points_against
            self.user.stats.avg_points = avg_points
            self.user.stats.avg_points_against = avg_points_against
            self.user.stats.most_played = most_played
            self.user.stats.games_against_most_played = games_against_most_played
            self.user.stats.win_ratio = win_ratio
        else:
            user_stats = Stats(
                user_id=self.user.id,
                games_played=games_played,
                games_won=games_won,
                total_points=total_points,
                total_points_against=total_points_against,
                avg_points=avg_points,
                avg_points_against=avg_points_against,
                most_played=most_played,
                games_against_most_played=games_against_most_played,
                win_ratio=win_ratio
            )
            db.session.add(user_stats)
        db.session.commit()
