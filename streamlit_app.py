import streamlit as st
from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline

st.set_page_config(page_title="AI Job Hunt Assistant", layout="centered")

st.title("AI Job Hunt Assistant")
st.markdown("Use AI agents to analyze jobs, tailor your resume, and write outreach messages — all from one interface.")

# Input fields
keyword = st.text_input("Job Keyword")
location = st.text_input("Location", "New York")
resume_text = st.text_area("Paste Your Resume", height=200)
user_bio = st.text_area("Short Bio (for outreach tone)", "I’m a data professional passionate about public service.")

if st.button("Run Job Hunt Assistant"):
    job = fetch_usajobs(keyword, location, results_per_page=5)
    if not job:
        st.error("No job postings found for this search.")
    else:
        st.session_state["jobs"] = job
        st.success("Jobs fetched! Select the ones you'd like to apply for")

if "jobs" in st.session_state:
    selected_indexes =[]
    st.markdown("### Select Jobs to Apply For")
    for i, job in enumerate(st.session_state["jobs"]):
        job_data = job['MatchedObjectDescriptor']
        job_title = job_data.get("PositionTitle", "Unknown")
        org = job_data.get('OrganizationName', 'Unknown Agency')
        checkbox = st.checkbox(f"{job_title} — {org}", key=f"job_{i}")
        if checkbox:
            selected_indexes.append(i)
    if st.button("Apply to Selected Job"):
        if not selected_indexes:
            st.warning("Please select at least one job.")
        elif not resume_text.strip():
            st.warning("Please paste your resume before applying.")
        else:
            for i in selected_indexes:
                job_data = st.session_state["jobs"][i]['MatchedObjectDescriptor']
                with st.spinner(f"Applying to: {job_data.get('PositionTitle')}"):
                    #st.markdown(f"{job_data.get('PositionTitle')}")
                    result = run_pipeline(job_data, resume_text, user_bio)
                    st.markdown("---")
                    st.markdown(f"### The reach-out message for: {job_data.get('PositionTitle')}")
                    st.markdown("#### Resume Summary")
                    st.text(result["resume_summary"])

                    st.markdown("#### Cover Letter")
                    st.text(result["cover_letter"])

                    st.markdown("#### Outreach Message")
                    st.text(result["outreach_message"])

