import streamlit as st
import json
import groq


MODELS = [
    "deepseek-r1-distill-llama-70b",
    "gemma2-9b-it",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "llama-3.3-70b-versatile",
    "llama-guard-3-8b",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768"
]
def analyze_job_fit(client, json_data, job_description):
    prompt = f"""
    As an expert resume analyst, create a comprehensive optimization strategy for the given JSON resume data to match the job description. Your task:

    1. Parse the JSON resume thoroughly, extracting all key sections: work experience, skills, education, and projects.
    2. Map resume sections directly to job description requirements.
    3. Identify exact skill and experience matches.
    4. Determine the most relevant professional experiences.
    5. Create a targeted alignment strategy.
    6. Suggest relevant keywords from the job description to be added where appropriate.
    7. Propose a new arrangement of sections (especially projects and skills) to better match the job description.

    Important: Do not remove any information from the original JSON data. Instead, focus on rearranging and enhancing the content.

    Resume Data:
    {json.dumps(json_data)}

    Job Description:
    {job_description}

    Provide a structured, data-driven optimization strategy, including:
    1. Skill overlap percentage
    2. Recommended content modifications
    3. Suggested keyword additions
    4. Proposed section rearrangement
    5. A 3-line summary (tailored to the role):
       → This is the candidate's elevator pitch. Highlight their biggest achievements and skills that prove they're the right fit for the role. Make it sound natural, as if the candidate wrote it themselves. Be formal but conversational. Don't mention specific company names.

    For the summary, focus on making it sound authentic, human, and tailored to the specific role. Use the candidate's voice and perspective.

    Additionally, suggest how to consolidate skills sections if there are multiple, aiming for about 5 main categories under skills. Don't combine all sections, but identify opportunities to group related skills effectively.

    Emphasize the importance of keywords throughout the optimization strategy.
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.2
    )
    
    return response.choices[0].message.content

def optimize_latex_resume(client, job_analysis, original_latex, json_data,selected_model):
    prompt = f"""
    As an expert resume writer with 15 years of experience, optimize the given LaTeX resume based on the job analysis and JSON data. Your task:

    1. Generate a complete, ready-to-use LaTeX code for the optimized resume.
    2. Use the existing LaTeX template as a base, but modify it according to the optimization strategy.
    3. Incorporate all data from the JSON, rearranging sections as suggested in the job analysis.
    4. Add relevant keywords from the job description where appropriate, ensuring high keyword density.
    5. Include the 3-line summary at the top of the resume, formatted appropriately in LaTeX.
    6. Ensure no information from the original JSON is omitted.
    7. Consolidate skills sections as suggested in the job analysis, aiming for about 5 main categories.

    Follow these specific rules:
    - Preserve the overall style and formatting of the original template.
    - Reorder sections based on job relevance.
    - Use exact phrases from the JSON data where possible.
    - Maximize keyword matching with the job description.
    - Optimize section weights according to the job analysis.
    - Ensure the skills section is well-organized and keyword-rich.
    - Rearrange the projects and skills sections to better match the job description and if needed try to remove atmost 1 irrelevant projects.

    Job Fit Analysis: {job_analysis}
    Original LaTeX Template: {original_latex}
    JSON Resume Data: {json.dumps(json_data)}

    Provide the complete, optimized LaTeX code ready for compilation only the code no comments or explanations.
    """

    response = client.chat.completions.create(
        model=selected_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=8000,
        temperature=0.1
    )
    
    return response.choices[0].message.content

def evaluate_resume(client, original_latex, optimized_latex, job_description, selected_model):
    prompt = f"""
    Provide a concise, data-driven comparison of the original and optimized resumes. 
    Focus on key improvements and use a structured format. Compare:
    1. Keyword match percentage
    2. Section relevance
    3. Achievement descriptions
    4. Professional positioning
    5. Job description alignment

    Provide a brief, quantitative assessment with clear, measurable improvements.
    Highlight top 3 key enhancements and any potential areas for further refinement.

    Original Resume: {original_latex}
    Optimized Resume: {optimized_latex}
    Job Description: {job_description}
    """

    response = client.chat.completions.create(
        model=selected_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.1
    )
    
    return response.choices[0].message.content


def main():
    st.set_page_config(page_title="Multi-Agent Resume Optimizer", layout="wide")
    
    st.title("🚀 Multi-Agent Resume Optimization")

    # Sidebar configuration
    with st.sidebar:
        uploaded_json = st.file_uploader("Upload Resume JSON", type=['json'])
        groq_api_key = st.text_input("Groq API Key", type="password")
        selected_model = st.selectbox("Select Model for Optimization & Evaluation", MODELS)

    # Main content area
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Job Description")
        job_description = st.text_area("Paste Job Description", height=300)

    with col2:
        st.subheader("LaTeX Template")
        latex_template = st.text_area("Paste LaTeX Template", height=300)

    with col3:
        st.subheader("Resume Preview")
        if uploaded_json:
            resume_data = json.load(uploaded_json)
            st.json(resume_data, expanded=False)

    # Optimize button
    if st.button("Optimize Resume", use_container_width=True):
        if not all([uploaded_json, job_description, latex_template, groq_api_key]):
            st.error("Please complete all inputs")
            return

        try:
            client = groq.Client(api_key=groq_api_key)

            # Agent 1: Job Fit Analysis (using default model)
            with st.spinner("Analyzing Job Fit..."):
                job_fit_analysis = analyze_job_fit(client, resume_data, job_description)
                st.subheader("Job Fit Analysis")
                st.markdown(job_fit_analysis)

            # Agent 2: LaTeX Optimization (using selected model)
            with st.spinner(f"Optimizing LaTeX Resume using {selected_model}..."):
                optimized_latex = optimize_latex_resume(
                    client, job_fit_analysis, latex_template, resume_data, selected_model
                )
                st.subheader("Optimized LaTeX Resume")
                st.code(optimized_latex, language="latex")
                #st.latex(optimized_latex)

            # Agent 3: Comparative Evaluation (using selected model)
            with st.spinner(f"Evaluating Optimization using {selected_model}..."):
                resume_evaluation = evaluate_resume(
                    client, latex_template, optimized_latex, job_description, selected_model
                )
                st.subheader("Optimization Evaluation")
                
                # Create a table for easy comparison
                import pandas as pd
                
                # Parse the evaluation to extract key metrics
                evaluation_lines = resume_evaluation.split('\n')
                
                # Create a comparison DataFrame
                comparison_data = {
                    'Metric': [
                        'Keyword Match Percentage', 
                        'Section Relevance', 
                        'Achievement Descriptions', 
                        'Professional Positioning', 
                        'Job Description Alignment'
                    ],
                    'Original': ['Low', 'Generic', 'Standard', 'Generic', 'Partial'],
                    'Optimized': [line.split(':')[1].strip() for line in evaluation_lines if ':' in line][:5]
                }
                
                comparison_df = pd.DataFrame(comparison_data)
                
                # Use Streamlit to display the table
                st.table(comparison_df)
                
                # Add a text summary of key improvements
                st.markdown("### Key Improvements")
                st.markdown(resume_evaluation)

            # Download options
            st.download_button(
                label="Download Optimized LaTeX Resume",
                data=optimized_latex,
                file_name="optimized_resume.tex",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
