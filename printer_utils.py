"""
Printer utility functions for Receipt Task Printer.
Handles printer detection, selection, and printing using win32print.
"""

import win32print
import win32ui
import win32con
from datetime import datetime
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

RECEIPT_WIDTH_MM = 80
RECEIPT_DPI = 203  # Typical for thermal printers
RECEIPT_WIDTH_PX = int(RECEIPT_WIDTH_MM / 25.4 * RECEIPT_DPI)
MARGIN_PX = 20


def list_printers() -> List[str]:
    """Return a list of available printer names."""
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    return [p[2] for p in printers]


def find_rongta_printer() -> Optional[str]:
    """Return the name of the first RONGTA printer found, or None if not found."""
    for name in list_printers():
        if 'rongta' in name.lower():
            return name
    return None


def print_task(printer_name: str, task: str, timestamp: datetime) -> None:
    """Print a single task with timestamp to the specified printer."""
    # Prepare receipt text
    time_str = timestamp.strftime('%Y-%m-%d %H:%M')
    # Use Device Context for raw printing
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        hdc.StartDoc('Receipt Task')
        hdc.StartPage()

        # Fonts
        font_time = win32ui.CreateFont({
            'name': 'Arial',
            'height': 20,
            'weight': win32con.FW_NORMAL
        })
        font_task = win32ui.CreateFont({
            'name': 'Arial',
            'height': 44,  # Increased from 40 to 44 (4 points larger)
            'weight': win32con.FW_BOLD
        })

        # Draw task (centered, large) - now at the top
        hdc.SelectObject(font_task)
        # Center horizontally
        text_size = hdc.GetTextExtent(task)
        x = max(MARGIN_PX, (RECEIPT_WIDTH_PX - text_size[0]) // 2)
        y = MARGIN_PX + 20  # Start task closer to top
        hdc.TextOut(x, y, task)

        # Draw timestamp (bottom, small)
        hdc.SelectObject(font_time)
        time_y = y + text_size[1] + 40  # Position timestamp below task
        hdc.TextOut(MARGIN_PX, time_y, time_str)

        # Add extra bottom padding by advancing the Y position and printing blank lines
        bottom_padding_px = 120  # Increased bottom padding (was less before)
        y_end = time_y + 20 + bottom_padding_px  # Add padding below timestamp
        # Optionally, draw a blank line at the bottom to force paper feed
        hdc.SelectObject(font_time)
        hdc.TextOut(MARGIN_PX, y_end, " ")

        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()
        logger.info(f"Printed task to {printer_name}: {task}")
    except Exception as e:
        logger.error(f"Failed to print task: {e}")
        raise
    finally:
        win32print.ClosePrinter(hprinter) 