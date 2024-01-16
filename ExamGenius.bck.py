import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
from datetime import datetime

class TestGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Test Generator")

        self.label_file = tk.Label(master, text="Select Questions File:")
        self.label_file.grid(row=0, column=0)

        self.file_button = tk.Button(master, text="Choose File", command=self.choose_file)
        self.file_button.grid(row=0, column=1)

        self.label_tests = tk.Label(master, text="Number of Tests:")
        self.label_tests.grid(row=1, column=0)
        self.entry_tests = tk.Entry(master)
        self.entry_tests.grid(row=1, column=1)

        self.label_questions = tk.Label(master, text="Questions per Test:")
        self.label_questions.grid(row=2, column=0)
        self.entry_questions = tk.Entry(master)
        self.entry_questions.grid(row=2, column=1)

        self.label_name = tk.Label(master, text="Test Name:")
        self.label_name.grid(row=3, column=0)
        self.entry_name = tk.Entry(master)
        self.entry_name.grid(row=3, column=1)

        self.generate_button = tk.Button(master, text="Generate Tests", command=self.generate_tests)
        self.generate_button.grid(row=4, column=0, columnspan=2)

    def choose_file(self):
        file_path = filedialog.askopenfilename(title="Select Questions File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.questions_file = file_path
            self.label_file.config(text=f"Selected File: {file_path}")

    def generate_tests(self):
        try:
            num_tests = int(self.entry_tests.get())
            questions_per_test = int(self.entry_questions.get())
            test_name = self.entry_name.get() if self.entry_name.get() else 'Test'

            with open(self.questions_file, 'r') as file:
                questions = file.read().split('\n\n')

            for test_number in range(1, num_tests + 1):
                test_filename = f'{test_name}_test_{test_number}.pdf'

                selected_questions = random.sample(questions, k=min(questions_per_test, len(questions)))

                pdf_canvas = canvas.Canvas(test_filename, pagesize=letter)
                pdf_canvas.setFont("Helvetica", 12)

                student_name = "Student Name: ________________"
                current_date = datetime.now().strftime("%Y-%m-%d")

                pdf_canvas.drawString(50, 750, student_name)
                pdf_canvas.drawString(50, 735, f"Date: {current_date}")

                test_title = f"{test_name} {test_number}"
                title_width = pdf_canvas.stringWidth(test_title, "Helvetica", 14)
                pdf_canvas.drawString((letter[0] - title_width) / 2, 720, test_title)

                line_height = 15
                current_y = 700

                for idx, question in enumerate(selected_questions, start=1):
                    question_lines = question.split('\n')

                    for line in question_lines:
                        pdf_canvas.drawString(50, current_y, f'{idx}. {line}')
                        current_y -= line_height

                    current_y -= line_height

                pdf_canvas.save()

                print(f'Test {test_number} generated successfully: {test_filename}')

            messagebox.showinfo("Success", f"{num_tests} tests generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TestGeneratorGUI(root)
    root.mainloop()
