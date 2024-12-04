# User Management Specification Document


# Preface

In this document, the requirements to be used in the software development process of the user management app and information about the user experience are given in detail.

---

## General Requirements
- The User Management Screen is designed for authorized users to add, edit and manage user information. This screen must have a user list where users are displayed.
- The screen should be responsive designed to be user-friendly and ergonomic.

---

## Startup Screen
- When the application starts, the **User List** section is shown on the left side of the screen by default.
- “New User” form is shown on the right side looks blank and no fields are filled.
- On the List just Enabled users shown. To see Disabled users **Hide Disabled Users** option can be removed. 
---

## User Interface Components

### 1. User List
- **Position:** Left Panel.
- **Components:**
  - **Table Columns:** 
    - **ID:** The section containing users' ID numbers.
    - **Username:** Users' name in the system.
    - **Display Name:** User display name on the system.
    - **E-mail:** Users' registered e-mail address.
    - **Phone:** Phone number of the user.
    - **User Role:** The section that displays the user's role (Guest, Admin and SuperAdmin).
    - **Activation:** User's activation status. (Enabled/Disabled).
  - **Sorting:** Sorting can be done by clicking on the column headings.
  - **Filtering:** There is a checkbox at the top to filter users according to their Enabled/Disabled status (**Hide Disabled Users**). At the same time, users with that sign can be sorted by entering a letter or number by pressing the filter button on the column headers.
- **Behavior:**
  - When the edit user is right-clicked on a row, the **New User** form on the right is filled with the selected user's information and can be updated there. If the user exists, the **save user** button will change to **update user**.

### 2. New User Form
- **Position:** Right panel.
- **Zones:**
  - **Username:** Required space.
  - **Display Name:** Optional Space.
  - **Phone:** Optional Space.
  - **E-mail:** Required space. (must be in a valid e-mail format).
  - **User Roles:** Dropdown menu; "Guest", "Admin", "Super Admin" includes options.
  - **Activation:** Checkbox; to enable or disable the user.
- **Behavior:**
  - After all fields in the form are filled in, the information is saved by clicking the **Save** button at the top.
  - If the user exist the **save** button changes to **Update**.
  - If information is missing or incorrect, an error message is displayed next to the relevant field.

### 3. General Functions
- **Add New User:**
  - “+ New User” button, the form on the right is reset and prepared for user login.
- **Update User:**
  - When an existing user is selected, the information is filled in the form on the right and can be edited.
  - When the “Update” button is clicked, the user information is updated.
- **Filtering and Sorting:**
  - When “Hide Inactive Users” is checked, only active users are displayed.
    - Columns in the table can be sorted. 
    - Columns in the table can be filtered according to a mark entered.
    
- **Saving the Data:** User data is stored in the “User_Data.dat” file in the program files. Optionally or depending on the requirements, this file can be saved as an Excel file (.xlsx).
---

## Error Messages and Validation
- **Username and E-mail:** Required fields; if left blank, a warning is displayed.
- **Email:** Error message if an e-mail is entered in an invalid format: “Enter a valid e-mail address.”
- **User Roles:** If no option is selected: “Please select a user role.”
---

## Important Notes
- If the “Active” box is not checked, the user will be registered as passive.
- When the “Register” operation is successful, the message “Registration Successful” is displayed on the screen.
- In mobile view, the table should be reduced to one column and horizontal scrolling should be added.
---

## Mockup 
You can run the UMS.exe file in the file for the mockup and the source codes are also included.

---


