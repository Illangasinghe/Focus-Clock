# FocusClock

FocusClock is a simple alarm clock and Pomodoro timer application built using Python and Tkinter. It helps users set custom alarms, activate a 25-minute Pomodoro timer, and keep track of remaining time, even showing negative countdowns if the alarm is not dismissed.

## Features

- **Custom Alarms**: Set custom alarms with sound notifications to remind you to take breaks.
- **Pomodoro Timer**: Activate a 25-minute Pomodoro timer to help structure your focus and break times.
- **Remaining Time Display**: Shows the time remaining until the next alarm, including negative countdowns when the alarm is triggered.
- **Always on Top**: Toggle to keep the window on top of other windows.
- **Task Input**: Includes a text area for writing down your current task.
- **Status Bar**: Displays status messages related to alarm settings and app functionality.

## Requirements

- Python 3.x
- Required Python packages:
  - `tkinter`
  - `pygame`

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Illangasinghe/Focus-Clock.git
   cd Focus-Clock
   ```

2. **Install dependencies**:
   Install the `pygame` package if not already installed:
   ```bash
   pip install pygame
   ```

3. **Run the application**:
   ```bash
   python alarm_app.py
   ```

## How to Use

- **Set Alarm**: Click the "Set Alarm Time" button and enter the time in `HH:MM` format.
- **Start Pomodoro**: Click the "Go Pomodoro" button to start a 25-minute timer.
- **Clear Alarm**: Use the "Clear Alarm" button to reset and stop the current alarm.
- **Always on Top**: Toggle the "Always on Top" checkbox to keep the window above other windows.
- **Task Input**: Use the text box to note your current task.

## Application Components

- **Main Window**: Displays current date and time, next alarm time, remaining time, and a task input area.
- **Buttons**:
  - `Go Pomodoro`: Starts a 25-minute timer.
  - `Set Alarm Time`: Opens a dialog to set a custom alarm.
  - `Clear Alarm`: Clears the set alarm and stops any active countdown.
- **Status Bar**: Provides feedback for actions performed within the app.
  
## Bundling the App (Optional)

To create an executable version of the app, use [PyInstaller](https://www.pyinstaller.org/):
```bash
pyinstaller --onefile --windowed --add-data "cheering.wav;." alarm_app.py
```

This command creates an executable file in the `dist` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.