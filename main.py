#!/usr/bin/env python3
"""
Receipt Task Printer - Main Application
A simple GUI application for printing tasks to RONGTA receipt printers.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime
from typing import List

# Add printer_utils import
import printer_utils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('receipt_tasks.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ReceiptTaskApp:
    """Main application class for the Receipt Task Printer."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Receipt Task Printer")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
        # Initialize task storage
        self.tasks: List[str] = []
        
        # Create GUI components
        self._create_widgets()
        self._setup_layout()
        
        logger.info("Application initialized successfully")
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Receipt Task Printer", 
            font=("Arial", 16, "bold")
        )
        
        # Printer selection
        self.printer_frame = ttk.Frame(self.main_frame)
        self.printer_label = ttk.Label(self.printer_frame, text="Printer:")
        self.printer_var = tk.StringVar()
        self.printer_combo = ttk.Combobox(
            self.printer_frame,
            textvariable=self.printer_var,
            state="readonly",
            width=40
        )
        self._populate_printers()
        self.printer_combo.bind('<<ComboboxSelected>>', self._on_printer_selected)
        
        # Task entry section
        self.entry_frame = ttk.LabelFrame(self.main_frame, text="Add New Task", padding="10")
        
        self.task_entry = ttk.Entry(
            self.entry_frame, 
            width=50, 
            font=("Arial", 10)
        )
        self.task_entry.bind('<Return>', self._add_task)
        
        self.add_button = ttk.Button(
            self.entry_frame, 
            text="Add Task", 
            command=self._add_task
        )
        
        # Task list section
        self.list_frame = ttk.LabelFrame(self.main_frame, text="Task List", padding="10")
        
        # Create listbox with scrollbar
        self.listbox_frame = ttk.Frame(self.list_frame)
        
        self.task_listbox = tk.Listbox(
            self.listbox_frame,
            height=15,
            width=60,
            font=("Arial", 10),
            selectmode=tk.SINGLE
        )
        
        self.scrollbar = ttk.Scrollbar(
            self.listbox_frame, 
            orient=tk.VERTICAL, 
            command=self.task_listbox.yview
        )
        self.task_listbox.configure(yscrollcommand=self.scrollbar.set)
        
        # Control buttons
        self.button_frame = ttk.Frame(self.main_frame)
        
        self.print_button = ttk.Button(
            self.button_frame,
            text="Print Tasks",
            command=self._print_tasks,
            state=tk.DISABLED
        )
        
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Clear All",
            command=self._clear_all
        )
        
        self.remove_button = ttk.Button(
            self.button_frame,
            text="Remove Selected",
            command=self._remove_selected
        )
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Enter tasks to begin")
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
    
    def _setup_layout(self):
        """Setup the layout of all widgets."""
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        
        # Title
        self.title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Printer selection
        self.printer_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.printer_label.grid(row=0, column=0, sticky="w")
        self.printer_combo.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.printer_frame.columnconfigure(1, weight=1)
        
        # Entry frame
        self.entry_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.entry_frame.columnconfigure(0, weight=1)
        
        self.task_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.add_button.grid(row=0, column=1)
        
        # List frame
        self.list_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        self.list_frame.columnconfigure(0, weight=1)
        self.list_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        
        # Listbox with scrollbar
        self.listbox_frame.grid(row=0, column=0, sticky="nsew")
        self.listbox_frame.columnconfigure(0, weight=1)
        self.listbox_frame.rowconfigure(0, weight=1)
        
        self.task_listbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Button frame
        self.button_frame.grid(row=4, column=0, pady=(0, 10))
        
        self.print_button.grid(row=0, column=0, padx=(0, 5))
        self.clear_button.grid(row=0, column=1, padx=(0, 5))
        self.remove_button.grid(row=0, column=2)
        
        # Status bar
        self.status_bar.grid(row=5, column=0, sticky="ew")
    
    def _add_task(self, event=None):
        """Add a new task to the list."""
        task_text = self.task_entry.get().strip()
        
        if not task_text:
            messagebox.showwarning("Empty Task", "Please enter a task description.")
            return
        
        if len(task_text) > 100:
            messagebox.showwarning("Task Too Long", "Task description must be 100 characters or less.")
            return
        
        # Add task to list
        self.tasks.append(task_text)
        self.task_listbox.insert(tk.END, f"{len(self.tasks)}. {task_text}")
        
        # Clear entry and update UI
        self.task_entry.delete(0, tk.END)
        self._update_ui_state()
        
        logger.info(f"Task added: {task_text}")
        self.status_var.set(f"Task added. Total tasks: {len(self.tasks)}")
    
    def _remove_selected(self):
        """Remove the selected task from the list."""
        selection = self.task_listbox.curselection()
        
        if not selection:
            messagebox.showinfo("No Selection", "Please select a task to remove.")
            return
        
        index = selection[0]
        
        # Remove from internal list and listbox
        removed_task = self.tasks.pop(index)
        self.task_listbox.delete(index)
        
        # Refresh listbox display
        self._refresh_listbox()
        
        logger.info(f"Task removed: {removed_task}")
        self.status_var.set(f"Task removed. Total tasks: {len(self.tasks)}")
    
    def _clear_all(self):
        """Clear all tasks from the list."""
        if not self.tasks:
            messagebox.showinfo("Empty List", "No tasks to clear.")
            return
        
        result = messagebox.askyesno(
            "Clear All Tasks", 
            f"Are you sure you want to clear all {len(self.tasks)} tasks?"
        )
        
        if result:
            self.tasks.clear()
            self.task_listbox.delete(0, tk.END)
            self._update_ui_state()
            
            logger.info("All tasks cleared")
            self.status_var.set("All tasks cleared")
    
    def _refresh_listbox(self):
        """Refresh the listbox display with current task numbers."""
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks, 1):
            self.task_listbox.insert(tk.END, f"{i}. {task}")
    
    def _update_ui_state(self):
        """Update UI state based on current task count."""
        if self.tasks:
            self.print_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            self.remove_button.config(state=tk.NORMAL)
        else:
            self.print_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)
    
    def _populate_printers(self):
        """Populate the printer dropdown with available printers."""
        try:
            printers = printer_utils.list_printers()
            self.printer_combo['values'] = printers
            rongta = printer_utils.find_rongta_printer()
            if rongta:
                self.printer_var.set(rongta)
            elif printers:
                self.printer_var.set(printers[0])
            else:
                self.printer_var.set("")
        except Exception as e:
            logger.error(f"Failed to list printers: {e}")
            self.printer_combo['values'] = []
            self.printer_var.set("")
            messagebox.showerror("Printer Error", f"Could not list printers: {e}")

    def _on_printer_selected(self, event=None):
        """Handle printer selection change."""
        selected = self.printer_var.get()
        logger.info(f"Printer selected: {selected}")
        self.status_var.set(f"Printer selected: {selected}")
    
    def _print_tasks(self):
        """Print all tasks to the selected printer."""
        printer_name = self.printer_var.get()
        if not printer_name:
            messagebox.showerror("No Printer", "Please select a printer before printing.")
            return
        if not self.tasks:
            messagebox.showinfo("No Tasks", "There are no tasks to print.")
            return
        errors = []
        for i, task in enumerate(self.tasks, 1):
            try:
                printer_utils.print_task(printer_name, task, datetime.now())
            except Exception as e:
                logger.error(f"Error printing task {i}: {e}")
                errors.append((i, str(e)))
        if errors:
            msg = f"{len(errors)} task(s) failed to print. See log for details."
            messagebox.showerror("Print Error", msg)
            self.status_var.set(msg)
        else:
            messagebox.showinfo("Print Complete", f"All {len(self.tasks)} tasks printed successfully.")
            self.status_var.set(f"All {len(self.tasks)} tasks printed.")
            self.tasks.clear()
            self.task_listbox.delete(0, tk.END)
            self._update_ui_state()


def main():
    """Main entry point for the application."""
    try:
        root = tk.Tk()
        app = ReceiptTaskApp(root)
        
        # Set focus to task entry
        app.task_entry.focus()
        
        logger.info("Starting Receipt Task Printer application")
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main() 