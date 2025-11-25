import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox


class FileExplorer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Linux Command File Explorer')
        self.geometry('800x800')

        # Directory Display
        self.path_label = tk.Label(self, text="Current Directory: ")
        self.path_label.pack(pady=5)

        # Listbox to Display Files and Directories
        self.file_listbox = tk.Listbox(self, width=100, height=15)
        self.file_listbox.pack(pady=10)

        # Command Entry
        self.command_entry = tk.Entry(self, width=100)
        self.command_entry.pack(pady=5)
        self.command_entry.bind('<KeyRelease>', self.update_command_syntax)

        # Enter Button
        tk.Button(self, text="Enter", command=self.execute_command_button).pack(pady=5)

        # Command Syntax Box
        tk.Label(self, text="Command Syntax:").pack(pady=5)
        self.syntax_box = tk.Listbox(self, width=100, height=5)
        self.syntax_box.pack(pady=5)

        # Output Section
        tk.Label(self, text="Output:").pack(pady=5)
        self.output_box = tk.Listbox(self, width=100, height=10)
        self.output_box.pack(pady=10)

        # Status Bar
        self.status_label = tk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize with Current Directory
        self.current_path = os.getcwd()
        self.update_file_list()

    def update_file_list(self):
        self.path_label.config(text=f"Current Directory: {self.current_path}")
        self.file_listbox.delete(0, tk.END)
        for item in os.listdir(self.current_path):
            self.file_listbox.insert(tk.END, item)

    def execute_command_button(self):
        self.process_command(self.command_entry.get())

    def process_command(self, command_text):
        command = command_text.split()
        if not command:
            return

        action = command[0]
        try:
            if action == 'pwd':
                self.output_box.delete(0, tk.END)
                self.output_box.insert(tk.END, os.getcwd())
            elif action == 'cd':
                self.change_directory(command[1] if len(command) > 1 else None)
            elif action == 'mv':
                self.move_file(command[1], command[2] if len(command) > 2 else None)
            elif action == 'cp':
                self.copy_file(command[1], command[2] if len(command) > 2 else None)
            elif action == 'rm':
                self.delete_file(command[1])
            elif action == 'touch':
                self.create_file(command[1])
            elif action == 'cat':
                self.display_file_content(command[1])
            elif action == 'echo':
                self.echo_to_file(command_text)
            elif action == 'whoami':
                self.execute_whoami()
            elif action == 'chmod':
                self.change_permissions(command[1], command[2] if len(command) > 2 else None)
            elif action == 'mkdir':
                self.make_directory(command[1] if len(command) > 1 else None)
            elif action == 'rmdir':
                self.remove_directory(command[1] if len(command) > 1 else None)
            elif action == 'head':
                self.read_file_head(command[1])
            elif action == 'tail':
                self.read_file_tail(command[1])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_command_syntax(self, event=None):
        command_text = self.command_entry.get()
        action = command_text.split()[0] if command_text else ''
        self.show_command_syntax(action)

    def show_command_syntax(self, command):
        syntax = {
            'pwd': 'Usage: pwd',
            'cd': 'Usage: cd <directory_path>',
            'mv': 'Usage: mv <source> <destination>',
            'cp': 'Usage: cp <source> <destination>',
            'rm': 'Usage: rm <file_path>',
            'touch': 'Usage: touch <file_name>',
            'cat': 'Usage: cat <file_name>',
            'echo': "Usage: echo 'text' > <file_name>",
            'whoami': 'Usage: whoami',
            'chmod': 'Usage: chmod <mode> <file_path>',
            'mkdir': 'Usage: mkdir <directory_name>',
            'rmdir': 'Usage: rmdir <directory_name>',
            'head': 'Usage: head <file_name>',
            'tail': 'Usage: tail <file_name>',
        }
        self.syntax_box.delete(0, tk.END)
        if command in syntax:
            self.syntax_box.insert(tk.END, syntax[command])
        else:
            self.syntax_box.insert(tk.END, "Command not recognized.")

    def change_directory(self, path):
        try:
            os.chdir(path)
            self.current_path = os.getcwd()
            self.update_file_list()
            messagebox.showinfo("Success", f"Directory changed to {self.current_path}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def move_file(self, src, dest):
        try:
            shutil.move(src, dest)
            self.update_file_list()
            messagebox.showinfo("Success", f"Moved {src} to {dest}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_file(self, src, dest):
        try:
            shutil.copy(src, dest)
            self.update_file_list()
            messagebox.showinfo("Success", f"Copied {src} to {dest}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_file(self, path):
        try:
            os.remove(path)
            self.update_file_list()
            messagebox.showinfo("Success", f"Deleted {path}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_file(self, filename):
        try:
            with open(filename, 'w') as f:
                pass
            self.update_file_list()
            messagebox.showinfo("Success", f"Created file {filename}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_file_content(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            self.output_box.delete(0, tk.END)
            for line in content.splitlines():
                self.output_box.insert(tk.END, line)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def echo_to_file(self, command_text):
        try:
            split_text = command_text.split('>')
            text = split_text[0].replace("echo", "").strip().strip("'").strip('"')
            filename = split_text[1].strip()
            with open(filename, 'w') as f:
                f.write(text)
            self.update_file_list()
            messagebox.showinfo("Success", f"Content written to {filename}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def execute_whoami(self):
        try:
            result = subprocess.run(['whoami'], capture_output=True, text=True)
            if result.returncode == 0:
                self.output_box.delete(0, tk.END)
                self.output_box.insert(tk.END, result.stdout.strip())
                messagebox.showinfo("Success", "Command executed successfully.")
            else:
                messagebox.showerror("Error", result.stderr)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def change_permissions(self, mode, path):
        try:
            os.chmod(path, int(mode, 8))
            messagebox.showinfo("Success", f"Permissions for {path} changed to {mode}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def make_directory(self, directory):
        try:
            os.mkdir(directory)
            self.update_file_list()
            messagebox.showinfo("Success", f"Directory {directory} created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_directory(self, directory):
        try:
            os.rmdir(directory)
            self.update_file_list()
            messagebox.showinfo("Success", f"Directory {directory} removed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_file_head(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()[:10]  # Read the first 10 lines
            self.output_box.delete(0, tk.END)
            for line in lines:
                self.output_box.insert(tk.END, line.strip())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_file_tail(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()[-10:]  # Read the last 10 lines
            self.output_box.delete(0, tk.END)
            for line in lines:
                self.output_box.insert(tk.END, line.strip())
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()
