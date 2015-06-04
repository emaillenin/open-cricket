def join_for_config(words):
    return ' "' + '" | "'.join(words) + '" '


def split_and_form_list(source):
    return list(set(sum([s.split() for s in source], [])))

ignore_title_case_words = {'odi', 't20', 'test', 't20i', 'ipl'}
match_type_list = ['test', 'odi', 't20i', 't20']
expandable_filters = ['match_type', 'series', 'year', 'ground']
expandable_filters_in = list('word_in ' + e for e in expandable_filters)
metric_list = join_for_config(
    ['fifties', 'sixes', 'fours', '100s', '50s', '30s', 'hundreds', 'centuries', 'matches', 'innings', 'runs',
     'wickets', 'not', 'outs', 'high', 'individual', 'score', 'balls', 'faced', 'minutes', 'strike', 'rate',
     'average', 'thirties', 'bowled', 'maiden', 'over', 'overs', 'conceded', 'best', 'bowling', 'figure',
     'catches', 'stumpings', 'economy', 'five', 'wicket', 'haul', 'ten'])
series_list = join_for_config(
    ['ipl', 'indian', 'premier', 'league', 'champions', 'league', 'world', 'cup', 'clt20',
     't20', 'trophy', 'icc', 'twenty20'])
team_names_list = ['india', 'pakistan', 'australia', 'england', 'zimbabwe', 'bangladesh', 'afghanistan', 'kenya',
                   'ireland', 'netherlands', 'scotland', 'canada', 'bermuda', 'namibia', 'usa', 'chennai super kings',
                   'csk', 'royal challengers bangalore', 'rcb', 'rajastan royals', 'rr', 'sunrisers hyderabad', 'srh',
                   'mumbai indians', 'mi', 'kings xi punjab', 'kxip', 'kolkata knight riders', 'kkr', 'pune warriors',
                   'pwi', 'delhi daredevils', 'dd', 'new zealand', 'nz', 'south africa', 'sa', 'sri lanka', 'sl',
                   'west indies',
                   'wi', 'uae', 'east africa', 'hong kong']
team_player_list = team_names_list + ['indian', 'australian', 'kenyan', 'canadian', 'namibian', 'african',
                                      'lankan', 'pakistani']
team_list = join_for_config(split_and_form_list(team_names_list))
team_player_list = join_for_config(split_and_form_list(team_player_list))

match_clauses = {
    'clause_result_by_team': ['word_won_lost word_by team',
                              'word_played word_by team',
                              'word_played word_by team_A word_and team_B',
                              'word_won_lost word_by team_A word_against team_B'],
    'clause_batting_order': 'word_batting word_batting_order',
    'clause_innings_score': 'word_scoring innings_score',
    'clause_chasing_score': 'word_chasing target',
    'clause_wickets_left': 'word_with wickets word_wickets word_left'
}

expandable_match_clauses = list(match_clauses.keys())

# TODO A dynamic generator for 'word' helpers

cfg_helpers = {
    'word_in': "word_in -> 'in'",
    'word_a': "word_a -> 'a'",
    'word_team': "word_team -> 'team'",
    'word_won': "word_won -> 'won'",
    'word_against': "word_against -> 'against'",
    'word_left': "word_left -> 'left'",
    'word_wickets': "word_wickets -> 'wickets'",
    'word_with': "word_with -> 'with'",
    'word_won_lost': "word_won_lost -> 'won' | 'lost'",
    'word_lost': "word_lost -> 'lost'",
    'word_by': "word_by -> 'by'",
    'word_chasing': "word_chasing -> 'chasing'",
    'word_played': "word_played -> 'played'",
    'word_captain': "word_captain -> 'captain'",
    'word_scoring': "word_scoring -> 'scoring'",
    'innings_score': "innings_score -> nlp_number",
    'target': "target -> nlp_number",
    'wickets': "wickets -> nlp_number",
    'word_has': "word_has -> 'has'",
    'word_between': "word_between -> 'between'",
    'word_batting': "word_batting -> 'batting'",
    'word_batting_order': "word_batting_order -> '1st' | 'first' | '2nd' | 'second' | '3rd' | 'third' | '4th' | 'fourth'",
    'word_articles': "word_articles -> 'a' | 'an' | 'the'",
    'word_this_last': "word_this_last -> 'this' | 'last'",
    'word_year': "word_year -> 'year'",
    'word_as': "word_as -> 'as'",
    'word_extent': "word_extent -> 'highest' | 'lowest' | 'recent'",
    'word_and': "word_and -> 'and'",
    'word_wkt_order': "word_wkt_order -> '1st'| '2nd'| '3rd'| '4th'| '5th'| '6th'| '7th'| '8th'| '9th'| '10th'",
    'dismissals': "dismissals -> 'bowled' | 'caught' | 'lbw' | 'run out' | 'stumping' | 'hit_wicket'",
    'team': """
            team -> team1 team2 team3
            team -> team1 team2
            team -> team1
            team1 -> """ + team_list + """
            team2 -> """ + team_list + """
            team3 -> """ + team_list + """
            """,
    'teamplayer': """
            teamplayer -> team_player1 team_player2 team_player3
            teamplayer -> team_player1 team_player2
            teamplayer -> team_player1
            team_player1 -> """ + team_player_list + """
            team_player2 -> """ + team_player_list + """
            team_player3 -> """ + team_player_list + """
            """,
    'series': """
            series -> series1 series2 series3
            series -> series1 series2
            series -> series1
            series1 -> """ + series_list + """
            series2 -> """ + series_list + """
            series3 -> """ + series_list + """
            """,
    'metric': """
            metric -> metric1 metric2 metric3
            metric -> metric1 metric2
            metric -> metric1
            metric1 -> """ + metric_list + """
            metric2 -> """ + metric_list + """
            metric3 -> """ + metric_list + """
            """,
    'in_match_type': """
            match_type -> %s
            """ % join_for_config(match_type_list),
    'last_time': """
            last_time -> word_when word_was word_the word_last word_time
            word_when -> 'when'
            word_was -> 'was'
            word_the -> 'the'
            word_last -> 'last'
            word_time -> 'time'
            """,
    'how_many_times': """
            how_many_times -> word_how word_many word_times
            word_how -> 'how'
            word_many -> 'many'
            word_times -> 'times'
            """
}


def empty_pos(pos, tag):
    return len([p[0] for p in pos if p[1] == tag]) == 0

def extract_words_with_tag(pos, tag):
    return [p[0] for p in pos if p[1] == tag]
