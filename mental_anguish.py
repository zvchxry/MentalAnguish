# Zachary Ryan, CIS 345 Olsen 10:30-11:45 Project

from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import ttk
import json
from difflib import get_close_matches
from tkinter import messagebox
import random

# button color
btn_bg = "#DEDEFF"

# creates tkinter window
window = Tk()
window.title("Mental Anguish")

widgets = {}
# creates font size for program
btn_font = tkFont.Font(family='Ariel', size=20, weight='bold')


class Question:
    """This allows the user's input to be stored in our question class"""

    def __init__(self):
        self.__question = ''
        self.__points = 0
        self.__answer_index = 0
        self.__feedback = {True: '', False: ''}
        self.__answers = ['', '', '', '']

    # getting and setting everything within the class
    def get_answer_index(self):
        return self.__answer_index

    def set_answer_index(self, answer_index):
        if type(answer_index) == int:
            # answer index has to be within 1-4
            if answer_index >= 0 and answer_index <= 3:
                self.__answer_index = answer_index
            else:
                raise ValueError(f'{answer_index} invalid, 0 <= answer_index <= 3')
        else:
            raise TypeError("answer index must be type int")

    answer_index = property(get_answer_index, set_answer_index)

    def get_correct_feedback(self):
        return self.__feedback[True]

    def set_correct_feedback(self, correct_feedback):
        if type(correct_feedback) == str:
            # makes sure feedback isn't blank
            if len(correct_feedback.strip()) > 0:
                self.__feedback[True] = correct_feedback
            else:
                raise ValueError("please enter correct feedback")
        else:
            raise TypeError("correct feedback must be type str")

    correct_feedback = property(get_correct_feedback, set_correct_feedback)

    def get_incorrect_feedback(self):
        return self.__feedback[False]

    def set_incorrect_feedback(self, incorrect_feedback):
        if type(incorrect_feedback) == str:
            # makes sure feedback isn't blank
            if len(incorrect_feedback.strip()) > 0:
                self.__feedback[False] = incorrect_feedback
            else:
                raise ValueError("please enter incorrect feedback")
        else:
            raise TypeError("Incorrect feedback must be type str")

    incorrect_feedback = property(get_incorrect_feedback, set_incorrect_feedback)

    def get_answers(self):
        return self.__answers

    def set_answers(self, answers):
        if type(answers) == list:
            # checks if 4 answers
            if len(answers) == 4:
                # loops through 4 answers and makes sure none are blank
                for answer in answers:
                    if len(answer.strip()) == 0:
                        raise ValueError("Answers cannot be blank")
                self.__answers = answers
            else:
                raise ValueError('There must be 4 answers')
        else:
            raise TypeError("Please provide a list of 4 answers")

    answers = property(get_answers, set_answers)

    def get_question(self):
        return self.__question

    def set_question(self, question):
        if type(question) == str:
            # makes sure no blank questions
            if len(question.strip()) > 0:
                self.__question = question
            else:
                raise ValueError("please enter a question")
        else:
            raise TypeError('Questions must be a string')

    question = property(get_question, set_question)

    def get_points(self):
        return self.__points

    def set_points(self, points):
        if type(points) == int:
            # makes sure points aren't 0 or greater than 3
            if points > 0 and points < 4:
                self.__points = points
            else:
                raise ValueError("Questions must be worth 1, 2, or 3 points")
        else:
            raise TypeError('Points must be an int')

    points = property(get_points, set_points)


# global variables
question_list = []
json_file_name = ""
current_question_index = None


