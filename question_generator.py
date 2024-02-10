# Program Copyrighted by TuanHA47@fpt.com / anhtuanhoang2001@gmail.com / tuanx18
# This program runs along with question bank called "question_bank.json

import pandas as pd
import random
import time
import math
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import Dialog

# Initial DataFrame
ques_df = pd.read_json('question_bank.json')
pd.set_option('display.max_columns', None)


# Function to get the choice value based on the last letter
def get_choice_value(letter):
    letter = letter.lower()
    for var_name, var_value in globals().items():
        if var_name.startswith("choice_") and var_name.endswith(letter) and isinstance(var_value, str):
            return var_value
    return None


class AnswerFeedbackDialog(Dialog):
    def __init__(self, parent, title, feedback_text, is_correct, page):
        self.feedback_text = feedback_text
        self.is_correct = is_correct
        self.page = page
        super().__init__(parent, title)

    def body(self, master):
        text_widget = tk.Text(master, wrap='word', font=("Arial", 13), height=20, width=60)
        text_widget.insert(tk.END, self.feedback_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(pady=10)

        # Change background color based on correctness
        if self.is_correct:
            master.configure(bg='green')
        else:
            master.configure(bg='red')

        # Close the dialog after a delay
        master.after(1200000, master.destroy)  # Auto-close the dialog after 20 minutes

        return text_widget


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application BETA")
        self.root.geometry("1000x800")

        # Set the application icon using an ICO file
        icon_path = "cloud_app.png"  # Replace with the actual path to your ICO file
        try:
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            img = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, img)

        # Add big name
        tk.Label(root, text="GCP Quiz Application BETA 2024", font=("Arial", 24)).pack(pady=20)

        # Add copyright line
        tk.Label(root, text="© TuanHA47 / tuanx18\nVersion: 5.401", font=("Arial", 12)).pack()

        # Add buttons
        start_button = tk.Button(root, text="Start Quiz Generator", command=self.show_exam_customization)
        start_button.pack(pady=10)

        practice_button = tk.Button(root, text="Practice Document", command=self.practice_document)
        practice_button.pack(pady=10)

        # Add "Instruction / User Manual" button
        manual_button = tk.Button(root, text="Instruction / User Manual", command=self.show_user_manual)
        manual_button.pack(pady=10)

        # Add "Quit" button
        quit_button = tk.Button(root, text="Quit", command=self.quit_program)
        quit_button.pack(pady=10)

        # Center the main menu window on the screen
        self.center_window()

    def show_user_manual(self):
        try:
            with open("user_manual.txt", "r", encoding="utf-8") as file:
                manual_text = file.read()

            # Create a new window for user manual
            manual_window = tk.Toplevel(self.root)
            manual_window.title("User Manual")

            # Add a text widget to display the user manual content
            text_widget = tk.Text(manual_window, wrap='word', font=("Arial", 12), height=30, width=80)
            text_widget.insert(tk.END, manual_text)
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(pady=10, padx=10)

            # Add a scrollbar to the text widget
            scrollbar = tk.Scrollbar(manual_window, command=text_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar.set)

            # Center the manual window on the screen
            manual_window.update_idletasks()
            width = manual_window.winfo_width()
            height = manual_window.winfo_height()
            x = (manual_window.winfo_screenwidth() - width) // 2
            y = (manual_window.winfo_screenheight() - height) // 2
            manual_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open user manual: {e}")

    def quit_program(self):
        self.root.quit()

    def show_main_menu(self):
        # Re-create the main menu window
        main_menu_root = tk.Tk()
        main_menu = MainMenu(main_menu_root)
        main_menu_root.mainloop()

    def show_exam_customization(self):
        # Destroy the main menu window
        self.root.destroy()

        # Start the Exam Customization screen
        customization_root = tk.Tk()
        customization = ExamCustomization(customization_root, self)
        customization_root.mainloop()

    def start_quiz(self):
        # Destroy the main menu window
        self.root.destroy()

        # Start the quiz application
        quiz_root = tk.Tk()
        app = QuizApp(quiz_root)
        quiz_root.mainloop()

    def practice_document(self):
        messagebox.showinfo("Not Available", "This feature is not available at the moment.")

    def center_window(self):
        # Center the main menu window on the screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def show_not_available(self):
        # Display a message for the Practice Document button
        messagebox.showinfo("Not Available", "This feature is not available at the moment.")


