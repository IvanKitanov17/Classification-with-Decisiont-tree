import io
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import pandas
from CSVReader import CSVReader
from Algorithm import DecisionTreeAlgorithm
from Application import NewWindow
from Algorithm.Leaf import Leaf
from Algorithm.HelperMethods import is_number
from os import path

#  creating the global variables for the application and their default values
data_set_filename = ""
new_data_filename = ""
decision_tree = None
headers = []
training_data = []
new_data = []


def is_filename_empty(filename):
    return filename == "" or filename is None


def delete_content(filename):
    with open(filename, "w"):
        pass


def show_gini_impurity():
    if len(training_data) == 0:
        massage = tkinter.messagebox.showwarning("Caution",
                                                 "Please select a data set for classification before proceeding!")
    else:
        gini_impurity = round(DecisionTreeAlgorithm.get_gini_impurity(training_data), 3)

        message_text = "The Gini Impurity of the data set is: " + str(gini_impurity)
        statusbar["text"] = "Gini impurity calculated."
        message = tkinter.messagebox.showinfo("Gini Impurity", message_text)

        if message == "ok":
            statusbar["text"] = "Classification algorithm GUI"


def show_data_details():
    data_set_filename_info = data_set_filename
    new_data_filename_info = new_data_filename
    tree = None

    if is_filename_empty(data_set_filename):
        data_set_filename_info = "empty"

    if is_filename_empty(new_data_filename_info):
        new_data_filename_info = "empty"

    if decision_tree is None:
        tree = "empty"
    else:
        tree = "built"

    message_text = "Data set filename:  " + data_set_filename_info + "\nNew data filename:   " + new_data_filename_info + "\nTree: " + tree
    statusbar["text"] = "Data details showed."
    message = tkinter.messagebox.showinfo("Data Details", message_text)

    if message == "ok":
        statusbar["text"] = "Classification algorithm GUI"


def on_closing(master):
    statusbar["text"] = "Classification algorithm GUI"
    master.destroy()


def exit_now():
    exit(0)


def clear_parameters():
    global data_set_filename
    data_set_filename = ""
    global new_data_filename
    new_data_filename = ""
    global decision_tree
    decision_tree = None
    global headers
    headers = []
    global training_data
    training_data = []
    global new_data
    new_data = []
    statusbar["text"] = "Parameters cleared."


def how_the_algorithm_works():
    text = 'The classification is done through iterating the data set, finding its unique values and creating questions, based on the values. ' \
           'While building the decision tree each question is iterated and the one chosen for partitioning the data is the question that provides the most information gain. ' \
           'The information gain is based on the uncertainty of the data set (its Gini impurity), from it is subtracted the weighted impurity of the two subtrees created by the partitioning' \
           ' based on the question. This is done recursively until a leaf node is reached at the end of each partition. Each leaf node represents a row in the data set ' \
           'meaning that once the leaf node is reached it is already classified. Based on this classification the algorithm returns the result for the new data.'

    statusbar["text"] = "How the algorithm works?"
    message = tkinter.messagebox.showinfo('Help - "How the algorithm works?"', text)

    if message == "ok":
        statusbar["text"] = "Classification algorithm GUI"


def how_to_classify():
    text = 'To classify new data, first the data set should be loaded. To do this click the "Load data set" button in the toolbar. ' \
           'Then the new data needs to be added by clicking on the "Load new data" button. To see if this is done correctly click on "Show data details" in the file menu.' \
           'The classification is completed by pressing the "Classify new data" button, a new window appears with the result of the classification.'

    statusbar["text"] = "How to classify new data?"
    message = tkinter.messagebox.showinfo('Help - "How to classify new data?"', text)

    if message == "ok":
        statusbar["text"] = "Classification algorithm GUI"


def how_the_printing_is_done():
    text = 'To print the tree first a classification should be performed. To see if classification is done, press "Show data details" in the file meny. ' \
           'If the message shows that the tree is built, press the "Show decision tree" button. After that a new window appears with the decision tree for the current training_data.'

    statusbar["text"] = "How to get decisiont tree?"
    message = tkinter.messagebox.showinfo('Help - "How to get the decision tree?"', text)

    if message == "ok":
        statusbar["text"] = "Classification algorithm GUI"


