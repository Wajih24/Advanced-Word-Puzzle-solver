# Advanced-Word-Puzzle-solver
=> An efficient algorithm to solve word puzzles, in addition to the option to have the ability to convert a word puzzle image into a text puzzle and run the solver to solve the converted puzzle. 
## In this project we have two main parts, the first part will be the image-conversion script, and the second part will be for the solver algorithm. 
### Part 1: Convert image to text 
In previous steps, we used a custom dataset created from a set of images to train OCR models especially for our specific word case, and due to the difficulty of the input raw image can be, we came up with the idea of using multiple models to generate our final input and do some analysis for each output extracted from each model then combine the results to get the final prediction, so basically our input would be something like this :

![alt text](images/rednew.png)

and it needs to be converted into a raw_text like this : 

![alt text](images/raw_text.PNG)

### Part 2: Solving the puzzle
In both cases if you already have a text file ready to work with or use the previous part to extract the puzzle letters using OCR models we built, the next step will be setting the puzzle text file in the output folder (in case you will add it manually) otherwise it will be created automatically, the text file should be named "final.txt" otherwise you can change any name you want in the code **puzzle.py** line 117. After setting up the puzzle, now we are ready to set the words we need to search for in a text file it should be named "words.txt".
If all the requirements are ready, you are ready to run the solver but let us explain how the solver works 
