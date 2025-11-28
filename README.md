# Smart Resume & Job Matcher (Agentic AI + Flask + CrewAI)

This project is a **web‑based Agentic AI application** built for lab evaluation.

It uses:

- **Flask** for the web interface
- **CrewAI** for multi‑agent orchestration
- A set of agents:
  - Resume Analyst
  - Job Description Analyst
  - Matching Specialist
  - Interview Coach

## Features

1. Upload a **resume file** (PDF/TXT/DOCX).
2. Paste a **job description**.
3. Agents:
   - Analyze resume
   - Analyze JD
   - Compute match score & skill gaps
   - Generate interview questions and model answers
4. Results are shown as markdown‑style text in the browser.

> NOTE: For simplicity in this lab version, non‑TXT resume files are not fully parsed;
> they are passed as file path text so the LLM can still infer context. In a real
> project, you would add proper PDF/DOCX parsing.

## Project Structure

```text
.
├── app.py                # Flask web app
├── crew.py               # CrewAI agents & tasks
├── main.py               # CLI runner for quick testing
├── config
│   ├── agents.yaml       # Optional agent config (not strictly required by crew.py)
│   └── tasks.yaml        # Optional task config (documentation)
├── templates
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static
│   └── css
│       └── style.css
├── requirements.txt
└── README.md
```

## Setup & Run

1. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
# or
venv\Scripts\activate         # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your LLM API key (example using OpenAI):

```bash
export OPENAI_API_KEY="your-key-here"   # Linux / macOS
set OPENAI_API_KEY=your-key-here        # Windows (cmd)
$env:OPENAI_API_KEY="your-key-here"     # Windows (PowerShell)
```

4. Run the Flask app:

```bash
python app.py
```

5. Open your browser at:

```text
http://127.0.0.1:5000/
```

## Viva / Lab Explanation Points

- This project demonstrates **Agentic AI**:
  - Multiple specialized agents (HR‑style roles)
  - Sequential process: Resume → JD → Matching → Interview Prep
- It uses **Flask** as the web framework (fulfilling "web‑based project" requirement).
- Clearly explain each agent's role and how the `Crew` orchestrates them.

You can extend it further by:
- Adding real PDF/DOCX parsers
- Displaying the match score visually (progress bar)
- Exporting the report as a PDF.
