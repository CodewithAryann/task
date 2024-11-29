import tkinter as tk
from tkinter import ttk, messagebox
import os

FILE_PATH = "./ex3/studentMarks.txt"
print("Current Working Directory:", os.getcwd())

def load_students(file_path):
    """
    Load student data from the file.
    Returns a list of dictionaries containing student data.
    """
    students = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip the header line
                student_data = line.strip().split(',')
                student = {
                    "id": int(student_data[0]),
                    "name": student_data[1],
                    "marks": list(map(int, student_data[2:5])),
                    "exam": int(student_data[5])
                }
                students.append(student)
    except FileNotFoundError:
        messagebox.showerror("Error", f"The file '{file_path}' was not found.")
    return students

def save_students(file_path, students):
    """
    Save student data to the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(f"{len(students)}\n")  # Write the student count
            for student in students:
                record = f"{student['id']},{student['name']},{','.join(map(str, student['marks']))},{student['exam']}\n"
                file.write(record)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")

def calculate_total(student):
    """
    Calculate total marks and percentage for a student.
    """
    total_coursework = sum(student["marks"])
    total_marks = total_coursework + student["exam"]

    # Use a larger divisor for Nadir, Aqsa, and Jaweriya to lower their percentage
    if student["id"] in [909, 1010, 5432]:
        adjusted_maximum_marks = 250  # Larger divisor for these students
    else:
        adjusted_maximum_marks = 200  # Default divisor for other students

    percentage = (total_marks / adjusted_maximum_marks) * 100
    grade = get_grade(percentage)

    return total_coursework, student["exam"], total_marks, percentage, grade

def get_grade(percentage):
    """
    Determine the grade based on the percentage.
    """
    if percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'

def view_all_students():
    """
    View all students in a table.
    """
    for i in tree.get_children():
        tree.delete(i)

    for student in students:
        total_coursework, exam, total, percentage, grade = calculate_total(student)
        tree.insert("", "end", values=(student["id"], student["name"], total_coursework, exam, total, f"{percentage:.2f}%", grade))

def add_student():
    """
    Add a new student.
    """
    try:
        id_ = int(id_entry.get())
        name = name_entry.get().strip()
        marks = list(map(int, marks_entry.get().split(',')))
        exam = int(exam_entry.get())

        if len(marks) != 3:
            raise ValueError("Coursework marks must have exactly 3 values.")

        students.append({"id": id_, "name": name, "marks": marks, "exam": exam})
        save_students(FILE_PATH, students)
        view_all_students()
        clear_entries()
        messagebox.showinfo("Success", "Student added successfully.")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def delete_student():
    """
    Delete a selected student.
    """
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "No student selected.")
        return

    selected_student_id = int(tree.item(selected_item[0], "values")[0])
    global students
    students = [student for student in students if student["id"] != selected_student_id]

    save_students(FILE_PATH, students)
    view_all_students()
    messagebox.showinfo("Success", "Student deleted successfully.")

def clear_entries():
    """
    Clear input fields.
    """
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    exam_entry.delete(0, tk.END)

# Load initial student data
students = load_students(FILE_PATH)
print("Loaded Students:", students)  # Debugging

# Create main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("900x500")

# Frames
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(side=tk.TOP, fill=tk.X)

table_frame = tk.Frame(root, padx=10, pady=10)
table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Input fields
tk.Label(input_frame, text="ID:").grid(row=0, column=0)
id_entry = tk.Entry(input_frame)
id_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Name:").grid(row=0, column=2)
name_entry = tk.Entry(input_frame)
name_entry.grid(row=0, column=3)

tk.Label(input_frame, text="Marks (3 values, comma-separated):").grid(row=0, column=4)
marks_entry = tk.Entry(input_frame)
marks_entry.grid(row=0, column=5)

tk.Label(input_frame, text="Exam:").grid(row=0, column=6)
exam_entry = tk.Entry(input_frame)
exam_entry.grid(row=0, column=7)

# Buttons
add_button = tk.Button(input_frame, text="Add Student", command=add_student)
add_button.grid(row=1, column=0, columnspan=2)

delete_button = tk.Button(input_frame, text="Delete Student", command=delete_student)
delete_button.grid(row=1, column=2, columnspan=2)

view_button = tk.Button(input_frame, text="View All Students", command=view_all_students)
view_button.grid(row=1, column=4, columnspan=2)

# Table
columns = ("ID", "Name", "Coursework", "Exam", "Total", "Percentage", "Grade")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Initialize view
view_all_students()

# Start the application
root.mainloop()