def search_questions():
    """searches the editor for questions that have been created in the listbox"""
    # gets results from the search box
    query = widgets['Search bar'].get()
    search_results = []
    properties = ['question', 'correct_feedback', 'incorrect_feedback']
    # loops through question list and searches for similar matches and not case sensitive
    for question in question_list:
        added = False
        # loops through properties to see if question is in there
        for prop in properties:
            # getattr takes an object and a string and returns the property from that object that's listed in that
            # string
            if query.lower() in getattr(question, prop).lower():
                search_results.append(question)
                added = True
                break
        if not added:
            for answer in question.answers:
                if len(get_close_matches(query, answer, 1, 0.75)) > 0:
                    search_results.append(question)
                    break

    widgets['Listbox of Q'].delete(0, END)
    for question in search_results:
        widgets['Listbox of Q'].insert(END, question.question)


def clear_search():
    """function clears the search bar in the editor"""
    widgets['Search bar'].delete(0, END)
    # refreshes the question list
    refresh_q_list()


def check_question_exists(question):
    """This function checks if a question entered in the editor gui is the same as one already in the question
    file the user has uploaded. Is called once the add question has been selected"""
    return get_close_matches(widgets['Question'].get(), widgets['Listbox of Q'].get(0, END), 3, 0.75)


def clear_gui():
    """This function clears the screen of all gui components (buttons, labels, entry boxes, etc.)
    It is triggered once the user leaves a specific screen to go to another part of the program. Example: user
    goes from main menu to quiz menu"""
    global widgets
    keys = list(widgets.keys()).copy()
    # loops through all widget keys in dictionary and removes them from program
    for key in keys:
        # begins try statement to remove widget keys
        try:
            widgets[key].grid_remove()
        # catches AttributeErrors so program doesn't crash
        except AttributeError:
            pass
        widgets.pop(key)
    # deletes the menu bar
    menu_bar.delete(0, END)


def clear_edit_menu():
    """This function clears the editor gui, it is called on in the editor gui, editor, and clear cascade option"""
    global widgets
    # deletes widget entries
    widgets['Question'].delete(0, END)
    widgets['ans1 entry'].delete(0, END)
    widgets['ans2 entry'].delete(0, END)
    widgets['ans3 entry'].delete(0, END)
    widgets['ans4 entry'].delete(0, END)
    widgets['Right Feedback'].delete(0, END)
    widgets['Wrong Feedback'].delete(0, END)
    widgets['Points entry'].delete(0, END)
    widgets['Search bar'].delete(0, END)
    widgets['combo_box'].set(1)


def question_list_select(evt):
    """creates a selector for the listbox """
    try:
        global current_question_index
        # clears the menu
        clear_edit_menu()
        # widget builds an event widget for getting the click index from the question list click
        widg = evt.widget
        # curson selection
        current_question_index = int(widg.curselection()[0])
        current_question = question_list[current_question_index]
        widgets['Question'].insert(0, current_question.question)
        # widgets['ans1 entry'].insert(0, current_question.question)
        widgets['ans1 entry'].insert(0, current_question.answers[0])
        widgets['ans2 entry'].insert(0, current_question.answers[1])
        widgets['ans3 entry'].insert(0, current_question.answers[2])
        widgets['ans4 entry'].insert(0, current_question.answers[3])
        widgets['Right Feedback'].insert(0, current_question.correct_feedback)
        widgets['Wrong Feedback'].insert(0, current_question.incorrect_feedback)
        # add points
        widgets['Points entry'].insert(0, current_question.points)
        # widgets['Correct Answer Label'].insert(0, current_question.answer_index)
        widgets['combo_box'].set(current_question.answer_index + 1)
    except:
        pass


def add_extension():
    """Adds json extension to file names"""
    global json_file_name
    # makes file ending a json
    if not json_file_name.endswith(".json"):
        json_file_name += ".json"


def new_file():
    """This allows the user to save a new file within the editor gui. It is called when the user selects save file
    within the editor gui's editor cascade option and save file"""
    global json_file_name
    # creates a file dialog popup to save the file as a json
    json_file_name = filedialog.asksaveasfilename(title="Save file", filetypes=(("question files", "*.json"),))
    add_extension()


