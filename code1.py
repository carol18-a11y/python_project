import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QHBoxLayout, QMessageBox, QComboBox, QTabWidget, QListWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

# ===============================
# Backend Data
# ===============================
users = []
employers = []
jobs = []
users = []     
employers = []  
jobs = [] 
applications = []

user_id_counter = 1
employer_id_counter = 1
job_id_counter = 1
@@ -39,341 +29,250 @@ def get_job_by_id(job_id):
return None


# ===============================
# UI Classes
# ===============================

def apply_global_style(app):
    """Applies modern color theme and font."""
    app.setStyleSheet("""
        QWidget {
            background-color: #f0f6ff;
            font-family: 'Segoe UI';
            font-size: 13pt;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border-radius: 8px;
            padding: 8px 15px;
            font-size: 12pt;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QLineEdit, QComboBox {
            background-color: #ffffff;
            border: 2px solid #0078d7;
            border-radius: 6px;
            padding: 6px;
            font-size: 12pt;
        }
        QLabel {
            color: #003366;
            font-weight: bold;
            font-size: 13pt;
        }
        QListWidget {
            background-color: #ffffff;
            border: 2px solid #0078d7;
            border-radius: 6px;
            font-size: 12pt;
        }
        QTabWidget::pane {
            border: 2px solid #0078d7;
            border-radius: 6px;
        }
        QTabBar::tab {
            background: #e7f0ff;
            border: 1px solid #0078d7;
            border-radius: 6px;
            padding: 6px 12px;
            margin: 3px;
            font-size: 12pt;
        }
        QTabBar::tab:selected {
            background: #0078d7;
            color: white;
        }
    """)


