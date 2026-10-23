# Concept Pace Explorer

A small web app for students at Mahatma Phule Apang Prashikshan Kendra (Service Learning project).
It teaches simple concepts in three formats (picture, audio, story), records how each learner
responds, and uses a multi-armed bandit to learn which format and pace suits each learner.
Teachers see a plain-language profile on a dashboard.

## Run it
```
python -m venv venv
venv\Scripts\activate        # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## How it works
- `bandit.py` - epsilon-greedy bandit chooses the teaching format (explore 20%, exploit 80%)
- `db.py` - SQLite storage of anonymous interactions (time, hints, correctness)
- `lessons.py` - lesson content, add your own concepts here
- `app.py` - Flask routes; `templates/` and `static/` - the interface

## Ethics
Anonymous IDs only. Results show learning preferences, never a diagnosis. Teacher stays in the loop.

## AI assistance
The code was drafted with an AI assistant (Claude). The problem, observations at the NGO,
design decisions and testing were done by our team. See BUILD_LOG.md.

## Known limitations
Timer starts when the page loads; very small lesson set; needs ~6 answers per learner before the
dashboard summary appears.