def load_file():
    global question_list
    """This function will load a json file. It is called in the editor under the editor cascade and load file"""
    # open file variable
    json_file_name = filedialog.askopenfilename(title="Open file", filetypes=(("question files", "*.json"),))
    add_extension()
    # opens and loops through json file and assigns it to all Question class aspects
    try:
        with open(json_file_name, 'r') as question_file:
            for dictionary in question_file:
                question = Question()
                dictionary = json.loads(dictionary)
                question.question = dictionary['_Question__question']
                question.points = dictionary['_Question__points']
                question.answer_index = dictionary['_Question__answer_index']
                question.correct_feedback = dictionary['_Question__feedback']['true']
                question.incorrect_feedback = dictionary['_Question__feedback']['false']
                question.answers = dictionary['_Question__answers']
                question.answer_index = dictionary['_Question__answer_index']
                question_list.append(question)
        refresh_q_list()
    # catches error when the file entered is blank or not a json
    except Exception as e:
        question_list = []
        messagebox.showinfo(title="Error: File I/O",
                            message=str(e) + "\nfile incompatible or corrupt")


def save_file():
    """This function saves a file entered into the editor. It is called in the editor gui, under the editor cascade and
    save file"""
    global json_file_name
    # opens new file if json file name is empty
    if json_file_name == "":
        new_file()
    # writes to new json file name and dumps info into it
    with open(json_file_name, 'w') as question_file:
        for question in question_list:
            json.dump(question.__dict__, question_file)
            question_file.write('\n')


def add_question():
    """This function will add a question to be used in the quiz. It is called in the editor gui, under the editor
    cascade, and called add question"""
    # creating a new Question variable
    added_question = Question()

    # gets input from question entry box and adds it to new Question variable
    try:
        # saves input into a Question
        added_question.question = str(widgets['Question'].get())
        # get_close_matches function to see if question exists
        similar_questions = check_question_exists(added_question.question)
        # if similar questions is greater than 0 it'll ask if you want to add it to the question list
        if len(similar_questions) > 0:
            # message prompt
            prompt = ('Your Question:\n' + added_question.question +
                      '\nis similar to:\n' + '\n'.join(similar_questions) +
                      '\nProceed with adding it to the question list?')
            will_add = messagebox.askyesno("Similar Questions Found", prompt)
        else:
            will_add = True

        # adds question if the user says yes they want to add it to the listbox
        if will_add == True:
            added_question.answers = [widgets['ans1 entry'].get(), widgets['ans2 entry'].get(),
                                      widgets['ans3 entry'].get(), widgets['ans4 entry'].get()]
            added_question.correct_feedback = widgets['Right Feedback'].get()
            added_question.incorrect_feedback = widgets['Wrong Feedback'].get()
            # changed set_question to answer_index, cast to int
            added_question.answer_index = int(widgets['combo_box'].get()) - 1
            if len(widgets['Points entry'].get().strip()) == 0:
                raise Exception("please enter a value for points")
            added_question.points = int(widgets['Points entry'].get())
            widgets['Listbox of Q'].insert(END, added_question.question)
            question_list.append(added_question)
            clear_edit_menu()
            current_question_index = None
    # catches errors if user does not enter in all the information to the text boxes preventing it from crashing
    except Exception as e:
        messagebox.showinfo(title="Error: Incomplete question",
                            message=str(e) + "\nquestion not added yet")


def refresh_q_list():
    """This function clears the editor gui's entry boxes of it's content for it to display with nothing in it."""
    # try and except to catch errors
    try:
        widgets['Listbox of Q'].delete(0, END)
        for question in question_list:
            widgets['Listbox of Q'].insert(END, question.question)
    except:
        pass