def load_data_set():
    filename = filedialog.askopenfilename(title="Select file", filetypes=(("CSV Files", "*.csv"),))
    global data_set_filename
    filename_holder = data_set_filename

    if not filename:
        data_set_filename = filename_holder
    else:
        data_set_filename = filename
        global headers
        global training_data
        headers, training_data = CSVReader.read(data_set_filename)
        statusbar["text"] = "Training data loaded."


def load_new_data_set():
    filename = filedialog.askopenfilename(title="Select file", filetypes=(("CSV Files", "*.csv"),))
    global new_data_filename
    filename_holder = new_data_filename

    if not filename:
        new_data_filename = filename_holder
    else:
        new_data_filename = filename
        global new_data
        new_data = CSVReader.read_without_headers(new_data_filename)
        statusbar["text"] = "New data loaded."


def show_data_set(filename):
    if is_filename_empty(filename):
        massage = tkinter.messagebox.showwarning("Caution", "Please select a file before proceeding!")
    else:
        df = CSVReader.get_dataframe(filename)
        root = Tk()
        root.title("Data set")
        root.geometry("700x400")

        new_window = NewWindow.TextBoxWindow(root)
        new_window.textbox.insert(END, df.to_string())
        new_window.textbox.config(state="disabled")

        statusbar["text"] = "Data set shown."
        root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))


def classify_new_data():
    if len(training_data) == 0 or len(new_data) == 0:
        massage = tkinter.messagebox.showwarning("Caution",
                                                 "Please select file destination for training data or new data to be classified before proceeding!")
    else:
        tree = DecisionTreeAlgorithm.build_tree(training_data)
        global decision_tree
        decision_tree = tree

        root = Tk()
        root.title("Classification")
        root.geometry("700x400")

        new_window = NewWindow.TextBoxWindow(root)

        new_window.textbox.insert(END, "Classification of the new data:\n")
        iterator = 1
        delete_content("classification_result.txt")
        classification_file = open("classification_result.txt", 'a')

        for row in new_data:
            result = DecisionTreeAlgorithm.get_results_with_percentages(DecisionTreeAlgorithm.classify(row, tree))
            textbox_line = str(iterator) + ": " + str(result) + "\n"
            new_window.textbox.insert(END, textbox_line)

            keys = list(result.keys())
            classification_file.write(str(keys[0]) + "\n")
            iterator += 1

        classification_file.close()
        new_window.textbox.config(state="disabled")
        statusbar["text"] = "Classification completed."
        root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))


def print_classification_result():
    filename = "classification_result.txt"

    if decision_tree is None or path.exists(filename) == FALSE:
        massage = tkinter.messagebox.showwarning("Caution",
                                                 "The classification is not performed yet or the classification_results file is missing. Before proceding please perform a classification of the data ")
    else:
        classification_file = open(filename, 'r')
        lines = classification_file.readlines()
        results = {}

        for line in lines:
            if line not in results:
                results[line] = 0
            results[line] += 1

        text = "Classification results:\n"
        keys = list(results.keys())
        values = list(results.values())
        for i in range(len(results)):
            text = text + str(keys[i]).rstrip() + ": " + str(values[i]) + "\n"

        statusbar["text"] = "CLassification results shown"
        message = tkinter.messagebox.showinfo("Classification results", text)

        if message == "ok":
            statusbar["text"] = "Classification algorithm GUI"


def get_question_as_string(question):
    condition = "=="

    if is_number(question.value):
        condition = ">="

    question_text = str(headers[question.get_column()]) + " " + condition + " " + str(question.get_value()) + "?"
    return question_text


def print_tree(node, distance=""):
    if isinstance(node, Leaf):
        print(distance + "Result: ", node.get_result())
        return

    print(distance + get_question_as_string(node.get_question()))

    print(distance + 'True branch:')
    print_tree(node.get_true_branch(), distance + "  ")

    print(distance + 'False branch:')
    print_tree(node.get_false_branch(), distance + "  ")


