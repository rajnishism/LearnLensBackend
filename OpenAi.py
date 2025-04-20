from typing import List, TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from YoutubeTranscript import get_transcript_from_youtube
from PdfGenerator import PDFGeneratorReportLab
load_dotenv()
model = ChatOpenAI(model='gpt-3.5-turbo-1106')
# schema
# Define nested structure for questions
# For MCQ questions
class MCQQuestion(TypedDict):
    question: str
    options: List[str]
    answer: str

# For short answer questions
class ShortAnswerQuestion(TypedDict):
    question: str
    answer: str

# Grouping all questions
class Questions(TypedDict):
    mcq: List[MCQQuestion]
    short_answer: List[ShortAnswerQuestion]

# Final structure
class SummaryData(TypedDict):
    summary: str
    keywords: List[str]
    questions: Questions
    
    
structured_model = model.with_structured_output (SummaryData)
video_id="ukzFI9rgwfU"
transcript=get_transcript_from_youtube(video_id)
# Define your custom prompt template with variables
prompt = ChatPromptTemplate.from_template(
    "Summarize the following video transcript in clear, easy-to-understand language. Do not refer to the speaker or their actions (e.g., avoid phrases like `the speaker explains` or `the speaker compares`). Present the content as factual information. Structure the summary in coherent paragraphs followed by key bullet points for quick revision of the main ideas.{transcript}.List Down the important keywords of the video, and frame different kinds of question with answer with the given transcript for the revesion of the important concepts used in the transcript like MCQ, short question with answwers"

)
# Format the prompt with actual values
formatted_prompt = prompt.format_messages(
    transcript=transcript
)
result = structured_model.invoke(formatted_prompt)
pdf=PDFGeneratorReportLab(result, filename=video_id+".pdf")
pdf.generate()
print(result)

