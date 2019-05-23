from nltk.tree import Tree
from textblob import Word
import random


def express_player(team, player):
    player_name = player
    player_with_team = team + "'s " + player
    expressions = [player_name, player_with_team]
    return random.choice(expressions)


def express_time(time):
    return f'in the {time}th minute'


def express_action(action):
    vowels = 'a', 'o', 'e', 'i', 'u'
    article = 'an' if Word(action).startswith(vowels) else 'a'
    return f'{article} {action}'


def apply_template(team, player, minute, goal_type):
    template = Tree('', [Tree('NP', [express_player(team, player)]), Tree('VP', [
        Tree('VP', [Tree('V', ['scores']), Tree('NP', [express_action(goal_type)])]),
        Tree('PP', [express_time(minute)])])])
    return template.flatten()


if __name__ == '__main__':
    print(apply_template('Bayern', 'Lewandowski', 38, 'penalty'))
