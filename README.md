# **Online School Registration System**

### **Introduction**

The **Online School Registration System** simplifies the school admission process for students and administrators. It allows students to create accounts, submit registration details, upload documents, and track admission status. Administrators can manage and verify student information and documents through a centralized platform.

Final project blog article: [Read the Blog Post]([#](https://blog.abogo.tech/announcing-the-online-school-registration-system-api-simplifying-school-admissions-for-developers?showSharer=true))  
Author LinkedIn:  

- [Abogo Lincoln](https://www.linkedin.com/in/abogo-nono)

---

### **Installation**

Follow these steps to set up the project on your local machine:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/abogo-nono/ors-backend.git
   cd ors-backend
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate     # For Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   Create a `.env` file in the root directory and add the required database configuration.  
   Then, run the following commands to create the database tables:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the application:**

   ```bash
   flask run
   ```

---

### **Screenshots**

![Student Registration Page](screenshots/Screenshot%202024-09-25%20025658.png)

![Admin Dashboard](screenshots/Screenshot%202024-09-25%20025955.png)

![Admin Dashboard](screenshots/Screenshot%202024-09-25%20030057.png)

---

### **Usage**

- **For Students:**
  - Register on the platform.
  - Submit required documents.
  - Track admission status.

- **For Administrators:**
  - View student submissions.
  - Verify documents.
  - Update admission status.

---

### **Contributing**

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add a feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a pull request.

---

### **Related Projects**

- [Online Course Registration System](https://github.com/iamtusharbhatia/Online-Course-Registration-System)

---

### **Licensing**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
