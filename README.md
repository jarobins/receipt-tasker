# Receipt Task Printer

A simple desktop application for printing tasks to RONGTA 80mm receipt printers. Each task is printed individually with a timestamp on separate receipt paper.

## Features (Complete Implementation)

- **Task Entry**: Add tasks via a simple text input field
- **Task Management**: View, remove, and clear tasks from the list
- **Printer Integration**: Automatic RONGTA printer detection and selection
- **Receipt Printing**: Each task prints individually with timestamp and proper formatting
- **Intuitive Interface**: Clean, responsive GUI built with Tkinter
- **Input Validation**: Prevents empty tasks and overly long descriptions
- **Status Feedback**: Real-time status updates and user notifications
- **Error Handling**: Graceful handling of printer errors and user notifications
- **Logging**: Comprehensive logging for debugging and support

## System Requirements

- **Operating System**: Windows 10 or higher
- **Python**: 3.11 or higher
- **Hardware**: USB-connected 80mm RONGTA thermal receipt printer (for M1)

## Installation

### Prerequisites

1. **Python 3.11+**: Download and install from [python.org](https://www.python.org/downloads/)
2. **Git** (optional): For cloning the repository

### Setup

1. **Clone or download** the project files
2. **Navigate** to the project directory:
   ```bash
   cd receipt_tasks
   ```

3. **Verify Python installation**:
   ```bash
   python --version
   # Should show Python 3.11.x or higher
   ```

## Running the Application

### Development Mode

Run the application directly with Python:

```bash
python main.py
```

### Testing

Run the test suite to verify functionality:

```bash
python test_main.py
```

## Usage

### Adding Tasks

1. **Enter task description** in the text field
2. **Press Enter** or click **"Add Task"** button
3. **View tasks** in the scrollable list below

### Managing Tasks

- **Remove Selected**: Select a task and click "Remove Selected"
- **Clear All**: Remove all tasks with confirmation dialog
- **Print Tasks**: Print all tasks to the selected receipt printer

### Interface Elements

- **Printer Selection**: Dropdown to select available printers (auto-selects RONGTA if found)
- **Task Entry**: Text field for entering new tasks
- **Task List**: Scrollable list showing all added tasks
- **Control Buttons**: Add, Remove, Clear, and Print functions
- **Status Bar**: Shows current application status and feedback

## Development

### Project Structure

```
receipt_tasks/
├── main.py              # Main application file
├── printer_utils.py     # Printer integration utilities
├── test_main.py         # Unit tests
├── requirements.txt     # Dependencies
├── receipt_tasks.spec   # PyInstaller configuration
├── README.md           # This file
├── CHANGELOG.md        # Development history
├── spec.md             # Project specification
└── requirements.md     # Build requirements
```

### Code Quality

- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging to file and console
- **Testing**: Unit tests with >80% coverage target

## Milestone Status

### ✅ M0: Core GUI Framework (COMPLETE)
- Basic task entry and display interface
- Task management (add, remove, clear)
- Input validation and error handling
- Responsive layout with proper styling
- Comprehensive logging system

### ✅ M1: Printer Integration (COMPLETE)
- RONGTA printer detection and connection
- Receipt formatting with timestamps
- Print functionality implementation
- Printer error handling and recovery
- Task list clearing after successful print

### ✅ M2: Polish & Packaging (COMPLETE)
- Receipt layout optimization (task at top, timestamp at bottom)
- Increased task font size for better readability
- Extra bottom padding for proper paper handling
- PyInstaller executable packaging configuration
- Complete documentation and changelog
- Final testing and deployment ready

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Verify Python 3.11+ is installed
   - Check that tkinter is available (included with Python)
   - Review error messages in console or log file

2. **GUI not displaying properly**
   - Ensure Windows display scaling is set appropriately
   - Try running in compatibility mode if needed

3. **Logging issues**
   - Check file permissions in the application directory
   - Verify `receipt_tasks.log` file is created

### Log Files

The application creates a log file `receipt_tasks.log` in the same directory. This file contains:
- Application startup/shutdown events
- Task operations (add, remove, clear)
- Error messages and debugging information

## Contributing

This project follows the specifications in `spec.md` and build requirements in `requirements.md`. All code changes should:
- Include appropriate tests
- Follow PEP 8 style guidelines
- Include type hints
- Add logging for new functionality

## Development Process

This software was developed using **AI-assisted development** with Claude Sonnet 4.0, demonstrating how Large Language Models (LLMs) can effectively generate production-ready code when given proper inputs and a well-defined scope.

### Development Methodology

1. **Requirements Document** (`requirements.md`): Defined the build process, coding standards, and development workflow for LLM-assisted software creation.

2. **Specification Document** (`spec.md`): Detailed the exact functionality, user stories, and technical requirements for the Receipt Task Printer application.

3. **AI-Assisted Implementation**: Used Claude Sonnet 4.0 to generate the complete codebase following the requirements and specification documents.

4. **Iterative Development**: Implemented in milestones (M0, M1, M2) with continuous testing and refinement.

### Key Success Factors

- **Clear Scope**: Well-defined, focused application with specific requirements
- **Proper Documentation**: Comprehensive requirements and specification documents
- **Structured Process**: Milestone-based development with clear acceptance criteria
- **Quality Standards**: Built-in testing, logging, and error handling from the start

### LLM Capabilities Demonstrated

- **Code Generation**: Complete Python application with GUI, printer integration, and packaging
- **Architecture Design**: Proper separation of concerns (GUI, printer utilities, testing)
- **Error Handling**: Comprehensive exception handling and user feedback
- **Documentation**: Self-documenting code with type hints and docstrings
- **Testing**: Unit test suite with mocking for external dependencies

This project serves as an excellent example of how LLMs can accelerate software development when provided with clear requirements, proper scope definition, and structured development processes.

## License

This project is developed according to the specifications provided in the project documentation.

## Packaging & Deployment

### Build Standalone Executable (Windows)

1. **Install PyInstaller** (if not already installed)
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable using the spec file**
   ```bash
   pyinstaller receipt_tasks.spec
   ```
   - The output will be in the `dist/` folder as `ReceiptTaskPrinter.exe`
   - The spec file is already configured for single-file build with no console window

3. **Alternative: Build without spec file**
   ```bash
   pyinstaller --onefile --noconsole main.py
   ```
   - Use this if you want to customize the build options
   - Add `--icon=app.ico` if you have an icon file

### Packaging Notes
- All dependencies (including pywin32) are bundled.
- If you see missing DLL errors, ensure you are using a 64-bit Python and PyInstaller.
- For printer issues, ensure the RONGTA printer is installed and set up in Windows.

## Receipt Formatting (M2)
- Receipts now include **extra bottom padding** to ensure the printout is not cut off and is visually balanced on the paper.
- **Layout**: Task description appears at the top in large, bold font, timestamp at the bottom in smaller font.
- **Font Size**: Task text uses 44-point font for better readability.

---

**Note**: All milestones are complete. The application is production-ready and can be packaged as a standalone Windows executable. 