"""
Small helper script to run the crew from the command line
for quick testing without the web UI.
"""

from crew import ResumeMatcherCrew

if __name__ == "__main__":
    resume_text = input("Paste resume text:\n")
    print("\n---\n")
    jd_text = input("Paste job description:\n")
    print("\nRunning Agentic AI Resume Matcher...\n")

    crew = ResumeMatcherCrew()
    result = crew.run(resume_text=resume_text, job_description=jd_text)

    print("\n===== FINAL RESULT (Markdown) =====\n")
    print(result["full_markdown"])
