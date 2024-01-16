from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
from datetime import datetime

def generate_test_pdf(input_file, num_tests, questions_per_test, test_name):
    with open(input_file, 'r') as file:
        questions = file.read().split('\n\n')  # Assuming questions are separated by double line breaks

    for test_number in range(1, num_tests + 1):
        test_filename = f'{test_name}_test_{test_number}.pdf'  # Include test_name in the file name
        
        # Select a subset of questions for each test
        selected_questions = random.sample(questions, k=min(questions_per_test, len(questions)))

        # Create a PDF document
        pdf_canvas = canvas.Canvas(test_filename, pagesize=letter)

        # Set up the font and size for the questions
        pdf_canvas.setFont("Helvetica", 12)

        # Add student name and date at the top
        student_name = "Student Name: ________________"
        current_date = datetime.now().strftime("%Y-%m-%d")

        pdf_canvas.drawString(50, 750, student_name)
        pdf_canvas.drawString(50, 735, f"Date: {current_date}")

        # Center the title below the top line
        test_title = f"{test_name} {test_number}"  # Include test_name in the title
        title_width = pdf_canvas.stringWidth(test_title, "Helvetica", 14)  # Increased font size for title
        pdf_canvas.drawString((letter[0] - title_width) / 2, 720, test_title)

        # Write questions to the PDF
        line_height = 15
        current_y = 700

        for idx, question in enumerate(selected_questions, start=1):
            # Split the question into lines
            question_lines = question.split('\n')
            
            # Write each line to the PDF
            for line in question_lines:
                pdf_canvas.drawString(50, current_y, f'{idx}. {line}')
                current_y -= line_height

            current_y -= line_height  # Add extra space between questions

        # Save the PDF
        pdf_canvas.save()

        print(f'Test {test_number} generated successfully: {test_filename}')

# Example usage
input_file = 'questions.txt'  # Replace with the actual file name
num_tests = 5  # Replace with the desired number of tests
questions_per_test = 5  # Replace with the desired number of questions per test
test_name = 'Verifica di Filosofia'  # Replace with the desired test name
generate_test_pdf(input_file, num_tests, questions_per_test, test_name)
