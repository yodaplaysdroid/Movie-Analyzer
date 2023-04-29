# Movie Recommender System for MovieLens25M Dataset
School Project : Simple Movie Recommender System using Correlation 


### 1 Requirements
1. According to the given dataset, design a rating-based movie recommender system. 
2. For the given users' attributes, design a movie recommender system that predict users' favorite.


### 2 Dataset Source
MovieLens25M Dataset URL : https://grouplens.org/datasets/movielens/25m/ 
+ After downloaded, Dataset is then extracted to a relative directory 'raw'


### 3 Dependencies
- OS : Linux Kernel 5.15
- Python 3.11
- Pandas 2.0


### 4 Contents

##### i. Folder : data
Contains search history to speed up future queries that searches for the same keyword.

##### ii. Python File : Init.py
Creates separate files for all different genome tags to reduce operation time when working with genome tags score.

##### iii. Python File : Recommender.py
Contains all rating-based recommendation methods and some basic utility functions.

##### iv. Python File : User.py
User Class definition.

##### v. Python File : main.py
Main Console-based program for the whole recommender system.
