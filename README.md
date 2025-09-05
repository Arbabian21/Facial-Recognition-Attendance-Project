# Facial Recognition Attendance Tracker (Python + OpenCV)

**Overview:** Real-time webcam face recognition for classroom attendance with per-day CSV logs and duplicate-proof marking.

## Features

* Face encoding of known students from `/ImagesStudents` (JPG/PNG/WEBP/BMP)
* Live recognition via webcam; draws bounding boxes & labels
* One-click logging → `Attendance/YYYY-MM-DD.csv` (Name, Time)
* Duplicate protection (no double marks per session)
* Robust I/O: invalid images skipped with warnings; no-face images ignored
* macOS camera **AVFoundation** fallback + clear permission hints

---

## Setup

### 1) Prerequisites

* **macOS** (tested) with Python 3.10+
* Xcode Command Line Tools:

  ```bash
  xcode-select --install
  ```
* (If you hit `dlib` build issues) CMake available:

  ```bash
  brew install cmake
  ```

### 2) Create & activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

If you have a `requirements.txt`, do:

```bash
pip install -r requirements.txt
```

If not, this minimal set works for most Macs:

```bash
pip install opencv-python face_recognition numpy pillow
```

> If `face_recognition` warns about models, also run:

```bash
pip install git+https://github.com/ageitgey/face_recognition_models
```

### 4) Grant camera permission (macOS)

First run will prompt for camera usage. If you denied it, enable via:
**System Settings → Privacy & Security → Camera → Terminal / VSCode → ON**

---

## How to Label Photos (Very Important)

1. Put **at least one** clear, front-facing photo per student into `ImagesStudents/`.
2. **File name = label shown on screen & in CSV.** Use the student’s full name.

   * Examples:

     * `ImagesStudents/Alice Smith.jpg`
     * `ImagesStudents/Bob-Jones.png`
3. You may add **multiple photos per student** to improve accuracy. Use any suffix:

   * `Alice Smith (1).jpg`, `Alice Smith classroom.png`, etc.
     All files that start with the same base name will map to the same label.
4. Tips for best results:

   * Even lighting, face \~straight at camera, no heavy sunglasses.
   * Crop out busy backgrounds if possible.
   * Aim for at least 200×200px faces; higher is fine.

---

## Running the Program

```bash
# 1) Activate venv (if not already)
source .venv/bin/activate

# 2) Ensure your labeled images are in ImagesStudents/
#    e.g., ImagesStudents/Alice Smith.jpg

# 3) Start the tracker
python AttendanceTracker.py

# 4) Controls
#    q : quit
```

**Output:**

* A daily CSV is created at `Attendance/YYYY-MM-DD.csv` with columns: `Name, Time`.
* Each known student is marked **once per app session** (duplicate-proof).

---

## How It Works (Quick)

1. **Encode known faces** from `ImagesStudents/` at startup. Files with no detectable face are skipped and logged as `[WARN]`.
2. **Capture frames** from the webcam (downscaled to 0.25× for speed).
3. **Detect & match** faces against encodings; draw boxes/labels on the live video.
4. **Log attendance** the first time a label appears that day (per session), writing to `Attendance/YYYY-MM-DD.csv`.

---

## Project Structure

```
ImagesStudents/        # known faces (file name = label)
Attendance/            # auto-created daily CSVs (YYYY-MM-DD.csv)
AttendanceTracker.py   # main app
requirements.txt       # (optional) pinned deps
```

---

## Notes & Tips

* Uses 0.25× frames for speed; boxes re-scaled to full frame.
* Skips files with no detectable face; prints `[WARN]` messages with index & path.
* If you see `IndexError: list index out of range` during encoding, that image likely had **no detectable face**—remove/replace it.
* If OpenCV can’t open the camera, pass an explicit device index in code (e.g., `cv2.VideoCapture(0)` → `cv2.VideoCapture(1)` for an external cam).

---

## Troubleshooting

* **macOS camera blocked:** Re-enable in **System Settings → Privacy & Security → Camera**.
* **dlib build errors:**

  * Ensure `brew install cmake` was done.
  * Use Python 3.10–3.12.
  * Try a clean venv and reinstall `face_recognition`.
* **No faces recognized:**

  * Try better/larger training photos.
  * Add 2–3 images per student in different lighting.
  * Reduce tolerance in code (stricter matching) or increase if false negatives appear.

---

## Future Goals (Proof-of-Concept → Product)

These are **out of scope for this PoC**, but ideal for a robust v1:

1. **GUI Application**

   * Cross-platform GUI (PyQt / Tkinter): live preview, start/stop, status bar.
   * Buttons for “Export CSV,” “Refresh Encodings,” device selection, and tolerance slider.
   * Inline warnings panel for skipped images and permission prompts.

2. **Persistence & Robustness**

   * Persist “already marked” across restarts (e.g., store a hash or a same-day cache file).
   * Cache face encodings on disk to avoid re-encoding images each run.
   * Graceful handling when `ImagesStudents/` is empty (UI prompt + link to folder).

3. **Configuration & CLI**

   * CLI flags: `--camera-index`, `--scale 0.25`, `--tolerance 0.6`, `--save-video`.
   * Config file (`config.toml`) to persist defaults per machine.

4. **Data Destinations**

   * Export to **Google Sheets** (gspread) or **SQLite** for historical analytics.
   * Optional CSV → Sheets sync with retries and offline queue.

5. **Accuracy & Performance**

   * Support multiple cameras.
   * Batch detection every N frames; track faces between frames to reduce re-compute.
   * Optional higher-quality detectors (retinaface/mediapipe) as a toggle.

6. **Admin Tools**

   * Image quality checker (flag blurry/occluded photos).
   * “Relabel” utility to quickly rename files in `ImagesStudents/`.

7. **Testing & CI**

   * Unit tests for encoding, matching, and CSV logging.
   * Sample fixtures with synthetic faces; precommit hooks for linting/format.

---

## Example `requirements.txt` (optional)

```
opencv-python
face_recognition
numpy
pillow
```

> If you still see model warnings:

```
git+https://github.com/ageitgey/face_recognition_models
```
