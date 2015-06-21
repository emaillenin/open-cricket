def join_for_config(words):
    return ' "' + '" | "'.join(words) + '" '

def join_for_pipe_config(words):
    return ' | '.join(words)

def split_and_form_list(source):
    return list(set(sum([s.split() for s in source], [])))

def form_multi_word_config(words_list):
    return list("'" + "' '".join(w.split()) + "'" for w in words_list)

ignore_title_case_words = {'odi', 't20', 'test', 't20i', 'ipl'}
match_type_list = join_for_pipe_config(form_multi_word_config(['test', 'odi', 't20i', 't20']))
expandable_filters = ['match_type', 'series', 'year', 'ground']
expandable_filters_in = list('word_in ' + e for e in expandable_filters)
metric_list = join_for_pipe_config(form_multi_word_config(
    ['fifties', 'sixes', 'fours', '100s', '50s', '30s', 'hundreds', 'centuries', 'matches', 'innings', 'runs',
     'wickets', 'not outs', 'individual score', 'balls faced', 'minutes', 'strike rate', 'bowling strike rate',
     'average', 'thirties', 'balls bowled', 'maiden overs', 'runs conceded', 'bowling figure', 'bowling average',
     'catches', 'stumpings', 'economy rate', 'five wicket haul', 'ten wicket haul', 'nineties', 'ducks',
     'man of the match']))
series_list = join_for_pipe_config(form_multi_word_config(
    ['ipl', 'world cup', 'clt20']))
team_names_list = ['india', 'pakistan', 'australia', 'england', 'zimbabwe', 'bangladesh', 'afghanistan', 'kenya',
                   'ireland', 'netherlands', 'scotland', 'canada', 'bermuda', 'namibia', 'usa', 'chennai super kings',
                   'csk', 'royal challengers bangalore', 'rcb', 'rajastan royals', 'rr', 'sunrisers hyderabad', 'srh',
                   'mumbai indians', 'mi', 'kings xi punjab', 'kxip', 'kolkata knight riders', 'kkr', 'pune warriors',
                   'pwi', 'delhi daredevils', 'dd', 'new zealand', 'nz', 'south africa', 'sa', 'sri lanka', 'sl',
                   'west indies',
                   'wi', 'uae', 'east africa', 'hong kong']
team_player_list = team_names_list + ['indian', 'australian', 'kenyan', 'canadian', 'namibian', 'south african',
                                      'sri lankan', 'pakistani']
team_list = join_for_pipe_config(form_multi_word_config(team_names_list))
team_player_config_list = join_for_pipe_config(form_multi_word_config(team_player_list))

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
    'word_single': "word_single -> 'single'",
    'word_innings': "word_innings -> 'innings'",
    'word_match': "word_match -> 'match'",
    'word_series': "word_series -> 'series'",
    'word_ground': "word_ground -> 'ground'",
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
            team -> """ + team_list + """
            """,
    'teamplayer': """
            teamplayer -> """ + team_player_config_list + """
            """,
    'series': """
            series -> """ + series_list + """
            """,
    'metric': """
            metric -> """ + metric_list + """
            """,
    'in_match_type': """
            match_type -> %s
            """ % match_type_list,
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
