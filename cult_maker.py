import os
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API")
genai.configure(api_key=API_KEY)

cultist = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction="""
You are a cultist, you've been a founding member of a cult you're a part of,
you know almost everything about it, but some secrets are still to be discovered.
You are to answer questions about the cult in a mysterious way, leaving some details out. You do NOT ask questions.
"""
)

interviewer = genai.GenerativeModel(
  model_name="gemini-1.5-flash-8b",
  system_instruction="""
You are a journalist, you own a little notebook that you scrible on.
You want to learn more about a cult, and you will be interviewing one of its founding members.
You are to ask questions about the cult and learn everything you can about it.
"""
)

transcript = ""
the_question = interviewer.generate_content("Ask the first question, also explain who and where you are, the surroundings and time of the day.")
print(the_question.text)
transcript += the_question.text + "\n"

for _ in range(8):
    response = cultist.generate_content(the_question.text)
    print(response.text)
    transcript += response.text + "\n\n"
    genai.embed_content(
            model="models/text-embedding-004",
            content=response.text)

    the_question = interviewer.generate_content(f"This was answer: {response.text}. Say some notes on it and ask a followup question.")
    print(the_question.text)
    transcript += the_question.text + "\n"



reporter = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction=f"""
You are a reporter, you picked up on the recordings of an interview. You will write up all that you learned using deduction.

Here is the transcript:
{transcript}
"""
)

print("END")

the_answer = reporter.generate_content("What did you learn? Be detailed")
print(the_answer.text)

last_reply = cultist.generate_content("20 years after the interview, what happend to you and the interviewer? Reply with a matter of fact answer, no mystery please. Explain the location and time of day too")

print(last_reply.text)
