import sys
sys.path.append(r'C:\Users\thanu\Downloads\python-3.12.1-amd64\Lib\site-packages')


import mysql.connector

# Create a MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="teacher"
)
cursor = conn.cursor()

# Function to create a table
def create_table(table_name):
    global cursor

    create_query = "CREATE TABLE IF NOT EXISTS "+table_name+"(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), class VARCHAR(10), physics FLOAT, chem FLOAT, maths FLOAT, percentage float)"
    cursor.execute(create_query)
    conn.commit()

# Function to insert student data
def insert_data(table_name, name,class_name, physics, chem, maths):
    insert_query = f"INSERT INTO {table_name} (name, class, physics, chem, maths) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (name,class_name, physics, chem, maths))
    conn.commit()

# Function to insert co-curricular activity marks for a student
def insert_co_curricular_activity_marks(name, class_name, sports, dance, music, arts):
    insert_query = "INSERT INTO co_curricular_activities (name, class, sports, dance, music, arts) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (name, class_name, sports, dance, music, arts))
    conn.commit()

    
# Function to display student data
def display_table(table_name):
    select_query = f"SELECT ID, name, class, physics, chem, maths FROM {table_name}"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    if not rows:
        print("Table is empty.")
        return

    print(f"Table: {table_name}")
    print("{:<5} {:<15} {:<10} {:<10} {:<10} {:<10}".format("ID", "Name", "Class", "Physics", "Chemistry", "Maths"))

    for row in rows:
        ID, name, class_name, physics, chem, maths = row
        print(f"{ID:<5} {name:<15} {class_name:<10} {physics:<10} {chem:<10} {maths:<10}")

# Create the four tables
table_names = ["UT1", "UT2", "MIDT", "FINAL",]
for table_name in table_names:
    create_table(table_name)
    
#create table for co_curricular activities
a= "CREATE TABLE IF NOT EXISTS co_curricular_activities (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), class VARCHAR(10), SPORTS FLOAT, DANCE FLOAT, MUSIC FLOAT, ARTS FLOAT)"
cursor.execute(a)
conn.commit()
# Ask the teacher for the table name
table_choice = input("Enter the table name (UT1, UT2, MIDT, FINAL,co_curricular_activities): ")

if table_choice in ("UT1", "UT2", "MIDT", "FINAL"):
    # Insert data
    num_students = int(input("Enter the number of students: "))
    for _ in range(num_students):
        name = input("Name: ")
        class_name = input("Class: ")
        physics = float(input("Physics Marks: "))
        chem = float(input("Chemistry Marks: "))
        maths = float(input("Maths Marks: "))
        insert_data(table_choice, name, class_name, physics, chem, maths)

elif table_choice == "co_curricular_activities":
    num_student = int(input("Enter the number of students: "))
    for _ in range(num_student):
        name = input("Name: ")
        class_name = input("Class: ")
        sports_marks = float(input(f"Enter Sports Marks for {name} (out of 10): "))
        dance_marks = float(input(f"Enter Dance Marks for {name} (out of 10): "))
        music_marks = float(input(f"Enter Music Marks for {name} (out of 10): "))
        arts_marks = float(input(f"Enter Arts Marks for {name} (out of 10): "))
        insert_co_curricular_activity_marks(name, class_name, sports_marks, dance_marks, music_marks, arts_marks)
    
else:
    print("Invalid table name.")


        
# Function to calculate and store percentages
def calculate_and_store_percentages(table_name):
    select_query = f"SELECT id, physics, chem, maths FROM {table_name}"
    cursor.execute(select_query)
    rows = cursor.fetchall()


    for row in rows:
        student_id, physics, chem, maths = row
        total_marks = physics + chem + maths
        percentage = (total_marks / (3 * 100)) * 100  # Assuming each subject has a maximum of 100 marks
        update_query = f"UPDATE {table_name} SET percentage = %s WHERE id = %s"
        cursor.execute(update_query, (percentage, student_id))
        conn.commit()


# Create the four tables
table_names = ["UT1", "UT2", "MIDT", "FINAL"]
for table_name in table_names:
    calculate_and_store_percentages(table_name)


# Display the table
if table_choice in table_names:
    display_table(table_choice)
    
# Update data
def update_data(table_name, student_id, subject, marks):
    # Assuming your update query function is available
    if subject == "physics":
        update_query = f"UPDATE {table_name} SET physics = %s WHERE id = %s"
    elif subject == "chemistry":
        update_query = f"UPDATE {table_name} SET chem = %s WHERE id = %s"
    elif subject == "maths":
        update_query = f"UPDATE {table_name} SET maths = %s WHERE id = %s"
    else:
        print("Invalid subject choice.")
        return

    cursor.execute(update_query, (marks, student_id))
    conn.commit()


update_choice = input("Do you want to update any marks (yes/no)? ").lower()
if update_choice == "yes":
    student_id = int(input("Enter student ID to update: "))
    subject_choice = input("Which subject marks do you want to update (Physics/Chemistry/Maths)? ").lower()
    
    if subject_choice in ["physics", "chemistry", "maths"]:
        updated_marks = float(input(f"Updated {subject_choice.capitalize()} Marks: "))
        update_data(table_choice, student_id, subject_choice, updated_marks)
    else:
        print("Invalid subject choice.")


    
# Close the MySQL connection when done
cursor.close()
conn.close()
