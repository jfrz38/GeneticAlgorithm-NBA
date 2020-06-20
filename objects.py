class Player:
    def __init__(self, name: str, salary: int, adjusted_production: float, team: str, position: str, ):
        self.name = name
        self.salary = salary
        self.adjusted_production = adjusted_production
        self.team = team
        self.position = position

    def __repr__(self):
        return '{}: {} ({}) -> ${}'.format(self.position, self.name, self.team, self.salary)


class Starter:
    def __init__(self, players: [Player]):
        self.players = players

    def count(self, player: Player):
        return self.players.count(player)

    def index(self, player: Player):
        return self.players.index(player)

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        return iter(self.players)

    def __getitem__(self, item):
        return self.players[item]

    def __setitem__(self, key, value):
        self.players[key] = value

    def __repr__(self):
        str = ""
        for p in self.players:
            str+= '{}: {} ({}) -> ${}'.format(p.position, p.name, p.team, p.salary) + " ; "
        return str