def main_menu_gui():
    """This is the main menu gui. When the user starts the program, this is what they will see. It is called when the
    program starts, or when the user hits Home in the file cascade in either the editor gui or quiz gui"""
    global widgets
    # clears all editor gui options in the program
    clear_gui()
    file_menu = Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='New File', command=new_file)
    file_menu.add_command(label='Load File', command=load_file)
    file_menu.add_command(label='Exit', command=exit)

    widgets['Quiz Button'] = Button(window, text='Quiz', font=btn_font, width=8, command=quiz_gui, bg=btn_bg)
    widgets['Quiz Button'].grid(row=0, column=0, padx=5, pady=3)

    widgets['Editor Button'] = Button(window, text='Editor', font=btn_font, width=8, command=editor_gui, bg=btn_bg)
    widgets['Editor Button'].grid(row=0, column=1, padx=5, pady=3)


def quiz_gui():
    """This is the quiz gui. It allows the user to cycle through a 3 question quiz and takes them automatically to the
        main menu once finished."""

    class Quiz():
        def __init__(self):
            # brings up error if there isn't 3 questions within the quiz
            if len(question_list) < 3:
                messagebox.showinfo(title="Game Error",
                                    message="Not Enough Questions\nA minimum of 3 question must be in the list")
                self.questions = None
            # initializes quiz variables
            else:
                self.questions = []
                self.score = 0
                self.possible_score = 0
                self.responses = []
                self.correct = []
                self.current_index = 0
                indices = []
                while len(indices) < 3:
                    index = random.randint(0, len(question_list))
                    if index not in indices and index < len(question_list):
                        indices.append(index)
                for index in indices:
                    current_question = question_list[index]
                    self.questions.append(current_question)
                    self.possible_score += current_question.points

        # loads questions into widgets
        def load_question(self):
            # creates current question
            current_question = self.questions[self.current_index]
            # creates questions, answers, values of them along with the index of the answer
            widgets['Question']['text'] = current_question.question
            widgets['Answer 1']['text'] = current_question.answers[0]
            widgets['Answer 1']['state'] = "normal"
            widgets['Answer 1']['bg'] = btn_bg
            widgets['Answer 2']['text'] = current_question.answers[1]
            widgets['Answer 2']['state'] = "normal"
            widgets['Answer 2']['bg'] = btn_bg
            widgets['Answer 3']['text'] = current_question.answers[2]
            widgets['Answer 3']['state'] = "normal"
            widgets['Answer 3']['bg'] = btn_bg
            widgets['Answer 4']['text'] = current_question.answers[3]
            widgets['Answer 4']['state'] = "normal"
            widgets['Answer 4']['bg'] = btn_bg
            widgets['Value']['text'] = ''
            # assigns a value based off of entered question points and current question
            value = f'Value: {current_question.points} point'
            # if point is more than one makes points plural
            if current_question.points > 1:
                value += 's'
            widgets['Value']['text'] = value
            # sets state of next question button to make user not be able to go through
            widgets['Next Question']['state'] = DISABLED
            # doesn't show feedback score yet
            widgets['Feedback']['text'] = ''
            # calls update score function
            self.update_score()

        def update_score(self):
            """Updates and sets score out of possible score"""
            widgets['Score']['text'] = f'Score: {self.score} of {self.possible_score}'

        def select_answer(self, answer_index):
            """Selected answer function based off of answer index"""
            keys = ['Answer 1', 'Answer 2', 'Answer 3', 'Answer 4']
            self.responses.append(self.questions[self.current_index].answers[answer_index])
            if self.questions[self.current_index].answer_index == answer_index:
                # Correct answer
                widgets[keys[answer_index]]['bg'] = "#00FF00"
                # adds question score to the user's score
                self.score += self.questions[self.current_index].points
                # updates score
                self.update_score()
                # Updates feedback to correct feedback
                widgets['Feedback']['text'] = self.questions[self.current_index].correct_feedback
                self.correct.append(True)
            else:
                # Incorrect answer
                # turns buttons red
                widgets[keys[answer_index]]['bg'] = "#FF0000"
                # updates feedback to incorrect feedback
                widgets['Feedback']['text'] = self.questions[self.current_index].incorrect_feedback
                self.correct.append(False)
            # loops through keys and disables them once answer is selected
            for key in keys:
                widgets[key]['state'] = DISABLED
            # sets quiz question number
            self.current_index += 1
            # sets next question button so user can go through more questions
            widgets['Next Question']['state'] = "normal"
            # once user has answered 3 questions the results pop up
            if self.current_index > 2:
                widgets['Next Question']['text'] = "Results"
                # displays results
                widgets['Next Question']['command'] = self.show_results

        def show_results(self):
            """Function to display the results"""
            msg = ''
            # loops through question indexes and gets the question and the responses
            for index in range(3):
                # adds users questions and responses to the msg to show in result
                msg += f'Question {index + 1}:\n'
                msg += self.questions[index].question + '\n\t'
                msg += self.responses[index] + ': '
                if self.correct[index]:
                    msg += 'correct'
                else:
                    msg += 'incorrect'
                msg += '\n'
            # prints final score
            msg += f'Final Score: {self.score} out of {self.possible_score}'
            # message box that shows the results and message
            messagebox.showinfo(title="Results",
                                message=msg)
            # goes back to main menu to have user do whatever they want
            main_menu_gui()

    game = Quiz()

    def start_game():
        """Function to start the quiz gui"""
        # next question button
        widgets['Next Question']['text'] = 'Next Question'
        # command that loads in the next question to the quiz
        widgets['Next Question']['command'] = game.load_question
        widgets['Score'] = Label(window, text='', font=btn_font)
        widgets['Score'].grid(row=0, column=4, pady=5, sticky=E, padx=5)

        widgets['Question'] = Label(text='', font=btn_font, width=35, anchor=W)
        widgets['Question'].grid(row=1, column=0, pady=10, padx=5)

        widgets['Answer 1'] = Button(window, text='', font=btn_font,
                                     width=50, anchor=W, command=lambda: game.select_answer(0), bg=btn_bg)
        widgets['Answer 1'].grid(row=2, column=0, columnspan=5, pady=10, padx=5)

        widgets['Answer 2'] = Button(window, text='', font=btn_font,
                                     width=50, anchor=W, command=lambda: game.select_answer(1), bg=btn_bg)
        widgets['Answer 2'].grid(row=3, column=0, columnspan=5, pady=10, padx=5)

        widgets['Answer 3'] = Button(window, text='', font=btn_font,
                                     width=50, anchor=W, command=lambda: game.select_answer(2), bg=btn_bg)
        widgets['Answer 3'].grid(row=4, column=0, columnspan=5, pady=10, padx=5)

        widgets['Answer 4'] = Button(window, text='', font=btn_font,
                                     width=50, anchor=W, command=lambda: game.select_answer(3), bg=btn_bg)
        widgets['Answer 4'].grid(row=5, column=0, columnspan=5, pady=10, padx=5)

        widgets['Feedback'] = Label(window, text='', font=btn_font, anchor=W)
        widgets['Feedback'].grid(row=6, column=0, columnspan=7, sticky=W, padx=5)

        widgets['Value'] = Label(window, text='', font=btn_font)
        widgets['Value'].grid(row=6, column=4, pady=5, sticky=E, padx=5)
        game.load_question()

    global widgets
    # clears all widget gui's from the current window
    clear_gui()
    # creates file menu
    file_menu = Menu(menu_bar, tearoff=False)
    # creates cascade with file, home and exit as options
    menu_bar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Home', command=main_menu_gui)
    file_menu.add_command(label='Exit', command=exit)

    # creates buttons and labels used in quiz gui

    widgets['Next Question'] = Button(window, text='Start Quiz', font=btn_font,
                                      width=12, anchor=W, command=start_game, bg=btn_bg)
    widgets['Next Question'].grid(row=0, column=0, pady=10, sticky=W, padx=5)

    # goes back to main menu once the quiz has reached 3 questions and shown results
    if game.questions == None:
        main_menu_gui()


