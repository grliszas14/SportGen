from nltk.tree import Tree
from textblob import Word
import random
import pandas as pd


class Data2Language:

    def __init__(self):
        self.player_stats = pd.read_csv('../dataset/players.csv', sep=';')
        self.action_dictionaries = {
            'goal': ['scores', 'hits'],
			'save': ['saves', 'defends'],
			'faul': ['gets'],
            'penalty': ['gets', 'receives', 'is shown', 'is punished with'],
            'substitution': ['leaves the game', 'leaves', 'walks off the pitch', 'is substituted'],
            'injury': ['is injured', 'gets hurt', 'gets injured']
        }
        self.vowels = 'a', 'o', 'e', 'i', 'u'
        self.trivia_starter = ["Did you know?", "It is interesting that", "Trivia:", ""]
        self.player_features = ["Age", "Club", "Overall", "Value", "Wage", "Preferred Foot",
                                "Contract Valid Until", "Height", "Weight", "Release Clause"]

    def get_article(self, word):
        return 'an' if Word(word).startswith(self.vowels) else 'a'

    def express_player(self, team, player):
        player_data = self.player_stats[(self.player_stats["Name"].str.contains(player, case=False)) & (
            self.player_stats["Club"].str.contains(team, case=False))]
        player_with_team = f"{team}'s {player}"
        players_age = player_data["Age"].to_string(header=False, index=False).strip()
        player_with_age = f"{player}, {players_age} y.o.,"
        jersey_number = player_data["Jersey Number"].to_string(header=False, index=False,
                                                               float_format=lambda no: "{:10.0f}".format(no)).strip()
        player_with_jersey_number = f"{player} wearing number {jersey_number}"
        nationality = player_data["Nationality"].to_string(header=False, index=False).strip()
        player_with_nationality = f"{player} from {nationality}"
        expressions = [player, player_with_team, player_with_age, player_with_jersey_number, player_with_nationality]
        return random.choice(expressions)

    def express_time(self, time):
        return f'in the {time}th minute'

    def express_action(self, action, action_type):
        verbs = self.action_dictionaries.get(action)
        if action_type is not None:
            expressions = [f'{verb} {self.get_article(action)} {action} ({action_type})' for verb in verbs]
            [expressions.append(f'{verb} {self.get_article(action_type)} {action_type}') for verb in verbs]
        else:
            expressions = [f'{verb}' for verb in verbs]

        return random.choice(expressions)

    def apply_template(self, team, player, minute, action, action_type):
        template = Tree('', [Tree('NP', [self.express_player(team, player)]), Tree('VP', [
            Tree('VP', [self.express_action(action, action_type)]),
            Tree('PP', [self.express_time(minute)])])])
        return template.flatten().pformat().lstrip('(').rstrip(')')

    def generate_trivia(self, player, team):
        player_data = self.player_stats[(self.player_stats["Name"].str.contains(player, case=False)) & (
            self.player_stats["Club"].str.contains(team, case=False))]
        feature_name = random.choice(self.player_features)
        feature = player_data[feature_name].to_string(header=False, index=False).strip()
        template = Tree('', [Tree('NP', [Tree('N', [f"{player}'s"]), Tree('N', [feature_name.lower()])]),
                             Tree('VP', [Tree('V', ['is']), Tree('NP', [Tree('NP', [feature])])])]).flatten()
        return f"{random.choice(self.trivia_starter)} {template.pformat().lstrip('(').rstrip(')')}"


if __name__ == '__main__':
    d2l = Data2Language()
    print(d2l.apply_template(team='Bayern', player='Lewandowski', minute=38, action='goal',
                             action_type='penalty kick'))
    print(d2l.apply_template(team='United', player='Pogba', minute=10, action='penalty', action_type='yellow card'))
    print(d2l.apply_template(team='Barcelona', player='Messi', minute=89, action='substitution', action_type=None))
    print(d2l.apply_template(team='Real', player='Bale', minute=73, action='injury', action_type=None))
    print(d2l.generate_trivia(player="Lewandowski", team="Bayern"))
