from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key=GEMINI_API_KEY,
    max_retries=0
)
def get_resume_cl_agent():
    return Agent(
        role="Resume and Cover Letter Writer",
        goal="Customize application material to match job descriptions",
        backstory="You are an expert in professional writing and tailoring resumes job applications, especially in government and tech roles.",
        llm =llm,
        verbose= True
    )
def create_resume_cl_task(agent, jd_summary,resume_text):
    return Task(
        description=f"""
        Using the job summary below, tailor the candidate's application.

        Job Summary:
        {jd_summary}

        Candidate Resume:
        {resume_text[:700]}

        Generate:
        1. Resume professional summary (3–4 lines)
        2. Short government-style cover letter
        """,
                expected_output="""
        <<RESUME_SUMMARY>>
        ...

        <<COVER_LETTER>>
        ...
        """,
                agent=agent,
        output_file='/data/resume_agent_output.txt'
    )