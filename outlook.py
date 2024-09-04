import sys
sys.path.append(r'C:\Users\thanu_him4str\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages')

import tkinter as tk
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="teacher"
)
cursor = conn.cursor()

# Create a Tkinter window
root = tk.Tk()
root.title("Student Report Card")

# Function to fetch and display student data
def fetch_student_report():
    student_name = student_name_entry.get()
    student_class = student_class_entry.get()
    table_name = table_name_var.get()

    # Fetch student data from the selected table
    select_query = f"SELECT name, physics, chem, maths, percentage FROM {table_name} WHERE name = %s AND class = %s"
    cursor.execute(select_query, (student_name, student_class))
    student_data = cursor.fetchone()

    if student_data:
        student_name, physics, chemistry, maths, percentage = student_data

        # Create a frame for the student's report
        report_frame = ttk.Frame(root)
        report_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        # Create a label for student's name
        student_name_label = ttk.Label(report_frame, text=f"Student Name: {student_name}", font=("Helvetica", 12, "bold"))
        student_name_label.grid(row=0, column=0, columnspan=2)
        
        # Create a text widget for the student's report
        report_text = tk.Text(report_frame, height=15, width=40)
        report_text.grid(row=1, column=0, columnspan=2)

        report_text.insert(tk.END, f"Class: {student_class}\n")
        report_text.insert(tk.END, f"Table Name: {table_name}\n\n")
        report_text.insert(tk.END, "Test Scores:\n")
        report_text.insert(tk.END, f"Physics: {physics}\n")
        report_text.insert(tk.END, f"Chemistry: {chemistry}\n")
        report_text.insert(tk.END, f"Maths: {maths}\n\n")
        report_text.insert(tk.END, f"Percentage: {percentage}%\n")

        # Add performance advice based on the percentage
        advice = "Performance Advice: "
        if percentage >= 90:
            advice += "Excellent! Keep up the good work."
        elif 70 <= percentage < 90:
            advice += "Good. You can improve further."
        else:
            advice += "Needs improvement. Seek help if required."
        report_text.insert(tk.END, advice)

        # Generate bar graphs for test scores
        test_labels = ['Physics', 'Chemistry', 'Maths']
        test_scores = [physics, chemistry, maths]

        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        ax[0].bar(test_labels, test_scores)
        ax[0].set_title('Test Scores')
        ax[0].set_xlabel('Subjects')
        ax[0].set_ylabel('Marks')

        # Fetch co-curricular activity data
        select_co_curricular_query = f"SELECT SPORTS, DANCE, MUSIC, ARTS FROM co_curricular_activities WHERE name = %s AND class = %s"
        cursor.execute(select_co_curricular_query, (student_name, student_class))
        co_curricular_data = cursor.fetchone()

        if co_curricular_data:
            sports, dance, music, arts = co_curricular_data
            co_curricular_labels = ['Sports', 'Dance', 'Music', 'Arts']
            co_curricular_scores = [sports, dance, music, arts]

            ax[1].pie(co_curricular_scores, labels=co_curricular_labels, autopct='%1.1f%%')
            ax[1].set_title('Co-Curricular Activities')

        # Embed the Matplotlib plots in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=report_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=2, column=0, columnspan=2)

    else:
        # Display a message if student not found
        report_text.delete(1.0, tk.END)
        report_text.insert(tk.END, "Student not found in the selected table.")

# Create labels, entries, and buttons
student_name_label = ttk.Label(root, text="Student Name:")
student_name_label.grid(row=0, column=0)

student_name_entry = ttk.Entry(root)
student_name_entry.grid(row=0, column=1)

student_class_label = ttk.Label(root, text="Class:")
student_class_label.grid(row=1, column=0)

student_class_entry = ttk.Entry(root)
student_class_entry.grid(row=1, column=1)

table_name_var = tk.StringVar()
table_name_var.set("UT1")  # Default table selection
table_name_label = ttk.Label(root, text="Select Table:")
table_name_label.grid(row=2, column=0)

table_name_combobox = ttk.Combobox(root, textvariable=table_name_var, values=["UT1", "UT2", "MIDT", "FINAL"])
table_name_combobox.grid(row=2, column=1)

fetch_button = ttk.Button(root, text="Fetch Report", command=fetch_student_report)
fetch_button.grid(row=1, column=2)

# Run the Tkinter main loop
root.mainloop()

# Close the MySQL connection when done
cursor.close()
conn.close()
