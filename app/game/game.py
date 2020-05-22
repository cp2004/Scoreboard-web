#Handle scoring, winning etc. and feedback when requested
class Game():
    def __init__(self, player1, player2, firstServer=None):
        """Managing game functions for TableTennis."""
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        self.serving = firstServer
        self.pointsServed = 0
        self.winner = None
    
    def getScore(self, Player):
        return Player.score

    def Score(self, Player):
        #called on every score, arg for player
        Player.score += 1

        if self.player1.score + self.player2.score >= 20:
            #if tiebreak scoring
            self.changeServe()
            if self.player1.score - self.player2.score == 2:
                self.Win(self.player1)
            elif self.player2.score - self.player1.score == 2:
                self.Win(self.player2)

        elif Player.score == 11:
            #if won to 11
            self.Win(Player)

        else:
            #all other cases
            self.pointsServed +=1

        if self.pointsServed == 2:
            self.changeServe()

    def subtract(self, Player):
        if Player.score >=1 :
            Player.score -= 1

            if self.player1.score + self.player2.score >= 20:
                #if tiebreak scoring
                self.changeServe()
            elif self.pointsServed == 0:
                self.changeServe()
                self.pointsServed = 1
            else:
                self.pointsServed -=1

    def reset(self):
        self.winner = None
        self.player1.reset()
        self.player2.reset()
        self.serving = None
        self.pointsServed = 0

    def Win(self, Player):
        Player.wins += 1
        self.winner = Player

    def getServe(self):
        if self.serving == self.player1:
            return 1
        else:
            return 2

    def setServe(self, Player):
        if self.serving == None:
            Player.ServingFirst = True
            self.serving = Player
            self.pointsServed = 0

    def changeServe(self):
        if self.serving == self.player1:
            self.serving = self.player2
        else:
            self.serving = self.player1
        self.pointsServed = 0

    def checkStatus(self):
        #Possible statuses: Win, Reset(Serve = None)
        if self.serving == None:
            return "reset"
        elif self.winner != None:
            return "win"
        else:
            return "score"

class Player():
    def __init__(self, user):
        """Player Object."""
        self.score = 0
        self.wins = 0
        self.ServingFirst = False
        self.user = user

    def reset(self):
        self.score = 0
        self.ServingFirst = False