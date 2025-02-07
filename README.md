
# Resume & Cover Letter Optimizer

## Overview
An AI-powered tool that intelligently crafts resumes and cover letters using multiple LLM agents. The tool analyzes your complete professional profile in JSON format and selectively uses relevant information to match specific job descriptions.

## Core Features
- Smart profile-to-job matching
- Selective information highlighting
- Resume optimization in LaTeX
- Automated cover letter generation
- Performance evaluation metrics

## How It Works

### 1. Profile Analysis
- Analyzes complete user profile JSON
- Selectively picks relevant experiences and skills
- Creates tailored professional summary
- Identifies key matching points with job description

### 2. Resume Generation
- Uses built-in LaTeX template
- Selectively presents most relevant information
- Optimizes content order and keywords
- Maintains professional formatting

### 3. Cover Letter Creation
- 4-paragraph professional structure
- Highlights most relevant achievements
- Built-in LaTeX template
- Maintains consistent branding

## Usage
1. Prepare your complete profile in JSON format (sample format is provided as sample.json)
2. Input target job description
3. Select preferred LLM model
4. Generate tailored documents

## Required Files
- `profile.json`: Your complete professional profile (sample format is provided as sample.json)
- Groq API key 

## Available Models
```
deepseek-r1-distill-llama-70b
gemma2-9b-it
llama-3.2-1b-preview
llama-3.2-3b-preview
llama-3.3-70b-versatile
llama-guard-3-8b
llama3-70b-8192
mixtral-8x7b-32768
```

## Quick Start
```bash
# Install dependencies
pip install streamlit groq

# Run the application
streamlit run app.py
```
