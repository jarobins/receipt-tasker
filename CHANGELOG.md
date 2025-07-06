# Changelog

## [M2] Polish & Packaging
- Added extra bottom padding to printed receipts for better paper handling
- Flipped receipt layout: task now appears at top, timestamp at bottom
- Increased task font size by 4 points (from 40 to 44)
- Added PyInstaller spec for Windows executable packaging
- Updated README with packaging and troubleshooting instructions
- Final polish and test pass

## [M1] Printer Integration
- Added printer selection dropdown (auto-selects RONGTA if found)
- Integrated receipt printing logic using win32print
- Each task prints individually with timestamp and formatting
- Handles and logs printer errors, notifies user
- Task list is cleared after successful print
- All new logic is covered by tests

## [M0] Core GUI Framework
- Implemented Tkinter GUI for task entry, display, removal, and clearing
- Input validation, status bar, and logging
- Unit tests for all core GUI logic 