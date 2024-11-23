import os
import time
import google.generativeai as genai
from openai import OpenAI

API_KEY = os.environ.get("GEMINI_API")
GEMINI_MODEL = "gemini-1.5-flash"
OUTPUT_FILENAME = "output.md"
NUMBER_OF_QUESTIONS = 1


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

    cult_name = cultist.generate_content("What's the cult name? Don't be mysterious, just tell me straight up.")
    cult_name = cult_name.text

    interviewer = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction="""
        You are a journalist, you own a little notebook that you scrible on.
        You want to learn more about a cult, and you will be interviewing one of its founding members.
        You are to ask questions about the cult and learn everything you can about it.
        """,
    )

    interview_text = ""
    transcript = ""
    the_question = interviewer.generate_content(
        "Ask the first question, also explain who and where you are, the surroundings and time of the day."
    )
    interview_text += f"Interviewer: {the_question.text}"
    transcript += the_question.text + "\n"

    for _ in range(NUMBER_OF_QUESTIONS):
        response = cultist.generate_content(the_question.text)
        interview_text += f"Cultist: {response.text}"
        transcript += response.text + "\n\n"

        # Is this doing anything?
        genai.embed_content(
            model="models/text-embedding-004",
            content=response.text,
        )

        the_question = interviewer.generate_content(
            f"This was answer: {response.text}. Ask one single follow up question",
        )
        interview_text += f"Interviewer: {the_question.text}"
        transcript += the_question.text + "\n"

        # TODO: I can do this better
        time.sleep(10)

    reporter = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=f"""
        You are another reporter, you picked up on the recordings of an interview. You will write up all that you learned using deduction.

        Here is the transcript:
        {transcript}
        """,
    )

    the_answer = reporter.generate_content("What did you learn? Be detailed")
    reporter_text = f"Reporter: {the_answer.text}"

    last_reply = cultist.generate_content(
        "20 years after the interview, what happend to you and the interviewer? Reply with a matter of fact answer, no mystery please. Explain the location and time of day too"
    )

    future_text = f"20 years later...\n{last_reply.text}"

    images = []
    if os.environ.get("IMAGE_GEN"):
        cult_image = cultist.generate_content(
            "Describe a specific piece of art that was drawn by one of the cult members that best describes the cult"
        )
        img = generate_image(cult_image.text)
        images.append(f"![]({img}) \n_Fig 1. Art found in cult's HQ_")
        # print(f"Prompt for image: {cult_imagery.text}")


    #### BOOK ####

    cultist.generate_content(
        generation_config=genai.types.GenerationConfig(
            # Only one candidate for now.
            candidate_count=1,
            max_output_tokens=8192,
        ),
    )

    write_book(cult_name, book_text, interview_text, reporter_text, future_text, images)
    print("Book printed")


def write_book(cult_name: str, book: str, interview_text: str, reporter_text: str, future_text: str, images: list) -> None:
    with open(OUTPUT_FILENAME, "w") as output_file:
        output_file.write(f"# {cult_name}\n")
        output_file.write("\n## The Interview\n")
        output_file.write(interview_text)
        output_file.write("\n## Reporter Notes\n")
        output_file.write(reporter_text)
        output_file.write("\n## Annex\n")
        for img in images:
            output_file.write(img)
        output_file.write("\n\n")
        output_file.write(future_text)


def generate_image(prompt: str) -> str:
    """
    Generate an image and return the URL of it
    """
    client = OpenAI()
    response = client.images.generate(model="dall-e-3", prompt=prompt)
    return response.data[0].url


if __name__ == "__main__":
    main()
