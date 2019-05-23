from nltk.tree import Tree
from textblob import Word
import random
import pandas as pd


class Data2Language:

    def __init__(self):
        self.player_stats = pd.read_csv('../dataset/players.csv', sep=';')

    def express_player(self, team, player):
        player_name = player
        player_with_team = f"{team}'s {player}"
        # players_age = self.player_stats.query(f'Age.str.contains({player})', engine='python')
        # player_with_age = f"{player}, {players_age},"
        expressions = [player_name, player_with_team]
        return random.choice(expressions)

    def express_time(self, time):
        return f'in the {time}th minute'

    def express_action(self, action):
        vowels = 'a', 'o', 'e', 'i', 'u'
        article = 'an' if Word(action).startswith(vowels) else 'a'
        return f'{article} {action}'

    def apply_template(self, team, player, minute, goal_type):
        template = Tree('', [Tree('NP', [self.express_player(team, player)]), Tree('VP', [
            Tree('VP', [Tree('V', ['scores']), Tree('NP', [self.express_action(goal_type)])]),
            Tree('PP', [self.express_time(minute)])])])
        return template.flatten()


if __name__ == '__main__':
    d2l = Data2Language()
    print(d2l.apply_template(team='Bayern', player='Lewandowski', minute=38, goal_type='penalty'))
