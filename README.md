Open Cricket
============
[![Build Status](https://travis-ci.org/emaillenin/open-cricket.svg?branch=master)](https://travis-ci.org/emaillenin/open-cricket)

Open access to cricket stats.

by [DuggOut.com](http://duggout.com)

Live Demo
=========

An implementation of Open Cricket is available at [http://duggout.com/open-cricket](http://duggout.com/open-cricket)

About
=====

Open Cricket aims to provide free access to all cricket statistics via API. By statistics, it includes:

 - Scorecards of concluded matches - ODI, Test & T20I
 - Ball by Ball details
 - Player profiles
 - etc.,

Apart from raw stats, you can also ask questions like

 - When was the last time India chased down 300+ in Chennai?
 - Which team has the most number of the consecutive wins this year?
 - Yuvraj's performance in world cup finals?
 - When did Shoaib Akhtar took Sachin's wicket with a golden duck?
 - How many times Brett Lee has dismissed batsmen on their 90s?
 - How many times Gilchrist has hit fours in the first ball of the over?
 - etc.,

How it works?
=============

Once a match gets over, Open Cricket starts retrieving the details of a match from cricket forums. Live matches are not supported yet.

Why?
====

With huge amount of stats being generated every day, it is becoming really difficult to unearth the awesome facts that you wanted to know.
And Wolfram Alpha does not support Cricket subject (yet)!

Contribute
==========

Setup your development machine:

 - install nltk & nltk data
 - sudo pip install Flask
 - python flaskr.py to start the server
