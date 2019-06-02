from nltk.tree import Tree
from textblob import Word
import random
import pandas as pd


class Data2Language:

    def __init__(self):
        self.player_stats = pd.read_csv('../dataset/players.csv', sep=';')
        self.action_dictionaries = {
            'goal': ['scores', 'hits'],
			'save': ['save', 'defend'],
			'faul': ['gets'],
            'penalty': ['gets', 'receives', 'is shown', 'is punished with'],
            'substitution': ['leaves the game', 'leaves playing field', 'walks off the pitch', 'is substituted'],
            'injury': ['is injured', 'gets hurt', 'gets injured'],
            'pick': ['picks up the ball', 'taking over the ball'],
            'pass': ['gets upright pass', 'gets serving on the curb'],
            'loss': ['did not stay on the ball for a long time', 'quickly losses the ball', 'stopped by an opponent']
        }
        self.vowels = 'a', 'o', 'e', 'i', 'u'
        self.trivia_starter = ["Did you know?", "It is interesting that", "Trivia:", ""]
        self.player_features = ["Age", "Club", "Overall", "Value", "Wage", "Preferred Foot",
                                "Contract Valid Until", "Height", "Weight", "Release Clause"]
        self.good_adjectives = ["beautiful", "wonderful", "awesome", "terrific", "fantastic", "perfect"]
        self.shot_adjectives = ["powerful", "strong", "terrific", "beautiful", "tremendous", "mighty", "what a", "precise", "unbelievable"]
        self.bad_adjectives = ["terrible", "bad", "desperate", "hopeless", "poor", "weak"]

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
        return f'{time}th minute:'

    def express_adjective(self, mood):
        if mood is "bad":
            return random.choice(self.bad_adjectives)
        elif mood is "shot":
            return random.choice(self.shot_adjectives) + " shot!"
        elif mood is "pick":
            return random.choice(self.good_adjectives) + random.choice([" acquisition", " overtaking"])
        else:
            return random.choice(self.good_adjectives)

    def express_action(self, action, action_type):
        verbs = self.action_dictionaries.get(action)
        if action_type is not None and action is "goal":
            adj = self.express_adjective("shot")
            expressions = [f'{verb} {self.get_article(action)} {action} - {action_type} -, {adj}' for verb in verbs]
            [expressions.append(f'{verb} {self.get_article(action_type)} {action_type}') for verb in verbs]
        elif action_type is not None and action is not "goal":
            expressions = [f'{verb} {self.get_article(action)} {action} - {action_type} -' for verb in verbs]
            [expressions.append(f'{verb} {self.get_article(action_type)} {action_type}') for verb in verbs]
        elif action_type is None and action is "pick":
            adj = self.express_adjective("pick")
            expressions = [f'{verb}, {adj}' for verb in verbs]
        elif action_type is None and action is "save":
            adj = self.express_adjective("good")
            expressions = [f'{adj} {verb}' for verb in verbs]
        else:
            expressions = [f'{verb}' for verb in verbs]

        return random.choice(expressions)

    def apply_template(self, team, player, minute, action, action_type):
        template = Tree('', [Tree('PP', [self.express_time(minute)]), Tree('NP', [
            Tree('NP', [self.express_player(team, player)]),
            Tree('VP', [self.express_action(action,action_type)])])])
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
    print(d2l.apply_template(team='Real', player='Kroos', minute=15, action='pick', action_type=None))
    print(d2l.apply_template(team='Barcelona', player='Messi', minute=22, action='substitution', action_type=None))
    print(d2l.apply_template(team='Barcelona', player='Coutinho', minute=28, action='loss', action_type=None))
    print(d2l.apply_template(team='Real', player='Bale', minute=73, action='injury', action_type=None))
    print(d2l.apply_template(team='Real', player='Navas', minute=88, action='save', action_type=None))
    print(d2l.apply_template(team='Real', player='Ramos', minute=89, action='pick', action_type=None))
    print(d2l.generate_trivia(player="Lewandowski", team="Bayern"))
