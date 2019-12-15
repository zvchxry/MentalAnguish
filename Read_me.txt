[TOC]

Note: for this class I had to make this in a .txt file. It looks better in a markdown app like Typora and has a table of contents which is listed above.

# Description

Welcome to Mental Anguish. This is a python program developed by Zachary Ryan for Chris Olsen's CIS 345 class. It is a gui program that quizzes users on our pre-loaded questions (I chose the solar system for the theme).

# Features

- Allows users to load questions from a JSON file
  - Can also save questions to a new JSON file
- Users can perform the following a quiz:
  - Edit questions
  - Add questions
  - Delete questions
  - Save questions 
- Users can take a premade solar system 3 question quiz

# Getting started

## Python Version

This program was written in Python 3.7.4. To check your version of python, go to the command prompt (or terminal for Mac) and type "py --version". This program is compatible with any python 3 version for Windows or Mac.

### Don't have Python?

Python is easy to install. Navigate to this link here: https://www.python.org/downloads/ and download. YouTube is a valuable resource also to use if you need more help installing this great tool.

## Running the program

Once installed, open the file and run the program in Pycharm or a similar program.

# Working in the program

## Home screen

Upon first starting the program, you will see 2 button options. 

- The left button "Quiz" will take you to the quiz interface and begin a 3 question quiz once you have loaded the JSON file into the program
- The right button "Editor" will take you into the editor that will allow you to upload your own question file, save your own questions into a file, edit existing questions, add questions, and delete them.

In addition, there is a file menu cascade. The options and explanations are as follows:

- "New File"
  - Allows user to save their own file to the program.
- "Load File"
  - Allows user to upload their own special JSON file to the program.
- "Exit"
  - This will close the program.

## Quiz screen

Here's where the action happens. You must load the questions first from the file menu and "load file" option. Once you click quiz, you get the option to start the quiz. This screen presents the user with an interface that shows them a randomized question along with 4 answer choices. It will tell the how many points they have out of the total point value of the quiz, the value of the current question, and the option to go to the next question.

The user only gets one click on a button to answer the question, so be careful. The correct answer's button will turn green, and incorrect answers will turn red. Once the quiz is finished, the user will be presented with a results pop up that shows questions, answers and score, then automatically takes them back to the main menu.

In addition, there is a file menu cascade. The options and explanations are as follows:

- "Home"
  - Takes the user back home to the "Quiz" and "Editor" buttons.
- "Exit"
  - When you're done quizzing yourself, this will close the program.

## Editor screen

Not satisfied with my great solar system questions? Here's where you get to shine. This screen allows you to either completely create your own new quiz, edit the questions for a quiz (add, delete, edit), and either save it or load in your own new one. 

Question, answer 1, answer 2, answer 3, answer 4, right feedback, wrong feedback, and points are all fields that the user can fill out or edit. Correct Answer specifies which answer is the correct option from the newly entered/edited question.  **Note:** points must be either 1-3 points, no more or no less. All fields must be filled out or an error will popup to warn the user.

Once the user is done adding a question, it is added to the list box below, and the user can scroll through the entire list and double click on it to have the questions repopulate the boxes above for editing. Have too many questions? Use the search box. It will allow you to search the questions. Once you have a potential search typed into the box to the left of the search button, click the "Search" button and your query results will appear in the list box. Once you're done, hit "Clear Search" to have all results show again.

In addition, there is a file and editor menu cascade. The options and explanations are as follows:

- File cascade:
  - "Home"
    - Takes the user back home to the "Quiz" and "Editor" buttons.
  - "Exit"
    - When you're done with the program, this will close it.
- Editor cascade:
  - "Add Question"
    - Allows user to add their newly created question into the program's list box below to be saved
    - Must be filled in before pressing
  - "Save Question"
    - Allows user to save their newly created question into a JSON file
    - Must be filled in before pressing 
  - "Delete Question"
    - Allows user to delete a question that is highlighted in the list box
  - "New File"
    - Allows user to load new file
  - "Load File"
    - Allows user to load a new file also
  - "Save File"
    - Saves current editor questions into a new JSON file