def save_question():
    """This saves a question in the editor to the loaded file over a pre existing question"""
    global current_question_index
    if current_question_index != None:
        # creating a new Question variable
        added_question = Question()

        # gets input from question entry box and adds it to new Question variable
        try:
            # saves input into a Question
            added_question.question = str(widgets['Question'].get())
            added_question.answers = [widgets['ans1 entry'].get(), widgets['ans2 entry'].get(),
                                      widgets['ans3 entry'].get(), widgets['ans4 entry'].get()]
            added_question.correct_feedback = widgets['Right Feedback'].get()
            added_question.incorrect_feedback = widgets['Wrong Feedback'].get()
            # changed set_question to answer_index, cast to int
            added_question.answer_index = int(widgets['combo_box'].get()) - 1
            # raises an error if you don't enter a value for points
            if len(widgets['Points entry'].get().strip()) == 0:
                raise Exception("please enter a value for points")
            added_question.points = int(widgets['Points entry'].get())
            widgets['Listbox of Q'].insert(END, added_question.question)
            question_list[current_question_index] = added_question
            clear_edit_menu()
            refresh_q_list()
        # catches errors if user does not enter in all the information to the text boxes preventing it from crashing
        except Exception as e:
            messagebox.showinfo(title="Error: Incomplete question",
                                message=str(e) + "\nquestion not saved yet")
    # error if you try to save a question and nothing is selected
    else:
        messagebox.showinfo(title="Error: No Question Index",
                            message="You must select a question from the list to save over it\nquestion not saved")


