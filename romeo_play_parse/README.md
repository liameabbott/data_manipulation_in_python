# si601_romeo_play_parse
XML parsing assignment for SI 601, Data Manipulation course with Professor Yuhang Wang at the University of Michigan, Winter 2015

See Part 1 in 'SI_601_W15_Homework3.pdf' file for full assignment description.

The short 'si601_romeo_play_parse.py' Python script reads in the Shakespeare play 'Romeo & Juliet' in XML format, extracs the Scene,Act,Line numbers from the play (Scene 1, Act 1, Line 1 is '1.1.1' for example), and then pairs that line with the associated typographic line (for example, 'ftln-0015' is the typographic line associated with Scene 1, Act 1, Line 1). 

The script then writes a tab-delimited text file (si601_romeo_play_parse.txt) listing the line pairs.

To read and parse the XML file, the script utilizes the ElementTree package in Python.
