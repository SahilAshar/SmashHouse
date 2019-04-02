class Player():


    def __init__(self, username='', name='', rating=1200, matches_played=0, wins=0, losses=0):
        self.username = username
        self.name = name
        self.rating = rating
        self.matches_played = matches_played
        self.wins = wins
        self.losses = losses

    def setRating(self, newRating):
        self.rating = newRating
