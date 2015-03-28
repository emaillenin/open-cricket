Productions

 - For static word expansions, use word_* (eg. word_this_last -> 'this' | 'last')
 - For reference expansions, use a matching file name from expansions path (eg. team, match_type)
 - For others (dynamic expansions), do not use root, keys with numbers, keys matching expansion file name, starting with word_ 
 - For dynamic expansion, team_A can pick the expansions from file team.txt. Splits on underscore (except for word_)