class JobPortal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💼 Job Portal System")
        self.setGeometry(200, 100, 450, 400)
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.signup_tab = QWidget()
        self.login_tab = QWidget()

        self.tabs.addTab(self.signup_tab, "📝 Sign Up")
        self.tabs.addTab(self.login_tab, "🔐 Login")

        # Signup Tab
        signup_layout = QVBoxLayout()
        signup_layout.setAlignment(Qt.AlignTop)

        self.signup_user = QLineEdit()
        self.signup_user.setPlaceholderText("Enter Username")

        self.signup_pass = QLineEdit()
        self.signup_pass.setPlaceholderText("Enter Password")
        self.signup_pass.setEchoMode(QLineEdit.Password)

        self.signup_role = QComboBox()
        self.signup_role.addItems(["Admin", "Employer", "Jobseeker"])

        signup_btn = QPushButton("Register")
        signup_btn.clicked.connect(self.signup_action)

        signup_layout.addWidget(QLabel("🧾 Create New Account"))
        signup_layout.addWidget(self.signup_user)
        signup_layout.addWidget(self.signup_pass)
        signup_layout.addWidget(self.signup_role)
        signup_layout.addWidget(signup_btn)
        self.signup_tab.setLayout(signup_layout)

        # Login Tab
        login_layout = QVBoxLayout()
        login_layout.setAlignment(Qt.AlignTop)

        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Username")

        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("Password")
        self.login_pass.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login_action)

        login_layout.addWidget(QLabel("🔑 Login to Your Account"))
        login_layout.addWidget(self.login_user)
        login_layout.addWidget(self.login_pass)
        login_layout.addWidget(login_btn)
        self.login_tab.setLayout(login_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def signup_action(self):
        global user_id_counter, employer_id_counter
        username = self.signup_user.text().strip()
        password = self.signup_pass.text().strip()
        role = self.signup_role.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        for u in users:
            if u["username"].lower() == username.lower():
                QMessageBox.warning(self, "Error", "Username already exists!")
                return

        users.append({"id": user_id_counter, "username": username, "password": password, "role": role})
        if role == "Employer":
            employers.append({
                "id": employer_id_counter,
                "user_id": user_id_counter,
                "company_name": "N/A",
                "location": "N/A"
            })
            employer_id_counter += 1
        user_id_counter += 1
        QMessageBox.information(self, "Success", f"{role} registered successfully!")

    def login_action(self):
        username = self.login_user.text().strip()
        password = self.login_pass.text().strip()

        user = find_user(username, password)
        if not user:
            QMessageBox.warning(self, "Error", "Invalid credentials.")
            return

        role = user["role"]
        QMessageBox.information(self, "Welcome", f"Logged in as {role}")
        self.hide()

        if role == "Admin":
            self.admin_window = AdminWindow()
            self.admin_window.show()
        elif role == "Employer":
            self.emp_window = EmployerWindow(user)
            self.emp_window.show()
        elif role == "Jobseeker":
            self.job_window = JobSeekerWindow(user)
            self.job_window.show()


# ===============================
# Role Windows
# ===============================

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧑‍💼 Admin Panel")
        self.setGeometry(250, 120, 550, 450)
        layout = QVBoxLayout()

        self.list_box = QListWidget()
        view_users = QPushButton("👥 View All Users")
        view_jobs = QPushButton("📋 View All Jobs")

        view_users.clicked.connect(self.show_users)
        view_jobs.clicked.connect(self.show_jobs)

        layout.addWidget(QLabel("Admin Dashboard"))
        layout.addWidget(view_users)
        layout.addWidget(view_jobs)
        layout.addWidget(self.list_box)
        self.setLayout(layout)

    def show_users(self):
        self.list_box.clear()
        for u in users:
            self.list_box.addItem(f"ID:{u['id']} | {u['username']} | Role: {u['role']}")

    def show_jobs(self):
        self.list_box.clear()
        for j in jobs:
            self.list_box.addItem(f"ID:{j['id']} | {j['title']} | {j['location']}")


class EmployerWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.emp = get_employer_by_user(user["id"])
        self.setWindowTitle("🏢 Employer Panel")
        self.setGeometry(250, 120, 550, 450)

        layout = QVBoxLayout()
        self.job_title = QLineEdit()
        self.job_title.setPlaceholderText("Job Title")
        self.job_skills = QLineEdit()
        self.job_skills.setPlaceholderText("Required Skills (comma separated)")
        self.job_salary = QLineEdit()
        self.job_salary.setPlaceholderText("Salary")
        self.job_location = QLineEdit()
        self.job_location.setPlaceholderText("Location")

        post_btn = QPushButton("📤 Post Job")
        post_btn.clicked.connect(self.post_job)

        self.job_list = QListWidget()
        view_jobs_btn = QPushButton("📂 View My Jobs")
        view_jobs_btn.clicked.connect(self.view_jobs)

        layout.addWidget(QLabel("Manage Your Job Posts"))
        layout.addWidget(self.job_title)
        layout.addWidget(self.job_skills)
        layout.addWidget(self.job_salary)
        layout.addWidget(self.job_location)
        layout.addWidget(post_btn)
        layout.addWidget(view_jobs_btn)
        layout.addWidget(self.job_list)
        self.setLayout(layout)

    def post_job(self):
        global job_id_counter
        title = self.job_title.text().strip()
        skills = self.job_skills.text().strip()
        salary = self.job_salary.text().strip()
        location = self.job_location.text().strip()

        if not title or not skills:
            QMessageBox.warning(self, "Error", "Please fill all job details.")
            return
def signup():
    global user_id_counter
    print("\n--- Sign Up ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (Admin / Employer / Jobseeker): ").title()

        jobs.append({
            "id": job_id_counter,
            "employer_id": self.emp["id"],
            "title": title,
            "skills": skills,
            "salary": salary,
            "location": location
        })
        job_id_counter += 1
        QMessageBox.information(self, "Success", "Job posted successfully!")

    def view_jobs(self):
        self.job_list.clear()
        for j in jobs:
            if j["employer_id"] == self.emp["id"]:
                self.job_list.addItem(f"ID:{j['id']} | {j['title']} | {j['skills']}")


class JobSeekerWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("💻 Job Seeker Panel")
        self.setGeometry(250, 120, 550, 450)

        layout = QVBoxLayout()
        self.skill_search = QLineEdit()
        self.skill_search.setPlaceholderText("Enter skill keyword to search jobs")
        search_btn = QPushButton("🔍 Search Jobs")
        search_btn.clicked.connect(self.search_jobs)

        self.jobs_list = QListWidget()
        self.apply_input = QLineEdit()
        self.apply_input.setPlaceholderText("Enter Job ID to Apply")
        apply_btn = QPushButton("✅ Apply")
        apply_btn.clicked.connect(self.apply_job)

        layout.addWidget(QLabel("Search & Apply for Jobs"))
        layout.addWidget(self.skill_search)
        layout.addWidget(search_btn)
        layout.addWidget(self.jobs_list)
        layout.addWidget(self.apply_input)
        layout.addWidget(apply_btn)
        self.setLayout(layout)

    def search_jobs(self):
        skill = self.skill_search.text().strip().lower()
        self.jobs_list.clear()
        for j in jobs:
            if skill in j["skills"].lower():
                self.jobs_list.addItem(f"ID:{j['id']} | {j['title']} | {j['skills']} | {j['location']}")

    def apply_job(self):
        job_id_text = self.apply_input.text().strip()
        if not job_id_text.isdigit():
            QMessageBox.warning(self, "Error", "Enter a valid Job ID.")
    for u in users:
        if u["username"].lower() == username.lower():
            print(" Username already exists!")
return
        job_id = int(job_id_text)
        job = get_job_by_id(job_id)
        if not job:
            QMessageBox.warning(self, "Error", "Invalid Job ID.")
    users.append({
        "id": user_id_counter,
        "username": username,
        "password": password,
        "role": role
    })
    print(f" {role} registered successfully with User ID:", user_id_counter)
    user_id_counter += 1

    if role == "Employer":
        create_employer_profile(users[-1])


def login():
    print("\n--- Login ---")
    username = input("Username: ")
    password = input("Password: ")
    user = find_user(username, password)

    if user is None:
        print(" Invalid username or password.")
        return

    print(f" Welcome, {user['username']} ({user['role']})!")

    if user["role"] == "Admin":
        admin_menu(user)
    elif user["role"] == "Employer":
        employer_menu(user)
    elif user["role"] == "Jobseeker":
        jobseeker_menu(user)
    else:
        print(" Invalid role.")


def create_employer_profile(user):
    global employer_id_counter
    print("\n--- Employer Profile Setup ---")
    company = input("Enter company name: ")
    location = input("Enter company location: ")

    employers.append({
        "id": employer_id_counter,
        "user_id": user["id"],
        "company_name": company,
        "location": location
    })
    print(f"Employer profile created with Employer ID: {employer_id_counter}")
    employer_id_counter += 1


def post_job(employer):
    global job_id_counter
    print("\n--- Post a New Job ---")
    title = input("Enter job title: ")
    skills = input("Enter required skills (comma separated): ")
    salary = input("Enter salary: ")
    location = input("Enter location: ")

    jobs.append({
        "id": job_id_counter,
        "employer_id": employer["id"],
        "title": title,
        "skills": skills,
        "salary": salary,
        "location": location
    })
    print(f" Job posted successfully with Job ID: {job_id_counter}")
    job_id_counter += 1


def view_my_jobs(employer):
    print("\n--- Your Posted Jobs ---")
    found = False
    for j in jobs:
        if j["employer_id"] == employer["id"]:
            print(f"ID:{j['id']} | Title:{j['title']} | Skills:{j['skills']} | Salary:{j['salary']} | Location:{j['location']}")
            found = True
    if not found:
        print("No jobs posted yet.")


def view_applications(employer):
    print("\n--- Applications for Your Jobs ---")
    for job in jobs:
        if job["employer_id"] == employer["id"]:
            print(f"\nJob: {job['title']}")
            for app in applications:
                if app["job_id"] == job["id"]:
                    user = next((u for u in users if u["id"] == app["user_id"]), None)
                    if user:
                        print(f"Applicant: {user['username']} | Status: {app['status']}")
    print("\nEnd of list.")


def search_jobs():
    print("\n--- Search Jobs ---")
    skill = input("Enter skill keyword: ").lower()
    found = False
    for j in jobs:
        if skill in j["skills"].lower():
            print(f"ID:{j['id']} | Title:{j['title']} | Skills:{j['skills']} | Salary:{j['salary']} | Location:{j['location']}")
            found = True
    if not found:
        print(" No jobs found for that skill.")


def apply_job(user):
    print("\n--- Apply for Job ---")
    job_id = int(input("Enter Job ID: "))
    job = get_job_by_id(job_id)
    if job is None:
        print(" Invalid Job ID.")
        return

    for a in applications:
        if a["job_id"] == job_id and a["user_id"] == user["id"]:
            print(" You already applied to this job.")
return

        for a in applications:
            if a["job_id"] == job_id and a["user_id"] == self.user["id"]:
                QMessageBox.warning(self, "Error", "Already applied to this job.")
                return
        applications.append({
            "job_id": job_id,
            "user_id": self.user["id"],
            "status": "Pending"
        })
        QMessageBox.information(self, "Success", "Application submitted!")


# ===============================
# Run Application
# ===============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_global_style(app)
    win = JobPortal()
    win.show()
    sys.exit(app.exec_())
    applications.append({
        "job_id": job_id,
        "user_id": user["id"],
        "status": "Pending"
    })
    print("Application submitted successfully!")


def view_my_applications(user):
    print("\n--- My Applications ---")
    for app in applications:
        if app["user_id"] == user["id"]:
            job = get_job_by_id(app["job_id"])
            if job:
                print(f"Job: {job['title']} | Status: {app['status']}")
    print("\nEnd of list.")


def admin_menu(admin):
    while True:
        print("""
----- ADMIN MENU -----
1. View all users
2. View all jobs
3. Delete a job
4. Logout
""")
        ch = input("Enter choice: ")
        if ch == "1":
            print("\nAll Users:")
            for u in users:
                print(f"ID:{u['id']} | Name:{u['username']} | Role:{u['role']}")
        elif ch == "2":
            print("\nAll Jobs:")
            for j in jobs:
                print(f"ID:{j['id']} | Title:{j['title']} | Location:{j['location']}")
        elif ch == "3":
            jid = int(input("Enter Job ID to delete: "))
            for j in jobs:
                if j["id"] == jid:
                    jobs.remove(j)
                    print(" Job deleted.")
                    break
            else:
                print(" Job not found.")
        elif ch == "4":
            break
        else:
            print("Invalid choice.")

def employer_menu(user):
    emp = get_employer_by_user(user["id"])
    while True:
        print("""
----- EMPLOYER MENU -----
1. Post Job
2. View My Jobs
3. View Applications
4. Logout
""")
        ch = input("Enter choice: ")
        if ch == "1":
            post_job(emp)
        elif ch == "2":
            view_my_jobs(emp)
        elif ch == "3":
            view_applications(emp)
        elif ch == "4":
            break
        else:
            print("Invalid choice.")


def jobseeker_menu(user):
    while True:
        print("""
----- JOB SEEKER MENU -----
1. Search Jobs
2. Apply for Job
3. View My Applications
4. Logout
""")
        ch = input("Enter choice: ")
        if ch == "1":
            search_jobs()
        elif ch == "2":
            apply_job(user)
        elif ch == "3":
            view_my_applications(user)
        elif ch == "4":
            break
        else:
            print("Invalid choice.")

def main():
    print("====== JOB PORTAL SYSTEM ======")
    while True:
        print("""
MAIN MENU
1. Sign Up
2. Login
3. Exit
""")
        choice = input("Enter your choice: ")
        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")



main()
