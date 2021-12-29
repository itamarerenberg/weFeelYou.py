# weFeelYou.py

Emotion detection that fits playlist accordingly {MOOD --> PLAYLIST}

ABSTRACT

our program recognize users mood and fits a playlist accordingly.

the mood recognition process is, first the user send his picture 
(our program support the operation of taking picture of himself..) 
as input, then the program run a deep neural network to extract from 
the picture a vector of emotions that the user is corrently in. 

the vector contain percentages of these emotions {happy, sad, angry, energetic, neutral, calm, focus}.

our program then implement Gradient descent algorithm to convert the general vector emotions,
to more specific vector of emotions, from 7 to 4 basic emotions {happy, sad, energetic, calm}. 

finally the program takes the final vector and using neural network it create a playlist to
the user.
