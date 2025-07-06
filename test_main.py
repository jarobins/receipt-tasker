#!/usr/bin/env python3
"""
Unit tests for Receipt Task Printer application.
Tests core GUI functionality for M0 milestone.
"""

import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
import sys
import os

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ReceiptTaskApp

# Patch printer_utils for all tests
import printer_utils
from unittest.mock import patch


class TestReceiptTaskApp(unittest.TestCase):
    """Test cases for the ReceiptTaskApp class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.patcher_list = patch('printer_utils.list_printers', return_value=['RONGTA 80mm', 'Other Printer'])
        self.patcher_find = patch('printer_utils.find_rongta_printer', return_value='RONGTA 80mm')
        self.patcher_print = patch('printer_utils.print_task')
        self.mock_list = self.patcher_list.start()
        self.mock_find = self.patcher_find.start()
        self.mock_print = self.patcher_print.start()
        self.app = ReceiptTaskApp(self.root)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.patcher_list.stop()
        self.patcher_find.stop()
        self.patcher_print.stop()
        self.root.destroy()
    
    def test_initial_state(self):
        """Test that the application initializes with correct initial state."""
        self.assertEqual(len(self.app.tasks), 0)
        self.assertEqual(self.app.task_listbox.size(), 0)
        self.assertEqual(self.app.status_var.get(), "Ready - Enter tasks to begin")
    
    def test_add_task(self):
        """Test adding a task to the list."""
        test_task = "Test task"
        
        # Simulate entering text and clicking add button
        self.app.task_entry.insert(0, test_task)
        self.app._add_task()
        
        # Verify task was added
        self.assertEqual(len(self.app.tasks), 1)
        self.assertEqual(self.app.tasks[0], test_task)
        self.assertEqual(self.app.task_listbox.size(), 1)
        self.assertIn(test_task, self.app.task_listbox.get(0))
    
    def test_add_empty_task(self):
        """Test that empty tasks are not added."""
        initial_count = len(self.app.tasks)
        
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            self.app._add_task()
            
            # Verify warning was shown and no task was added
            mock_warning.assert_called_once()
            self.assertEqual(len(self.app.tasks), initial_count)
    
    def test_add_task_too_long(self):
        """Test that tasks longer than 100 characters are rejected."""
        long_task = "A" * 101
        
        self.app.task_entry.insert(0, long_task)
        
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            self.app._add_task()
            
            # Verify warning was shown and no task was added
            mock_warning.assert_called_once()
            self.assertEqual(len(self.app.tasks), 0)
    
    def test_remove_selected_task(self):
        """Test removing a selected task."""
        # Add a task first
        self.app.tasks.append("Test task")
        self.app.task_listbox.insert(tk.END, "1. Test task")
        
        # Select the first item
        self.app.task_listbox.selection_set(0)
        
        # Remove the selected task
        self.app._remove_selected()
        
        # Verify task was removed
        self.assertEqual(len(self.app.tasks), 0)
        self.assertEqual(self.app.task_listbox.size(), 0)
    
    def test_remove_no_selection(self):
        """Test removing when no task is selected."""
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app._remove_selected()
            
            # Verify info message was shown
            mock_info.assert_called_once()
    
    def test_clear_all_tasks(self):
        """Test clearing all tasks."""
        # Add some tasks
        self.app.tasks.extend(["Task 1", "Task 2", "Task 3"])
        for i, task in enumerate(self.app.tasks, 1):
            self.app.task_listbox.insert(tk.END, f"{i}. {task}")
        
        # Mock the confirmation dialog to return True
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app._clear_all()
            
            # Verify all tasks were cleared
            self.assertEqual(len(self.app.tasks), 0)
            self.assertEqual(self.app.task_listbox.size(), 0)
    
    def test_clear_all_empty_list(self):
        """Test clearing when no tasks exist."""
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app._clear_all()
            
            # Verify info message was shown
            mock_info.assert_called_once()
    
    def test_update_ui_state_with_tasks(self):
        """Test UI state when tasks are present."""
        # Add a task
        self.app.tasks.append("Test task")
        self.app._update_ui_state()
        
        # Verify buttons are enabled
        self.assertEqual(str(self.app.print_button.cget('state')), 'normal')
        self.assertEqual(str(self.app.clear_button.cget('state')), 'normal')
        self.assertEqual(str(self.app.remove_button.cget('state')), 'normal')
    
    def test_update_ui_state_no_tasks(self):
        """Test UI state when no tasks are present."""
        # Ensure no tasks
        self.app.tasks.clear()
        self.app._update_ui_state()
        
        # Verify buttons are disabled
        self.assertEqual(str(self.app.print_button.cget('state')), 'disabled')
        self.assertEqual(str(self.app.clear_button.cget('state')), 'disabled')
        self.assertEqual(str(self.app.remove_button.cget('state')), 'disabled')
    
    def test_refresh_listbox(self):
        """Test refreshing the listbox display."""
        # Add some tasks
        self.app.tasks.extend(["Task 1", "Task 2"])
        
        # Refresh the listbox
        self.app._refresh_listbox()
        
        # Verify correct display
        self.assertEqual(self.app.task_listbox.size(), 2)
        self.assertIn("1. Task 1", self.app.task_listbox.get(0))
        self.assertIn("2. Task 2", self.app.task_listbox.get(1))

    def test_printer_dropdown_populates_and_selects_rongta(self):
        """Test that the printer dropdown populates and selects RONGTA by default."""
        self.assertIn('RONGTA 80mm', self.app.printer_combo['values'])
        self.assertEqual(self.app.printer_var.get(), 'RONGTA 80mm')

    def test_print_tasks_success(self):
        """Test printing all tasks successfully clears the list and shows info dialog."""
        self.app.tasks = ['Task 1', 'Task 2']
        for i, task in enumerate(self.app.tasks, 1):
            self.app.task_listbox.insert(tk.END, f"{i}. {task}")
        self.app.printer_var.set('RONGTA 80mm')
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app._print_tasks()
            self.assertEqual(len(self.app.tasks), 0)
            self.assertEqual(self.app.task_listbox.size(), 0)
            mock_info.assert_called_with("Print Complete", "All 2 tasks printed successfully.")

    def test_print_tasks_with_error(self):
        """Test printing with a printer error shows error dialog and does not clear tasks."""
        self.app.tasks = ['Task 1']
        self.app.task_listbox.insert(tk.END, "1. Task 1")
        self.app.printer_var.set('RONGTA 80mm')
        self.mock_print.side_effect = Exception("Printer jam")
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app._print_tasks()
            self.assertEqual(len(self.app.tasks), 1)
            self.assertEqual(self.app.task_listbox.size(), 1)
            mock_error.assert_called()

    def test_print_tasks_no_printer_selected(self):
        """Test printing with no printer selected shows error dialog."""
        self.app.printer_var.set('')
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app._print_tasks()
            mock_error.assert_called_with("No Printer", "Please select a printer before printing.")

    def test_print_tasks_no_tasks(self):
        """Test printing with no tasks shows info dialog."""
        self.app.tasks.clear()
        self.app.printer_var.set('RONGTA 80mm')
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app._print_tasks()
            mock_info.assert_called_with("No Tasks", "There are no tasks to print.")


class TestMainFunction(unittest.TestCase):
    """Test cases for the main function."""
    
    @patch('tkinter.Tk')
    @patch('tkinter.messagebox.showerror')
    def test_main_function_success(self, mock_error, mock_tk):
        """Test successful application startup."""
        # Mock the Tkinter root
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        # Mock the ReceiptTaskApp to avoid actual GUI creation
        with patch('main.ReceiptTaskApp') as mock_app_class:
            mock_app = MagicMock()
            mock_app_class.return_value = mock_app
            
            # Import and run main
            from main import main
            main()
            
            # Verify Tk was called and mainloop was started
            mock_tk.assert_called_once()
            mock_root.mainloop.assert_called_once()
    
    @patch('tkinter.Tk')
    @patch('tkinter.messagebox.showerror')
    def test_main_function_exception(self, mock_error, mock_tk):
        """Test application startup with exception."""
        # Mock Tk to raise an exception
        mock_tk.side_effect = Exception("Test error")
        
        # Import and run main
        from main import main
        main()
        
        # Verify error dialog was shown
        mock_error.assert_called_once()


if __name__ == '__main__':
    unittest.main() 