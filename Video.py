from typing import List, TypedDict
# NEW (correct):
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from PdfGenerator import PDFGeneratorReportLab
from yt_dlp import get_transcript_from_youtube
from chunking import chunk_string_by_tokens
import os

# Load environment variables
load_dotenv()

# Define structured types
class MCQQuestion(TypedDict):
    question: str
    options: List[str]
    answer: str

class ShortAnswerQuestion(TypedDict):
    question: str
    answer: str

class Questions(TypedDict):
    mcq: List[MCQQuestion]
    short_answer: List[ShortAnswerQuestion]

class SummaryData(TypedDict):
    summary: str
    keywords: List[str]
    questions: Questions

# Main function
def generate_pdf_from_youtube_video(video_id: str, lectureNo=1):
    # Initialize model with schema
    model = ChatOpenAI(model='gpt-3.5-turbo-1106', max_tokens=4000 )
    #structured_model = model.with_structured_output(SummaryData)

    # Get transcript from YouTube
    transcript = get_transcript_from_youtube(video_id)

    # Define prompt template
    prompt = ChatPromptTemplate.from_template(
    """
You are an AI assistant. I will provide you with the transcript of a YouTube tutorial video.

Your task is to extract only the **technical and factual content** from the transcript, focusing on the **core methods, processes, techniques, steps, formulas, code logic, and key concepts** discussed in the video.

Do NOT include:
- Speaker's personal opinions or experiences
- Emphasis on why something is important
- Motivational or explanatory content
- Repetition or non-technical commentary

The goal is to create **concise academic-style notes** that would help a student quickly revise the key technical points taught in the video.

Organize the output under the following headings:

- 📘 Summary (Clear bullet points or structured outline of all key learnings)
- 📌 Key Terms and Concepts (List of important terms, functions, tools, or concepts)
- 🧠 Review Questions (factual or logic-based questions to reinforce understanding)

Transcript:
\"\"\"{transcript}\"\"\"
"""
)

    ##chunking the transcript 
    result=""
    chunks= chunk_string_by_tokens(transcript)
    for chunk in chunks:
        formatted_prompt = prompt.format_messages(transcript=chunk)
        response = model.invoke(formatted_prompt)
        result+=response.content
        result+="\n"
    
    # print(result.content)

    # Generate PDF report
    pdf = PDFGeneratorReportLab(result, lectureNo, filename=f"VideoSummary/{video_id}.pdf")
    pdf.generate()
    print("✅ "+video_id+".pdf Generated")
    return True
#generate_pdf_from_youtube_video("-xSJA8-o6Eg")