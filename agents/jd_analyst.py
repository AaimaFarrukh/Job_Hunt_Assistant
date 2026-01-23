from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=GEMINI_API_KEY,
    max_retries=0
)
def get_jd_analyst_agent():
    return Agent(
        role="JD Analyst",
        goal="Understand and summarize government job postings",
        backstory="You're an expert in job market analysis with a focus on US federal job listings.",
        llm=llm,
        verbose=True
    )
def create_jd_analysis_task(agent, job_description):
    return Task(
        description=f"""
        Summarize this USAJobs posting in a very concise way.

        Return ONLY:
        - 5 bullet points responsibilities
        - 5 bullet points required skills
        - Any eligibility or clearance (if mentioned)

        Job Description:
        {job_description[:1800]}
        """,
                expected_output="""
        <<JD_SUMMARY>>
        Responsibilities:
        - ...
        Skills:
        - ...
        Eligibility:
        - ...
        """,
        agent=agent,
        output_file='/data/report.md'
    )