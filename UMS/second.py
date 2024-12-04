import tkinter as tk
from tkinter import ttk, messagebox
import pickle

DATA_FILE = 'user_data.dat'
EXCEL_FILE = 'user_data.xlsx'

class UserManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()

        icon = tk.PhotoImage(file="C:/Users/doguk/PycharmProjects/UI for PIWorks/.venv/icon/icon.png")

        self.iconphoto(True, icon)
        self.title("User Management")
        self.geometry("800x800")
        self.is_fullscreen = False

        self.users = []
        self.load_user_data()

        self.create_widgets()
        self.populate_user_list()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)


        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)


        self.user_list_frame = ttk.LabelFrame(self.main_frame, text="User List")
        self.user_list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        button_frame = ttk.Frame(self.user_list_frame)
        button_frame.pack(anchor="w", pady=5)

        self.new_user_button = tk.Button(button_frame, text="+ New User", command=self.open_new_user_popup,
                                         bg="#007BFF", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        self.new_user_button.pack(side="left", padx=5)

        self.fullscreen_button = tk.Button(button_frame, text="Fullscreen", command=self.toggle_fullscreen,
                                           bg="#007BFF", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        self.fullscreen_button.pack(side="left", padx=5)

        self.hide_disabled_var = tk.BooleanVar()
        self.hide_disabled_check = ttk.Checkbutton(
            self.user_list_frame, text="Hide Disabled Users", variable=self.hide_disabled_var,
            command=self.populate_user_list
        )
        self.hide_disabled_check.pack(anchor="w", pady=5)


        columns = ("ID", "Username", "Display Name", "Phone", "Email","Role", "Enabled")
        self.user_tree = ttk.Treeview(self.user_list_frame, columns=columns, show="headings")
        for col in columns:
            self.user_tree.heading(col, text=col)
        self.user_tree.pack(fill="both", expand=True)

        self.user_tree.bind("<Button-3>", self.show_popup_menu)

    def open_new_user_popup(self, user=None):
        popup = tk.Toplevel(self)
        popup.title("New User" if not user else "Update User")
        popup.geometry("400x400")

        roles_var = tk.StringVar(value="Guest" if not user else user["roles"][0])
        enabled_var = tk.BooleanVar(value=True if not user else user["enabled"])


        def create_form_field(label_text, row, default_value=""):
            ttk.Label(popup, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(popup)
            entry.insert(0, default_value)
            entry.grid(row=row, column=1, padx=5, pady=5)

            error_label = tk.Label(popup, text=f"Please enter {label_text[:-1].lower()}!", fg="red")
            error_label.grid(row=row + 1, column=1, sticky="w", padx=5)
            error_label.grid_remove()

            def validate_input(event=None):
                if not entry.get().strip():
                    error_label.grid()
                else:
                    error_label.grid_remove()

            entry.bind("<KeyRelease>", validate_input)
            return entry

        self.username_entry = create_form_field("Username:", 0, user["username"] if user else "")
        self.display_name_entry = create_form_field("Display Name:", 2, user["display_name"] if user else "")
        self.phone_entry = create_form_field("Phone:", 4, user["phone"] if user else "")
        self.email_entry = create_form_field("Email:", 6, user["email"] if user else "")

        ttk.Label(popup, text="Roles:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        roles_combobox = ttk.Combobox(popup, textvariable=roles_var,state="readonly")
        roles_combobox["values"] = ("Guest", "Admin", "SuperAdmin")
        roles_combobox.grid(row=8, column=1, padx=5, pady=5)

        ttk.Checkbutton(popup, text="Enabled", variable=enabled_var).grid(row=9, column=1, sticky="w", padx=5, pady=5)

        def save_user():
            fields = [
                (self.username_entry, "username"),
                (self.display_name_entry, "display name"),
                (self.phone_entry, "phone"),
                (self.email_entry, "email")
            ]
            missing_fields = [name for entry, name in fields if not entry.get().strip()]
            if missing_fields:
                messagebox.showerror("Validation Error", f"Please fill in the following fields: {', '.join(missing_fields)}.")
                return

            new_user = {
                "id": len(self.users) + 1 if not user else user["id"],
                "username": self.username_entry.get(),
                "display_name": self.display_name_entry.get(),
                "phone": self.phone_entry.get(),
                "email": self.email_entry.get(),
                "roles": [roles_var.get()],
                "enabled": enabled_var.get()
            }

            if user:
                index = next((i for i, u in enumerate(self.users) if u["id"] == user["id"]), -1)
                if index != -1:
                    self.users[index] = new_user
            else:
                self.users.append(new_user)

            self.save_user_data()
            self.populate_user_list()
            popup.destroy()


        save_button = tk.Button(popup, text="Save"if not user else"Update", command=save_user, bg="#007BFF", fg="white",
                                font=("Helvetica", 12, "bold"), relief="flat")
        save_button.grid(row=10, column=0, columnspan=2, pady=10)

    def populate_user_list(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        for user in self.users:
            if self.hide_disabled_var.get() and not user["enabled"]:
                continue
            self.user_tree.insert('', 'end', values=(
                user["id"], user["username"], user["display_name"], user["phone"],user["email"],user["roles"] , "Yes" if user["enabled"] else "No"
            ))

    def show_popup_menu(self, event):
        selected_item = self.user_tree.identify_row(event.y)
        if selected_item:
            self.user_tree.selection_set(selected_item)
            popup_menu = tk.Menu(self, tearoff=0)
            popup_menu.add_command(label="Edit User", command=self.edit_user)
            popup_menu.add_command(label="Delete User", command=self.delete_user)
            popup_menu.post(event.x_root, event.y_root)

    def edit_user(self):
        selected_item = self.user_tree.selection()[0]
        item_values = self.user_tree.item(selected_item, "values")
        user_id = int(item_values[0])
        user = next((u for u in self.users if u["id"] == user_id), None)
        if user:
            self.open_new_user_popup(user)

    def delete_user(self):
        selected_item = self.user_tree.selection()[0]
        item_values = self.user_tree.item(selected_item, "values")
        user_id = int(item_values[0])
        self.users = [u for u in self.users if u["id"] != user_id]
        self.save_user_data()
        self.populate_user_list()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def save_user_data(self):
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(self.users, f)

    def load_user_data(self):
        try:
            with open(DATA_FILE, 'rb') as f:
                self.users = pickle.load(f)
        except FileNotFoundError:
            self.users = []

if __name__ == "__main__":
    app = UserManagementApp()
    app.mainloop()
