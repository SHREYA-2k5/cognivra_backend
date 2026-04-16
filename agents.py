import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def call_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  # or "mistralai/mistral-7b-instruct"
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ AI Error: {str(e)}"


def summary_agent(text):
    prompt = f"""
    Summarize the document in a clean structured format.

    STRICT RULES:
    - No markdown (** or #)
    - No symbols like - or •
    - Each point on a new line
    - Use simple readable format
    - Use clear labels

    Example:
    Student Information Summary
    Name: Rajesh Kumar
    Gender: Male
    CGPA: 9.4

    Text:
    {text[:3000]}
    """
    return call_ai(prompt)

def question_agent(text, summary):
    prompt = f"""
    Analyze the document.

    If it contains explicit questions:
    → Extract ONLY those questions.

    Otherwise:
    → Generate relevant questions.

    STRICT RULES:
    - Output ONLY questions
    - No explanations
    - No intro text
    - Each question on new line
    - Do NOT include numbering

    Example:
    What is the objective of the project?
    What data is used?

    Text:
    {text[:3000]}
    """
    return call_ai(prompt)


def study_agent(text, summary):
    prompt = f"""
    Generate clean study notes.

    STRICT RULES:
    - No markdown (**, #)
    - No bullets
    - Each point on new line
    - Simple readable sentences

    Example:
    Student performance is analyzed using marks.
    Machine learning is used for prediction.

    Text:
    {text[:3000]}
    """
    return call_ai(prompt)

def chat_agent(question, context):
    return call_ai(f"Context:\n{context[:3000]}\n\nQuestion:\n{question}")