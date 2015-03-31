Productions

# Why custom productions when nltk generate will do the job?

 - There are few custom tasks done here - like ignore same syntax in a different order, limiting the usual expansion for only 2 permutations, using only one of the word_ option if it has multiple possible values
 
# Notes
 - For static word expansions, use word_* (eg. word_this_last -> 'this' | 'last')
 - For reference expansions, use a matching file name from expansions path (eg. team, match_type)
 - For others (dynamic expansions), do not use root, keys with numbers, keys matching expansion file name, starting with word_ 
 - For dynamic expansion, team_A can pick the expansions from file team.txt. Splits on underscore (except for word_)
 - Dynamic expansion will expand up-to 1 level. So dynamic expansion should resolve to a word or an expansion file, not to another dynamic expansion 