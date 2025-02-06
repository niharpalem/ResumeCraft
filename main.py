import streamlit as st
import json
import groq 
import pandas as pd

MODELS = [
    "deepseek-r1-distill-llama-70b",
    "gemma2-9b-it",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "llama-3.3-70b-versatile",
    "llama-guard-3-8b",
    "llama3-70b-8192",
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
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.2
    )
    
    return response.choices[0].message.content

def optimize_latex_resume(client, job_analysis, original_latex, json_data, selected_model):
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

    Provide a short, quantitative assessment with clear, measurable improvements.
    Highlight top 3 key enhancements and any potential areas for further refinement.
    keep everything crisp and to the point.

    Original Resume: {original_latex}
    Optimized Resume: {optimized_latex}
    Job Description: {job_description}
    """

    response = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.1
    )
    
    return response.choices[0].message.content
def generate_cover_letter(client, json_data, job_description, selected_model):
    prompt = f"""
    As an expert LaTeX cover letter writer, follow these structured steps to create a professional cover letter:

    Step 1: Extract key information from job description:
    - Company name
    - Role title
    - Key responsibilities (top 3)
    - Required qualifications
    - Department/team name if mentioned
    
    Job Description for analysis:
    {job_description}

    Step 2: Analyze JSON resume to identify:
    - Most relevant experiences matching job requirements
    - Quantifiable achievements that align with role
    - Technical skills that match job needs
    - Educational background relevance
    
    Resume Data:
    {json.dumps(json_data)}

    Step 3: Generate a professional cover letter using this exact LaTeX template:

    \\documentclass[10pt,a4paper]{{letter}}
    \\usepackage[utf8]{{inputenc}}
    \\usepackage[T1]{{fontenc}}
    \\usepackage{{geometry}}
    \\usepackage{{parskip}}
    \\usepackage{{microtype}}
    \\usepackage[hidelinks]{{hyperref}}
    
    % Set margins
    \\geometry{{
        top=0.8in,
        bottom=0.8in,
        left=0.8in,
        right=0.8in
    }}
    
    \\begin{{document}}
    \\begin{{letter}}{{Hiring Manager, [Insert extracted company name here]}}
    \\opening{{Dear Hiring Manager,}}

    [Generate 4 paragraphs following this structure:]
    Paragraph 1 (Opening - 3-4 sentences):
    - Strong hook mentioning company name and role
    - Brief statement of key qualification
    - Expression of genuine interest
    
    Paragraph 2 (Experience - 4-5 sentences):
    - 2-3 most relevant achievements with metrics
    - Direct connection to job requirements
    - Demonstration of technical skills
    
    Paragraph 3 (Company Knowledge - 3-4 sentences):
    - Show research about company
    - Connect your values to company mission
    - Explain why this specific role interests you
    
    Paragraph 4 (Closing - 2-3 sentences):
    - Confident statement about contribution potential
    - Clear call to action
    - Professional thank you

    \\closing{{Sincerely,}}
    \\vspace{{-5em}}
    [Candidate full name] \\\\
    [Email] \\\\
    [Phone] \\\\
    [Location]
    \\end{{letter}}
    \\end{{document}}

    Requirements:
    1. Maximum 350 words for main content
    2. Use active voice and professional tone
    3. Include at least 3 quantifiable achievements
    4. Reference minimum 2 specific company details
    5. Maintain proper paragraph spacing
    6. Ensure all contact details match resume exactly
    7. Include relevant keywords from job description
    8. Keep technical details balanced with soft skills

    Return only the complete LaTeX code with no additional text or explanations.
    """

    response = client.chat.completions.create(
        model=selected_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.3
    )

    return response.choices[0].message.content

def main():
    st.set_page_config(page_title="Resume & Cover Letter Optimizer", layout="wide")
    
    st.title(" Resume & Cover Letter Optimization")
    
    with st.sidebar:
        uploaded_json = st.file_uploader("Upload Resume JSON", type=['json'])
        if uploaded_json is not None:
            resume_data = json.load(uploaded_json)
        else:
            st.write("Please upload a resume JSON file.")
        groq_api_key = st.text_input("Groq API Key", type="password")
        selected_model = st.selectbox("Select Model for Optimization & Evaluation", MODELS)
        
        tab_selection = st.radio("Select Document to Generate:", 
                               ["Resume", "Cover Letter", "Both"])

    st.subheader("Job Description")
    job_description = st.text_area("Paste Job Description", height=300)

    if tab_selection in ["Resume", "Both"]:
        st.subheader("LaTeX Resume Template")
        st.info("LaTeX template will be used as a base for optimization")

    if tab_selection in ["Cover Letter", "Both"]:
        st.subheader("Cover Letter Preview")
        st.info("LaTeX code will be generated automatically")

    file_path = 'latex.txt'
    with open(file_path, 'r') as f:
        latex_template = f.read()

    if st.button("Generate Documents", use_container_width=True):
        if not all([uploaded_json, job_description, groq_api_key]):
            st.error("Please complete all required inputs")
            return
        try:
            client = groq.Client(api_key=groq_api_key)

            if tab_selection in ["Resume", "Both"]:
                with st.spinner("Analyzing Job Fit..."):
                    job_fit_analysis = analyze_job_fit(client, resume_data, job_description)
                    st.subheader("Job Fit Analysis")
                    st.markdown(job_fit_analysis)

                with st.spinner(f"Optimizing LaTeX Resume using {selected_model}..."):
                    optimized_latex = optimize_latex_resume(
                        client, job_fit_analysis, latex_template, resume_data, selected_model
                    )
                    st.subheader("Optimized LaTeX Resume")
                    st.code(optimized_latex, language="latex")

                with st.spinner(f"Evaluating Optimization using {selected_model}..."):
                    resume_evaluation = evaluate_resume(
                        client, latex_template, optimized_latex, job_description, selected_model
                    )
                    st.subheader("Optimization Evaluation")
                    st.markdown(resume_evaluation)

            if tab_selection in ["Cover Letter", "Both"]:
                with st.spinner("Generating LaTeX Cover Letter..."):
                    cover_letter_latex = generate_cover_letter(
                        client, resume_data, job_description, selected_model
                    )
                    st.subheader("Generated LaTeX Cover Letter")
                    st.code(cover_letter_latex, language="latex")
                    
                    st.download_button(
                        label="Download LaTeX Cover Letter",
                        data=cover_letter_latex,
                        file_name="cover_letter.tex",
                        mime="text/plain"
                    )

            if tab_selection in ["Resume", "Both"]:
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
