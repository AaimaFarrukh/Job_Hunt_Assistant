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
    resume_task = create_resume_cl_task(resume_agent,job_summary, resume_text)
    messaging_task = create_messaging_task(messaging_agent, job_summary,agency_name, user_bio)

    crew = Crew(
        agents=[jd_agent, resume_agent, messaging_agent],
        tasks= [jd_task, resume_task, messaging_task],
        process = Process.sequential
    )
    result = crew.kickoff()
    resume_output = str(resume_task.output)
    resume_summary = extract_between_markers(resume_output, "<<RESUME_SUMMARY>>", "<<COVER_LETTER>>")
    cover_letter = extract_between_markers(resume_output, "<<COVER_LETTER>>")

    log_application(job_title, agency_name, resume_summary)
    save_cover_letter_file(job_title, cover_letter)

    print("\n=== FINAL OUTPUT ===\n")
    print(result)

    return result

if __name__ == "__main__":
    run_pipeline()