from textwrap import dedent
from typing import Dict
import os

from crewai import Agent, Task, Crew, Process, LLM

from dotenv import load_dotenv          # ✅ add this
load_dotenv()


# Configure Gemini LLM for CrewAI
# This uses the GEMINI_API_KEY you set in your environment.
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
)

class ResumeMatcherCrew:
    """
    Orchestrates all agents & tasks for the Smart Resume & Job Matcher.
    Uses Gemini as the underlying LLM through CrewAI's LLM wrapper.
    """

    def __init__(self):
        # Define agents with the same Gemini LLM
        self.resume_analyst = Agent(
            role="Resume Analyst",
            goal="Extract clear, structured information from the candidate's resume.",
            backstory=dedent(
                """
                You are an experienced HR analyst who reads candidate resumes and
                extracts their skills, experience, projects and education in a structured way.
                You always respond in clean, well-organized markdown lists.
                """
            ),
            llm=gemini_llm,
            verbose=True,
            allow_delegation=False,
        )

        self.jd_analyst = Agent(
            role="Job Description Analyst",
            goal="Extract key requirements, skills, and responsibilities from a job description.",
            backstory=dedent(
                """
                You are an expert recruiter. You specialize in reading job descriptions and
                identifying must-have skills, nice-to-have skills, responsibilities and role focus.
                """
            ),
            llm=gemini_llm,
            verbose=True,
            allow_delegation=False,
        )

        self.matching_specialist = Agent(
            role="Resume-JD Matching Specialist",
            goal="Compare candidate resume and job description and compute a match score.",
            backstory=dedent(
                """
                You carefully compare a candidate's profile with a job description,
                highlight strong matches and missing skills, and calculate a numeric match score
                between 0 and 100.
                """
            ),
            llm=gemini_llm,
            verbose=True,
            allow_delegation=False,
        )

        self.interview_coach = Agent(
            role="Interview Coach",
            goal="Generate interview questions and suggested answers based on the job and candidate profile.",
            backstory=dedent(
                """
                You are an experienced technical interviewer and HR professional.
                You design tailored interview questions and give short model answers
                that help candidates prepare.
                """
            ),
            llm=gemini_llm,
            verbose=True,
            allow_delegation=False,
        )

    def build_crew(self, resume_text: str, job_description: str) -> Crew:
        # Tasks
        resume_task = Task(
            description=dedent(
                f"""
                Read the following resume text and extract:
                - Key skills
                - Programming languages / tools / frameworks
                - Work experience (with role and duration)
                - Projects
                - Education

                Resume:
                \"\"\"{resume_text}\"\"\"

                Return your answer in markdown with clear headings.
                """
            ),
            agent=self.resume_analyst,
            expected_output=(
                "A markdown section titled 'Resume Analysis' listing skills, experience, "
                "projects and education."
            ),
        )

        jd_task = Task(
            description=dedent(
                f"""
                Read the following job description and extract:
                - Required skills
                - Preferred skills
                - Key responsibilities
                - Role level (e.g., intern, junior, senior)

                Job Description:
                \"\"\"{job_description}\"\"\"

                Return your answer in markdown with clear headings.
                """
            ),
            agent=self.jd_analyst,
            expected_output="A markdown section titled 'Job Description Analysis' summarizing requirements.",
        )

        match_task = Task(
            description=dedent(
                """
                Using the 'Resume Analysis' and 'Job Description Analysis' produced earlier,
                calculate a match score between 0 and 100 and identify:

                - Strongly matched skills
                - Partially matched skills
                - Missing or weak skills
                - Short explanation of why the score was assigned.

                Output format (markdown):

                # Match Summary
                - Match Score: XX / 100

                ## Strong Matches
                - ...

                ## Partial Matches
                - ...

                ## Missing / Weak Skills
                - ...

                ## Explanation
                - 3-4 bullet points explanation.
                """
            ),
            agent=self.matching_specialist,
            expected_output="A markdown report titled 'Match Summary' with score and skill breakdown.",
            context=[resume_task, jd_task],
        )

        interview_task = Task(
            description=dedent(
                """
                Based on the previous analyses and match summary, generate tailored interview preparation:

                - 5 technical questions with short model answers
                - 3 HR / behavioral questions with suggested answers
                - 3 suggestions for how the candidate can improve their resume for this job

                Output format (markdown):

                # Interview Preparation

                ## Technical Questions
                1. Question
                   - Suggested answer: ...

                ## HR Questions
                1. Question
                   - Suggested answer: ...

                ## Resume Improvement Suggestions
                - ...
                """
            ),
            agent=self.interview_coach,
            expected_output="A markdown section titled 'Interview Preparation' with questions and suggestions.",
            context=[resume_task, jd_task, match_task],
        )

        crew = Crew(
            agents=[
                self.resume_analyst,
                self.jd_analyst,
                self.matching_specialist,
                self.interview_coach,
            ],
            tasks=[resume_task, jd_task, match_task, interview_task],
            process=Process.sequential,
            verbose=True,
        )
        return crew

    def run(self, resume_text: str, job_description: str) -> Dict[str, str]:
        """
        Runs the full pipeline and returns a dict with
        combined markdown and useful extracted pieces.
        """
        crew = self.build_crew(resume_text, job_description)
        result_markdown = crew.kickoff()

        return {
            "full_markdown": str(result_markdown),
        }
