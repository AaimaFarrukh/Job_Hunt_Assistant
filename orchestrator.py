from crewai import Crew, Process
from agents.jd_analyst import get_jd_analyst_agent,create_jd_analysis_task
from usajobs_api import fetch_usajobs
from agents.resume_cl_agent import get_resume_cl_agent,create_resume_cl_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from utils.tracking import log_application, save_cover_letter_file

def extract_between_markers(text, start, end=None):
    try:
        start_idx = text.index(start) + len(start)
        end_idx = text.index(end, start_idx) if end else len(text)
        return text[start_idx:end_idx].strip()
    except ValueError:
        return "Not found"
        
def load_resume(path="data/sample_resume.txt"):
    with open(path, "r") as file:
        return file.read()
def run_pipeline(job_data, resume_text, user_bio):
    job_title = job_data["PositionTitle"]
    job_summary = job_data['UserArea']['Details']['JobSummary']
    agency_name = job_data.get('OrganizationName', 'Unknown Agency')

    job_summary = job_summary[:800]  # take first 800 characters
    resume_text = resume_text[:1500]

    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    messaging_agent = get_messaging_agent()

    jd_task = create_jd_analysis_task(jd_agent, job_summary)


    jd_crew = Crew(
        agents=[jd_agent],
        tasks= [jd_task],
        process = Process.sequential
    )
    jd_result = jd_crew.kickoff()
    jd_summary = extract_between_markers(jd_result, "<<JD_SUMMARY>>")

    resume_task = create_resume_cl_task(resume_agent,jd_summary, resume_text)
    resume_crew = Crew(
    agents=[resume_agent],
    tasks=[resume_task],
    process=Process.sequential
)

    resume_result = resume_crew.kickoff()

    messaging_task = create_messaging_task(messaging_agent, jd_summary,agency_name, user_bio)
    message_crew = Crew(
    agents=[messaging_agent],
    tasks=[messaging_task],
    process=Process.sequential
    )

    message_result = message_crew.kickoff()

    resume_output = str(resume_task.output)
    resume_summary = extract_between_markers(resume_output, "<<RESUME_SUMMARY>>", "<<COVER_LETTER>>")
    cover_letter = extract_between_markers(resume_output, "<<COVER_LETTER>>")

    log_application(job_title, agency_name, resume_summary)
    save_cover_letter_file(job_title, cover_letter)

    print("\n=== FINAL OUTPUT ===\n")
    result = {
    "jd_summary": jd_summary,
    "resume_summary": resume_summary,
    "cover_letter": cover_letter,
    "message": message_result
    }
    print(result)

    return result
