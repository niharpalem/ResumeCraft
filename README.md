# AI Resume & Cover Letter Optimizer

## Overview
An AI-powered tool that optimizes resumes and cover letters using multiple LLM agents. The tool analyzes your JSON-formatted resume against job descriptions and generates LaTeX-formatted documents.

## Core Features
- Job fit analysis with skill mapping
- Resume optimization in LaTeX
- Automated cover letter generation
- Performance evaluation metrics

## How It Works

### 1. Job Fit Analysis
- Analyzes resume JSON against job description
- Calculates skill overlap percentage
- Creates 3-line professional summary
- Suggests keyword optimizations

### 2. Resume Generation
- Converts analysis into LaTeX format
- Preserves original template styling
- Reorganizes content for relevance
- Optimizes keyword placement

### 3. Cover Letter Creation
- 4-paragraph professional structure
- Includes quantifiable achievements
- Automatically formats in LaTeX
- Maintains consistent branding

## Usage
1. Format your resume as JSON
2. Input job description
3. Select preferred LLM model
4. Generate optimized documents

## Required Files
- `resume.json`: Your resume data
- `latex.txt`: LaTeX template
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
