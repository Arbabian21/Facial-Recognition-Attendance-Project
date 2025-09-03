**Title:** Facial Recognition Attendance Tracker (Python + OpenCV)
**Overview:** Real-time webcam face recognition for classroom attendance with per-day CSV logs and duplicate-proof marking.

### Features

* Face encoding of known students from `/ImagesStudents` (JPG/PNG/WEBP/BMP)
* Live recognition via webcam; draws bounding boxes & labels
* One-click logging → `Attendance/YYYY-MM-DD.csv` (Name,Time)
* Duplicate protection (no double marks per session)
* Robust I/O: invalid images skipped with warnings; no-face images ignored
* macOS camera **AVFoundation** fallback + clear permission hints

### Getting Started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Place labeled images in ImagesStudents/, e.g. "Alice Smith.jpg"
python AttendanceTracker.py
# Press 'q' to quit
```

### Project Structure

```
ImagesStudents/        # known faces (file name = label)
Attendance/            # auto-created daily CSVs (YYYY-MM-DD.csv)
AttendanceTracker.py   # main app
```

### Notes

* Uses 0.25x frames for speed; boxes re-scaled to full frame.
* Skips files with no detectable face; prints `[WARN]` messages with index & path.
* Permissions: macOS → System Settings → Privacy & Security → Camera.

### Roadmap

* Persist “already marked” across app restarts (e.g., hash of CSV lines)
* CLI flags: camera index, scale, tolerance threshold
* Export to Google Sheets / SQLite
* Unit tests for encoding & CSV logic