def print_decision_tree():
    if decision_tree is None:
        massage = tkinter.messagebox.showwarning("Caution",
                                                 "The decision tree is not built. A tree can be built by classificating the data before proceding with printing the tree!")
    else:
        root = Tk()
        root.title("Decision tree representation")
        root.geometry("700x400")

        new_window = NewWindow.TextBoxWindow(root)

        new_window.textbox.insert(END, "Decision tree:\n")

        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        print_tree(decision_tree)

        output = new_stdout.getvalue()

        sys.stdout = old_stdout

        decision_tree_file = open("decision_tree.txt", 'w')
        decision_tree_file.write(output)
        decision_tree_file.close()

        decision_tree_file = open("decision_tree.txt", 'r')
        lines = decision_tree_file.readlines()

        for line in lines:
            new_window.textbox.insert(END, line)

        decision_tree_file.close()
        statusbar["text"] = "Decision tree shown."
        root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))


def save_classification_result():
    filename = "classification_result.txt"

    if decision_tree is None or path.exists(filename) == FALSE:
        massage = tkinter.messagebox.showwarning("Caution",
                                                 "The decision tree is not built or the classification_result file is missing."
                                                 " They can be obtained by classificating the data before proceding with saving the result!")
    else:
        filename = open("classification_result.txt", 'r')
        local_new_data = new_data
        results = []
        lines = filename.readlines()

        for line in lines:
            results.append(line.rstrip())

        for i in range(len(local_new_data)):
            local_new_data[i][-1] = results[i]

        df = pandas.DataFrame(local_new_data, columns=headers)
        df.to_csv("result_new_data.csv", index=False, header=True)

        statusbar["text"] = "Classification results saved"
        message = tkinter.messagebox.showinfo("Classification results saved",
                                              "Classification results saved successfully")

        if message == "ok":
            statusbar["text"] = "Classification algorithm GUI"


if __name__ == "__main__":
    base_window = Tk()
    base_window.title("Classification with decision tree")
    base_window.geometry("400x400")

    # This is the drop down menu
    menu = Menu(base_window)
    base_window.config(menu=menu)

    file_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Show Gini impurity of the data set", command=show_gini_impurity)
    file_menu.add_command(label="Show Data details", command=show_data_details)
    file_menu.add_command(label="Show Classification results", command=print_classification_result)
    file_menu.add_command(label="Save Classification results", command=save_classification_result)
    file_menu.add_separator()
    file_menu.add_command(label="Quit", command=exit_now)

    edit_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Clear", command=clear_parameters)

    help_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="How the algorithm works?", command=how_the_algorithm_works)
    help_menu.add_command(label="How to classify new data?", command=how_to_classify)
    help_menu.add_command(label="How to print the decision tree?", command=how_the_printing_is_done)

    # this is the toolbar

    toolbar = Frame(base_window, bg="light blue")
    load_data_button = Button(toolbar, text="Load data set", command=load_data_set)
    load_data_button.pack(side=LEFT, padx=2, pady=2)

    load_new_data_button = Button(toolbar, text="Load new data", command=load_new_data_set)
    load_new_data_button.pack(side=LEFT, padx=2, pady=2)

    show_data_button = Button(toolbar, text="Show data set", command=lambda: show_data_set(data_set_filename))
    show_data_button.pack(side=LEFT, padx=2, pady=2)

    show_new_data_button = Button(toolbar, text="Show new data", command=lambda: show_data_set(new_data_filename))
    show_new_data_button.pack(side=LEFT, padx=2, pady=2)

    toolbar.pack(side=TOP, fill=X)

    # main fuctionality buttons

    button_frame = Frame(base_window)

    classification_button = Button(button_frame, text=" Classify new data ", height=2, width=15,
                                   command=classify_new_data)
    classification_button.pack(side=LEFT, padx=15)

    show_decisiontreee_button = Button(button_frame, text=" Show decision tree ", height=2, width=15,
                                       command=lambda: print_decision_tree())

    show_decisiontreee_button.pack(side=LEFT, padx=64)
    button_frame.pack(pady=10, fill=X)
    # status bar

    statusbar = Label(base_window, text="Classification algorithm GUI", bd=1, relief=SUNKEN, anchor=W)
    statusbar.pack(side=BOTTOM, fill=X)

    base_window.mainloop()
