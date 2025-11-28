from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import pdfplumber

from crew import ResumeMatcherCrew

UPLOAD_FOLDER = "uploads"
# We actually only support PDF and TXT in the code below
ALLOWED_EXTENSIONS = {"pdf", "txt"}

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_file = request.files.get("resume")
        job_description = request.form.get("job_description", "").strip()

        # Basic validations
        if not resume_file or resume_file.filename == "":
            flash("Please upload a resume file.", "danger")
            return redirect(url_for("index"))

        if not job_description:
            flash("Please paste the job description.", "danger")
            return redirect(url_for("index"))

        if not allowed_file(resume_file.filename):
            flash("Unsupported file type. Please upload PDF or TXT.", "danger")
            return redirect(url_for("index"))

        # Save uploaded file
        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        resume_file.save(filepath)

        # ✅ Read resume text (TXT or PDF)
        try:
            if filename.lower().endswith(".txt"):
                # Plain text file
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    resume_text = f.read()

            elif filename.lower().endswith(".pdf"):
                # Extract text from PDF using pdfplumber
                with pdfplumber.open(filepath) as pdf:
                    pages_text = []
                    for page in pdf.pages:
                        text = page.extract_text() or ""
                        pages_text.append(text)
                resume_text = "\n".join(pages_text).strip()

                if not resume_text:
                    raise ValueError("No readable text found in PDF.")

            else:
                # Any other extension should not reach here because of ALLOWED_EXTENSIONS,
                # but just in case:
                flash(
                    "Currently only PDF and TXT resumes are supported. "
                    "Please upload your resume as PDF or TXT.",
                    "danger",
                )
                return redirect(url_for("index"))

        except Exception as e:
            flash(f"Error reading resume: {e}", "danger")
            return redirect(url_for("index"))

        # Run the Agentic AI crew
        crew = ResumeMatcherCrew()
        result = crew.run(resume_text=resume_text, job_description=job_description)

        return render_template("result.html", result=result, job_description=job_description)

    # GET request -> show form
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