class ExamCustomization:
    def __init__(self, root, main_menu_instance):
        self.root = root
        self.main_menu_instance = main_menu_instance

        # Define chapters
        chapters = [f"Chapter {i}" for i in range(1, 13)]

        self.root.title("Exam Customization")
        self.root.geometry("1000x800")

        # Configure column weights
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Container for the content
        content_frame = tk.Frame(root)
        content_frame.pack(expand=True, fill='both')

        # Left side for "Select Chapter"
        left_frame = tk.Frame(content_frame)
        left_frame.grid(row=1, column=2, sticky="nsew", padx=(170, 0))  # MARGIN LEFT

        # Title for "Select Chapter"
        title_label = tk.Label(left_frame, text="Select Chapter   ", font=("Arial", 20))
        title_label.grid(row=0, column=0, pady=(20, 10), columnspan=2)

        # Quiz Bank label to display the number of quizzes
        self.quiz_bank_label = tk.Label(left_frame, text="Quiz Bank: 0", font=("Arial", 12))
        self.quiz_bank_label.grid(row=len(chapters) + 1, column=0, pady=10, columnspan=3)

        # Check All checkbox
        self.check_all_var = tk.IntVar()
        check_all_checkbox = tk.Checkbutton(left_frame, text="Check All                             ",
                                            variable=self.check_all_var, command=self.check_all_toggle)
        check_all_checkbox.grid(row=0, column=2, pady=(25, 10), sticky="w")

        # Checkboxes for each chapter
        self.chapter_vars = [tk.IntVar() for _ in range(len(chapters))]
        for i, chapter in enumerate(chapters):
            chapter_checkbox = tk.Checkbutton(left_frame, text=chapter, variable=self.chapter_vars[i],
                                              command=self.update_quiz_bank_label)
            chapter_checkbox.grid(row=i + 1, column=0, columnspan=3, pady=5, sticky="w")

        # Right side for "Custom Exam Length"
        right_frame = tk.Frame(content_frame)
        right_frame.grid(row=1, column=7, sticky="nsew")

        # Title for "Custom Exam Length"
        title_label_right = tk.Label(right_frame, text="Custom Exam Length", font=("Arial", 20))
        title_label_right.grid(row=0, column=0, pady=(20, 10))

        # "Time Mode" section
        time_mode_label = tk.Label(right_frame, text="Time Mode", font=("Arial", 16))
        time_mode_label.grid(row=1, column=0, pady=(10, 5), sticky="w")

        time_mode_var = tk.StringVar()
        time_mode_var.set("No Time Limit")

        time_mode_options = ["No Time Limit", "Time Attack", "Flash Time Attack"]
        for i, option in enumerate(time_mode_options):
            time_mode_radio = tk.Radiobutton(right_frame, text=option, variable=time_mode_var, value=option,
                                             state=tk.DISABLED)
            time_mode_radio.grid(row=i + 2, column=0, pady=5, sticky="w")

        # "Result Mode" section
        result_mode_label = tk.Label(right_frame, text="Result Mode", font=("Arial", 16))
        result_mode_label.grid(row=5, column=0, pady=(20, 5), sticky="w")

        result_mode_var = tk.StringVar()
        result_mode_var.set("Instant Result")

        result_mode_options = ["Instant Result", "Exam Result at the end"]
        for i, option in enumerate(result_mode_options):
            result_mode_radio = tk.Radiobutton(right_frame, text=option, variable=result_mode_var, value=option,
                                               state=tk.DISABLED)
            result_mode_radio.grid(row=i + 6, column=0, pady=5, sticky="w")

        # Frame to contain Back and Continue buttons
        button_frame = tk.Frame(root)
        button_frame.pack(side="top", pady=100)

        # Back button
        back_button = tk.Button(button_frame, text="Back", command=self.back_to_main_menu)
        back_button.pack(side="left", padx=30)

        # Continue to Quiz button
        continue_button = tk.Button(button_frame, text="Continue to Quiz", command=self.continue_to_quiz)
        continue_button.pack(side="left", padx=0)  # Change the padx value to 0

        # Center the customization window on the screen
        self.center_window()

        # Bind the update_quiz_bank_label method to chapter checkbox events
        for var in self.chapter_vars:
            var.trace_add("write", self.update_quiz_bank_label)

        # "Number of Questions" section
        num_questions_label = tk.Label(right_frame, text="Number of Questions", font=("Arial", 16))
        num_questions_label.grid(row=9, column=0, pady=(20, 5), sticky="w")

        # Entry widget for user input - "Number of Questions"
        self.num_questions_var = tk.StringVar(value="30")
        num_questions_entry = tk.Entry(right_frame, textvariable=self.num_questions_var, font=("Arial", 12))
        num_questions_entry.grid(row=10, column=0, pady=5, sticky="w")

        # Small text label
        default_text_label = tk.Label(right_frame, text="Blank as Default (30 questions)", font=("Arial", 10),
                                      fg="gray")
        default_text_label.grid(row=11, column=0, pady=(0, 20), sticky="w")

        # Entry widget for user input - "Pass Requirement"
        self.pass_requirement_var = tk.StringVar(value="70%")
        pass_requirement_entry = tk.Entry(right_frame, textvariable=self.pass_requirement_var, font=("Arial", 12))
        pass_requirement_entry.grid(row=13, column=0, pady=5, sticky="w")

        # "Pass Requirement" section
        pass_requirement_label = tk.Label(right_frame, text="Pass Requirement", font=("Arial", 16))
        pass_requirement_label.grid(row=12, column=0, pady=(20, 5), sticky="w")

        # Set validation for "Number of Questions" entry
        num_questions_entry.config(validate="focusout",
                                   validatecommand=(num_questions_entry.register(self.validate_num_questions), "%P"))

        # Set validation for "Pass Requirement" entry
        pass_requirement_entry.config(validate="focusout", validatecommand=(
        pass_requirement_entry.register(self.validate_pass_requirement), "%P"))

    def validate_num_questions(self, value):
        try:
            num = int(value)
            if 5 <= num <= 100:
                return True
            else:
                messagebox.showwarning("Invalid Input", "For an ideal experience, consider selecting the number of questions between 5 and 100.")
                return False
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a numerical value for the number of questions. The default number will be applied otherwise.")
            return False

    def validate_pass_requirement(self, value):
        if "%" not in value:
            messagebox.showwarning("Invalid Input", "Pass requirement must be a percentage (e.g., 70%)")
            return False
        try:
            num = float(value.replace('%', ''))
            if 0 <= num <= 100:
                return True
            else:
                messagebox.showwarning("Invalid Input", "Pass requirement must be a percentage between 0 and 100")
                return False
        except ValueError:
            messagebox.showwarning("Invalid Input", "Pass requirement must be a percentage between 0 and 100")
            return False

    def check_all_toggle(self):
        check_all_state = self.check_all_var.get()
        for var in self.chapter_vars:
            var.set(check_all_state)

    def chapter_checkbox_toggle(self, *args):
        # Update the Check All checkbox state based on the individual checkboxes
        if all(var.get() == 1 for var in self.chapter_vars):
            self.check_all_var.set(1)
        else:
            self.check_all_var.set(0)

    def back_to_main_menu(self):
        # Destroy the current window and go back to the main menu
        self.root.destroy()
        self.main_menu_instance.show_main_menu()

    def continue_to_quiz(self):
        # Get the selected chapters
        selected_chapters = [i + 1 for i, var in enumerate(self.chapter_vars) if var.get() == 1]

        # If no chapter is selected, include questions from all chapters
        if not selected_chapters:
            selected_chapters = list(range(1, 13))

        # Convert 'chapter' column to integers
        ques_df['chapter'] = ques_df['chapter'].astype(int)

        # Filter questions based on selected chapters
        selected_questions = ques_df[ques_df['chapter'].isin(selected_chapters)]

        # Update the Quiz Bank label with the number of selected questions
        self.update_quiz_bank_label(selected_questions)

        # Shuffle the order of questions
        selected_questions = selected_questions.sample(frac=1).reset_index(drop=True)

        # Check if there are enough questions
        num_questions = self.num_questions_var.get()
        num_questions = int(num_questions) if num_questions.isdigit() else 30

        if len(selected_questions) < num_questions:
            if not self.show_not_enough_questions_warning():
                return

        # Retrieve values entered by the user for customization
        pass_requirement = self.pass_requirement_var.get()

        # Convert pass_requirement to a float (default to 70 if not provided or invalid)
        pass_requirement = float(pass_requirement.replace('%', '')) if pass_requirement.isdigit() else 70.0

        # Destroy the current window
        self.root.destroy()

        # Start the quiz application with the shuffled questions
        quiz_root = tk.Tk()
        app = QuizApp(quiz_root, selected_questions, ques_df, num_questions=num_questions,
                      pass_requirement=pass_requirement)
        quiz_root.mainloop()

    def show_not_enough_questions_warning(self):
        # Display a warning about not having enough questions
        warning_message = "There are not enough questions in the quiz bank for the whole exam.\n" \
                          "The exam will end instantly when it runs out of questions."

        # Show the warning and return True if the user clicks "OK"
        return messagebox.askokcancel("Not Enough Questions", warning_message)

    def update_quiz_bank_label(self, *args):
        # Update the Quiz Bank label with the number of selected questions
        selected_chapters = [i + 1 for i, var in enumerate(self.chapter_vars) if var.get() == 1]
        selected_questions = ques_df[ques_df['chapter'].isin(selected_chapters)]

        num_quiz_bank = len(selected_questions)
        self.quiz_bank_label.config(text=f"Quiz Bank: {num_quiz_bank}")

    def center_window(self):
        # Center the ExamCustomization window on the screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class QuizApp:
    def __init__(self, root, selected_questions, ques_df, num_questions=30, pass_requirement=70.0, time_mode="No Time Limit"):
        self.root = root
        self.root.title("Quiz Application - © TuanHA47")
        self.root.geometry("1000x800")

        # Set the application icon using an ICO file
        icon_path = "cloud_app.png"  # Replace with the actual path to your ICO file
        try:
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            img = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, img)

        self.question_label = tk.Label(root, text="", font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.choices_frame = tk.Frame(root)
        self.choices_frame.pack(pady=20)

        self.submit_button = tk.Button(root, text="Submit Answer", command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Next Question", command=self.next_question)
        self.next_button.pack(pady=10)

        self.exam_length = num_questions
        self.q_counter = 0
        self.correct_required = int((pass_requirement / 100) * self.exam_length)
        self.correct_user = 0
        self.user_score = 0
        self.used_questions = set()
        self.question_finished = []
        self.current_question = None
        self.selected_choice = tk.StringVar()
        self.selected_choices = []

        # Add progress label
        self.progress_label = tk.Label(root, text="", font=("Arial", 12))
        self.progress_label.pack(pady=10)

        # Add timer-related variables
        self.start_time = None
        self.end_time = None

        # Add timer label
        self.timer_label = tk.Label(root, text="", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        # Initialize timer ID
        self.timer_id = None

        # Center the main program window on the screen
        self.center_window()

        self.questions_df = ques_df
        self.selected_questions = selected_questions
        self.q_counter = 0

        # Start continuous timer update
        self.update_timer()

        self.next_question()

    def update_timer(self):
        try:
            self.update_timer_label()
            self.timer_id = self.root.after(1000, self.update_timer)  # Update every 1000 milliseconds (1 second)
        except Exception as e:
            print(f"An error occurred: {e}")

    def next_question(self):
        if self.q_counter < self.exam_length:
            # Find an unused question
            available_questions = set(self.questions_df.index) - set(self.used_questions)
            if not available_questions:
                messagebox.showinfo("Quiz Finished", "No more available questions.")
                self.display_results()
                return

            question_num = random.choice(list(available_questions))
            self.current_question = self.questions_df.loc[question_num]
            self.used_questions.add(question_num)
            self.display_question()

            # Start the timer when the first question is displayed
            if self.q_counter == 1:
                self.start_time = time.time()

            # Update the progress
            self.update_progress_label()
        else:
            self.display_results()

    def update_progress_label(self):
        progress_percentage = ((self.q_counter - 1) / self.exam_length) * 100
        progress_text = f"Progress: {self.q_counter - 1}/{self.exam_length} ({progress_percentage:.2f}%)"
        self.progress_label.config(text=progress_text)

    def update_timer_label(self):
        if self.start_time:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            timer_text = f"Time taken: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            self.timer_label.config(text=timer_text)

    def display_question(self):
        self.q_counter += 1
        self.selected_choice.set("")
        self.selected_choices.clear()

        if self.q_counter <= len(self.selected_questions):  # Check if there are questions left
            # Use the selected_questions DataFrame instead of self.questions_df
            self.current_question = self.selected_questions.iloc[self.q_counter - 1]

            # Split the question text into lines with a maximum length of 100 characters
            question_text = self.current_question['question']
            question_lines = self.split_text_into_lines(question_text)

            formatted_question = "\n".join(question_lines)
            self.question_label.config(
                text=f"Question {self.q_counter} ({self.current_question['point']}):\n\n{formatted_question}")

            for widget in self.choices_frame.winfo_children():
                widget.destroy()

            if self.current_question['multiple_choices']:
                # Display the number of correct answers
                correct_answers_count = len(self.current_question['correct_answer'])
                tk.Label(self.choices_frame, text=f"There are {correct_answers_count} correct answers",
                         font=("Arial", 12)).pack()

                # Create checkboxes for each choice
                choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                for i, choice in enumerate(choices):
                    choice_key = f'choice_{choice.lower()}'
                    if pd.notna(self.current_question.get(choice_key)):
                        choice_text = self.current_question[choice_key]
                        choice_lines = self.split_text_into_lines(choice_text)
                        formatted_choice = "\n".join(choice_lines)

                        checkbox_var = tk.IntVar()
                        checkbox = tk.Checkbutton(self.choices_frame,
                                                  text=f"{choice}. {formatted_choice}",
                                                  font=("Arial", 12), variable=checkbox_var)
                        checkbox.pack()
                        self.selected_choices.append((choice, checkbox_var))

            else:  # Single-choice question
                choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                for i, choice in enumerate(choices):
                    choice_key = f'choice_{choice.lower()}'
                    if pd.notna(self.current_question.get(choice_key)):
                        choice_text = self.current_question[choice_key]
                        choice_lines = self.split_text_into_lines(choice_text)
                        formatted_choice = "\n".join(choice_lines)

                        radio_button = tk.Radiobutton(self.choices_frame,
                                                      text=f"{choice}. {formatted_choice}",
                                                      font=("Arial", 12), variable=self.selected_choice, value=choice)
                        radio_button.pack()
        else:
            self.display_results()

    def split_text_into_lines(self, text, max_length=100):
        # Convert text to string if it's not already
        text_str = str(text)

        lines = []
        while len(text_str) > max_length:
            last_space = text_str.rfind(' ', 0, max_length)
            if last_space == -1:
                last_space = max_length
            lines.append(text_str[:last_space].strip())
            text_str = text_str[last_space:].strip()
        lines.append(text_str)
        return lines

    def check_answer(self):
        if self.current_question['multiple_choices']:
            # Check the selected checkboxes
            user_answers = [choice[0] for choice in self.selected_choices if choice[1].get() == 1]
            user_answer = user_answers  # user_answer is now a list for multiple-choice questions
        else:
            user_answer = self.selected_choice.get()

        # Convert correct_answer to a list if it is not already
        correct_answer = self.current_question['correct_answer']
        if not isinstance(correct_answer, list):
            correct_answer = [correct_answer]

        # Display detailed feedback for both correct and incorrect answers
        is_correct = set(user_answer) == set(correct_answer)
        feedback_text = f"Your answer is {'correct' if is_correct else 'INCORRECT!'}. " \
                        f"The correct answer is {', '.join(correct_answer)}\n\n" \
                        f"Reason: {self.current_question['reason']}\n\n" \
                        f"Chapter: {self.current_question['chapter']} - {self.current_question['chapter_name']}\n" \
                        f"Topic: {self.current_question['topic']}\n" \
                        f"Page: {int(self.current_question['page']) if 'page' in self.current_question and not math.isnan(self.current_question['page']) else 'N/A'}"

        # Use the modified AnswerFeedbackDialog with is_correct parameter and page information
        feedback_text = f"ID: {self.current_question['question_id']}\n" + feedback_text
        AnswerFeedbackDialog(self.root, "Answer Feedback", feedback_text, is_correct, self.current_question.get('page', 'N/A'))

        if is_correct:
            self.correct_user += 1
            self.user_score += self.current_question['point']

        self.question_finished.append(self.current_question['question_id'])
        self.next_question()

    def display_results(self):
        self.end_time = time.time()  # Stop the timer when the quiz is finished

        # Calculate average time per question
        average_time_per_question = self.calculate_total_time() / self.exam_length
        average_time_per_question_str = f"{average_time_per_question:.2f} seconds per question"

        result_message = f"Grade: {round((self.correct_user / self.exam_length) * 100, 2)} %\n" \
                         f"Number of correct answers: {self.correct_user}\n" \
                         f"Number of scores required to pass: {self.correct_required}\n" \
                         f"Total Points collected: {self.user_score}\n" \
                         f"Total Time taken: {round(self.calculate_total_time(), 2)} seconds\n" \
                         f"Average Time: {average_time_per_question_str}"

        result_title = "Quiz Results"

        if self.correct_user >= self.correct_required:
            result_title += "\n - ✓ Mission Passed!"
        else:
            result_title += "\n - × Mission Failed"

        # Show a message box with quiz results using askyesno
        result = messagebox.showinfo(result_title, result_message)

        if self.correct_user >= self.correct_required:
            # Show "You Passed" window with the option to take the exam again or quit
            self.show_passed_window()
        else:
            # Show "You Failed" window with the option to take the exam again or quit
            self.show_failed_window()

    def show_passed_window(self):
        # Create a new window for "You Passed"
        passed_window = tk.Toplevel(self.root)
        passed_window.title("You Passed!")

        # Add congratulatory message
        tk.Label(passed_window, text="Congratulations! You passed the quiz.", font=("Arial", 14)).pack(pady=20)

        # Add question about taking the exam again
        take_exam_button = tk.Button(passed_window, text="Take Exam Again", command=self.take_exam_again)
        take_exam_button.pack(pady=10)

        # Add "Back to Main Menu" button
        back_to_main_menu_button = tk.Button(passed_window, text="Back to Main Menu", command=self.back_to_main_menu)
        back_to_main_menu_button.pack(pady=10)

        quit_button = tk.Button(passed_window, text="Quit", command=self.root.destroy)
        quit_button.pack(pady=10)

        # Center the window on the main program screen
        self.center_window()

        # Center the passed window on the screen
        self.center_result_window(passed_window)

    def show_failed_window(self):
        # Create a new window for "You Failed"
        failed_window = tk.Toplevel(self.root)
        failed_window.title("You Failed!")

        # Add message about failing
        tk.Label(failed_window, text="Sorry, you did not pass the quiz. Better luck next time.",
                 font=("Arial", 14)).pack(pady=20)

        # Add question about taking the exam again
        take_exam_button = tk.Button(failed_window, text="Take Exam Again", command=self.take_exam_again)
        take_exam_button.pack(pady=10)

        # Add "Back to Main Menu" button
        back_to_main_menu_button = tk.Button(failed_window, text="Back to Main Menu", command=self.back_to_main_menu)
        back_to_main_menu_button.pack(pady=10)

        quit_button = tk.Button(failed_window, text="Quit", command=self.root.destroy)
        quit_button.pack(pady=10)

        # Center the window on the main program screen
        self.center_window()

        # Center the failed window on the screen
        self.center_result_window(failed_window)

    def back_to_main_menu(self):
        # Destroy the current window
        self.root.destroy()

        # Start the main menu
        main_menu_root = tk.Tk()
        main_menu = MainMenu(main_menu_root)
        main_menu_root.mainloop()

    def center_window(self):
        # Center the main program window on the screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def center_result_window(self, window):
        # Center the result window on the screen
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def take_exam_again(self):
        # Destroy the current window
        self.root.destroy()

        # Reset the quiz for another attempt
        root = tk.Tk()
        app = QuizApp(root, self.selected_questions, self.questions_df)
        root.mainloop()

    def reset_quiz(self):
        # Reset quiz variables and state
        self.q_counter = 0
        self.correct_user = 0
        self.user_score = 0
        self.used_questions.clear()
        self.question_finished.clear()
        self.start_time = None
        self.end_time = None
        self.selected_choice.set("")  # Clear the selected choice
        self.selected_choices.clear()

    def calculate_total_time(self):
        if self.start_time and self.end_time:
            total_time = self.end_time - self.start_time
            return float(total_time)
        else:
            return 0.0


if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()