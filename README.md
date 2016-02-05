# NLP-Assignments

Weekly programming assignment for NLP (CSCI-544)

##Assignment 1 - Part 1
A Python program which will take a string as the first parameter, and write an output file called anagram_out.txt which contains of all the anagrams (permutations) of the string, one per line, sorted alphabetically.

###Input : A String
###Output : All permutation of the string sorted alphabetically

###How to run:
> python anagram.py 'string'

##Assignment 1 - Part 2
A Python program which will take a path to an input file (absolute path name) as the first parameter. It will read the file as a binary file, and assume that it contains characters from Unicode's Basic Multilingual Plane (U+0000 to U+FFFF) in UTF-16 encoding (big endian), that is every 2 bytes correspond to one character and directly encode that character's Unicode code point. The program will encode each character in UTF-8 (between 1 and 3 bytes), and write the encoded bytes to a file called utf8encoder_out.txt.

###Input and Output
Attached sample files.

###How to run:
> python utf8encoder.py /path/to/input

##Assignment 2
A naive Bayes classifier to identify hotel reviews as either truthful or deceptive, and either positive or negative.