def delete_question():
    """deletes selected question from editor"""
    global current_question_index
    # if selected question in the editor is not nothing
    if current_question_index != None:
        # pops question from the listbox
        question_list.pop(current_question_index)
        # refreshes listbox
        refresh_q_list()
        # clears editor
        clear_edit_menu()
        # sets the index to none
        current_question_index = None
    # shows message error if you didn't select a question
    else:
        messagebox.showinfo(title="Error: No Question Index",
                            message="You must select a question from the list to delete it\nquestion not deleted")


def editor_gui():
    """This is the editor gui of the program. It allows the user to add, save, and delete questions. You can also
     create a new file, load, and save a file. It is called when the user presses "editor" from the main menu"""
    global widgets
    # Calls the clear gui function
    clear_gui()
    # creates a file menu option at top of program
    file_menu = Menu(menu_bar, tearoff=False)
    # creates cascade options for File, home and exit (next 3 lines)
    menu_bar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Home', command=main_menu_gui)
    file_menu.add_command(label='Exit', command=exit)

    # creates an edit menu option at top of program
    edit_menu = Menu(menu_bar, tearoff=False)
    # creates cascades for editor, add question, save question
    menu_bar.add_cascade(label='Editor', menu=edit_menu)
    edit_menu.add_command(label='Add question', command=add_question)
    edit_menu.add_command(label='Save question', command=save_question)
    edit_menu.add_command(label='Delete question', command=delete_question)
    # adds line separator
    edit_menu.add_separator()
    # Creates cascade option for new, load, and save file
    edit_menu.add_command(label='New File', command=load_file)
    edit_menu.add_command(label='Load File', command=load_file)
    edit_menu.add_command(label='Save File', command=save_file)
    edit_menu.add_separator()
    edit_menu.add_command(label='Clear', command=clear_edit_menu)

    # Creation of buttons, labels, comboboxes and list boxes for editor gui
    widgets['Question edit'] = Label(window, text='Question', font=btn_font)
    widgets['Question edit'].grid(row=0, column=0, sticky=E, padx=5)

    widgets['Question'] = Entry(font=btn_font, width=60)
    widgets['Question'].grid(row=0, column=1, columnspan=3, pady=10, padx=5)

    widgets['Ans1 edit'] = Label(window, text='Answer 1', font=btn_font)
    widgets['Ans1 edit'].grid(row=1, column=0, sticky=E, padx=5)

    widgets['ans1 entry'] = Entry(font=btn_font, width=60)
    widgets['ans1 entry'].grid(row=1, column=1, columnspan=3, pady=10, padx=5)

    widgets['ans2 label'] = Label(window, text='Answer 2', font=btn_font)
    widgets['ans2 label'].grid(row=2, column=0, sticky=E, padx=5)

    widgets['ans2 entry'] = Entry(font=btn_font, width=60)
    widgets['ans2 entry'].grid(row=2, column=1, columnspan=3, pady=10, padx=5)

    widgets['ans3 label'] = Label(window, text='Answer 3', font=btn_font)
    widgets['ans3 label'].grid(row=3, column=0, sticky=E, padx=5)

    widgets['ans3 entry'] = Entry(font=btn_font, width=60)
    widgets['ans3 entry'].grid(row=3, column=1, columnspan=3, pady=10, padx=5)

    widgets['ans4 label'] = Label(window, text='Answer 4', font=btn_font)
    widgets['ans4 label'].grid(row=4, column=0, sticky=E, padx=5)

    widgets['ans4 entry'] = Entry(font=btn_font, width=60)
    widgets['ans4 entry'].grid(row=4, column=1, columnspan=3, pady=10, padx=5)

    widgets['Right label'] = Label(window, text='Right Feedback', font=btn_font)
    widgets['Right label'].grid(row=5, column=0, sticky=E, padx=5)

    widgets['Right Feedback'] = Entry(font=btn_font, width=60)
    widgets['Right Feedback'].grid(row=5, column=1, columnspan=3, pady=10, padx=5)

    widgets['Wrong label'] = Label(window, text='Wrong Feedback', font=btn_font)
    widgets['Wrong label'].grid(row=6, column=0, sticky=E, padx=5)

    widgets['Wrong Feedback'] = Entry(font=btn_font, width=60)
    widgets['Wrong Feedback'].grid(row=6, column=1, columnspan=3, pady=10, padx=5, sticky=E)

    # creates combobox of correct answers
    widgets['Correct Answer Label'] = Label(window, text='Correct Answer', font=btn_font)
    widgets['Correct Answer Label'].grid(row=7, column=0, sticky=E)
    correct_answers = [1, 2, 3, 4]
    widgets['combo_box'] = ttk.Combobox(window, values=correct_answers, font=btn_font, width=5)
    widgets['combo_box'].current(0)
    widgets['combo_box'].grid(row=7, column=1, padx=5, sticky=W)

    widgets['Points label'] = Label(window, text='Points', font=btn_font)
    widgets['Points label'].grid(row=7, column=2, sticky=E, padx=5)

    widgets['Points entry'] = Entry(font=btn_font, width=10)
    widgets['Points entry'].grid(row=7, column=3, columnspan=3, pady=10, padx=5, sticky=W)

    # creates listbox of questions entered
    widgets['Listbox of Q'] = Listbox(window, height=5, font=btn_font)
    widgets['Listbox of Q'].grid(row=8, column=0, columnspan=4, sticky=(N, E, S, W), padx=5)
    # binds a double click to the listbox and allows questions to be repopulated within editor gui
    widgets['Listbox of Q'].bind('<Double-Button>', question_list_select)

    widgets['Search bar'] = Entry(window, width=38, font=btn_font)
    widgets['Search bar'].grid(row=9, column=0, sticky=E, columnspan=2, padx=5)

    widgets['Search button'] = Button(window, text='Search', font=btn_font, width=15,
                                      command=search_questions, bg=btn_bg)
    widgets['Search button'].grid(row=9, column=2, padx=5, sticky=E)

    widgets['Clear Search'] = Button(window, text='Clear Search', font=btn_font, width=15,
                                     command=clear_search, bg=btn_bg)
    widgets['Clear Search'].grid(row=9, column=3, sticky=E, padx=5)
    refresh_q_list()


# creates a menu bar
menu_bar = Menu(window)
window.config(menu=menu_bar)

# Calls main menu gui
main_menu_gui()
# runs Tkinter window
window.mainloop()
