import os
import time
import google.generativeai as genai
from openai import OpenAI

API_KEY = os.environ.get("GEMINI_API")
GEMINI_MODEL = "gemini-1.5-flash"


def main():
    genai.configure(api_key=API_KEY)

    cultist = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction="""
        You are a cultist, you've been a founding member of a cult you're a part of,
        you know almost everything about it, but some secrets are still to be discovered. The cult itself has elements of paranormal and occult.
        You are to answer questions about the cult in a mysterious way, leaving some details out. You do NOT ask questions.
        """,
    )

    interviewer = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction="""
        You are a journalist, you own a little notebook that you scrible on.
        You want to learn more about a cult, and you will be interviewing one of its founding members.
        You are to ask questions about the cult and learn everything you can about it.
        """,
    )

    transcript = ""
    the_question = interviewer.generate_content(
        "Ask the first question, also explain who and where you are, the surroundings and time of the day."
    )
    print(f"Interviewer: {the_question.text}")
    transcript += the_question.text + "\n"

    for _ in range(8):
        response = cultist.generate_content(the_question.text)
        print(f"Cultist: {response.text}")
        transcript += response.text + "\n\n"

        # Is this doing anything?
        genai.embed_content(
            model="models/text-embedding-004",
            content=response.text,
        )

        notes = interviewer.generate_content(
            f"This was answer: {response.text}. Write some notes on it",
        )
        print(f"Interviewer Notes: {notes.text}\n")

        the_question = interviewer.generate_content(
            f"This was answer: {response.text}. Ask one single follow up question",
        )
        transcript += the_question.text + "\n"
        time.sleep(10)

    print("END OF INTERVIEW\n\n---\n\n")

    reporter = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=f"""
        You are another reporter, you picked up on the recordings of an interview. You will write up all that you learned using deduction.

        Here is the transcript:
        {transcript}
        """,
    )

    the_answer = reporter.generate_content("What did you learn? Be detailed")
    print(f"Reporter: {the_answer.text}")

    last_reply = cultist.generate_content(
        "20 years after the interview, what happend to you and the interviewer? Reply with a matter of fact answer, no mystery please. Explain the location and time of day too"
    )

    print(f"20 years later...\n{last_reply.text}")

    cult_imagery = cultist.generate_content(
        "Describe a specific piece of art that was drawn by one of the cult members that best describes the cult"
    )

    print("---")
    print(generate_image(cult_imagery.text))

    print("Fig 1: Art found in the cult's HQ")
    print(f"Prompt for image: {cult_imagery.text}")


def generate_image(prompt: str) -> str:
    """
    Generate an image and return the URL of it
    """
    client = OpenAI()
    response = client.images.generate(model="dall-e-3", prompt=prompt)

    return response.data[0].url


if __name__ == "__main__":
    main()
