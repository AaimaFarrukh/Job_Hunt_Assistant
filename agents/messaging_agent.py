from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

llm =ChatGoogleGenerativeAI(
    model= 'gemini-2.5-flash',
    temperature=0.5,
    google_api_key=GEMINI_API_KEY,
    max_retries=0
)
def get_messaging_agent():
    return Agent(
        verbose= True,
        llm= llm, 
        role= "Personalized Ouutreach Messages Writer",
        goal="Draft personalized messages for job outreach",
        backstory="You're a professional career coach skilled in writing effective cold emails and outreach messages for job seekers in tech and government."
    )
def create_messaging_task(agent, jd_summary, agency_name, user_bio):
    return Task(
        description=f"""
        Write a friendly and professional outreach message.

        Agency: {agency_name}

        Job Summary:
        {jd_summary}

        Candidate Bio:
        {user_bio}

        Constraints:
        - Under 120 words
        - Suitable for LinkedIn or email
        """,
        agent=agent,
        expected_output="A short professional outreach message."
    )