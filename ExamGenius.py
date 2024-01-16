import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
from datetime import datetime
from tkinter import font
import os

class TestGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Test Generator")

        montserrat_font = font.Font(family="Montserrat", size=12)

        self.label_file = tk.Label(master, text="Select Questions File:", font=montserrat_font)
        self.label_file.grid(row=0, column=0, padx=10, pady=5)
        self.file_button = tk.Button(master, text="Choose File", command=self.choose_file, font=montserrat_font)
        self.file_button.grid(row=0, column=1, padx=10, pady=5)

        self.label_tests = tk.Label(master, text="Number of Tests:", font=montserrat_font)
        self.label_tests.grid(row=1, column=0, padx=10, pady=5)
        self.entry_tests = tk.Entry(master, font=montserrat_font)
        self.entry_tests.grid(row=1, column=1, padx=10, pady=5)

        self.label_questions = tk.Label(master, text="Questions per Test:", font=montserrat_font)
        self.label_questions.grid(row=2, column=0, padx=10, pady=5)
        self.entry_questions = tk.Entry(master, font=montserrat_font)
        self.entry_questions.grid(row=2, column=1, padx=10, pady=5)

        self.label_name = tk.Label(master, text="Test Name:", font=montserrat_font)
        self.label_name.grid(row=3, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(master, font=montserrat_font)
        self.entry_name.grid(row=3, column=1, padx=10, pady=5)

        self.label_date = tk.Label(master, text="Select Date:", font=montserrat_font)
        self.label_date.grid(row=4, column=0, padx=10, pady=5)

        self.selected_date_var = tk.StringVar()
        self.entry_date = tk.Entry(master, font=montserrat_font, state="readonly", textvariable=self.selected_date_var)
        self.entry_date.grid(row=4, column=1, padx=10, pady=5)
        self.calendar_button = tk.Button(master, text="Choose Date", command=self.choose_date, font=montserrat_font)
        self.calendar_button.grid(row=4, column=2, padx=10, pady=5)

        self.generate_button = tk.Button(master, text="Generate Tests", command=self.generate_tests, font=montserrat_font)
        self.generate_button.grid(row=5, column=0, columnspan=3, pady=10)

        self.selected_date = None

    def choose_file(self):
        file_path = filedialog.askopenfilename(title="Select Questions File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.questions_file = file_path
            self.label_file.config(text=f"Selected File: {file_path}")

    def choose_date(self):
        top = tk.Toplevel(self.master)
        current_date = datetime.now().date()
        cal = Calendar(top, font="Arial 14", selectmode="day", locale="en_US", cursor="hand1", date_pattern="dd.mm.yyyy", date=current_date)

        def set_date():
            selected_date_str = cal.get_date()
            self.selected_date = datetime.strptime(selected_date_str, "%d.%m.%Y").date()
            self.selected_date_var.set(selected_date_str)
            top.destroy()



        set_button = tk.Button(top, text="Set Date", command=set_date, font="Arial 12")
        set_button.pack()

        cal.pack()

    def generate_tests(self):
        try:
            # Check if the questions file exists
            if not hasattr(self, 'questions_file') or not os.path.exists(self.questions_file):
                messagebox.showerror("Error", "Please select a valid questions file.")
                return

            # Check if all fields are filled
            if not self.entry_tests.get() or not self.entry_questions.get() or not self.entry_name.get():
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            # Validate data types
            try:
                num_tests = int(self.entry_tests.get())
                questions_per_test = int(self.entry_questions.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for Number of Tests and Questions per Test.")
                return

            test_name = self.entry_name.get() if self.entry_name.get() else 'Test'

            with open(self.questions_file, 'r') as file:
                questions = file.read().split('\n\n')

            for test_number in range(1, num_tests + 1):
                test_filename = f'{test_name}_test_{test_number}.pdf'

                selected_questions = random.sample(questions, k=min(questions_per_test, len(questions)))

                pdf_canvas = canvas.Canvas(test_filename, pagesize=letter)
                pdf_canvas.setFont("Helvetica", 12)

                student_name = "Student Name: ________________"
                current_date = self.selected_date.strftime("%d.%m.%Y") if self.selected_date else datetime.now().strftime("%d.%m.%Y")

                pdf_canvas.drawString(50, 750, student_name)
                pdf_canvas.drawString(50, 735, f"Date: {current_date}")

                # ...

                pdf_canvas.save()

                print(f'Test {test_number} generated successfully: {test_filename}')

            messagebox.showinfo("Success", f"{num_tests} tests generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TestGeneratorGUI(root)
    root.mainloop()
