from transformers import pipeline, set_seed
import openai
     

def input_dialog() -> str:
    print("Welcome a us app!")
    prompt = input("Please type your text to complete: ")
    return prompt

def create_generator(
        prompt: str,
        seed: int,
        openai_api_key: str | None,
        model: str = "openai-gpt"
    ) -> str:

    if model == "text-davinci-002":
        openai.api_key = openai_api_key
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=15,
        n=1,
        stop=None,
        temperature=0.1
        )
        return response["choices"][0]["text"]
    else:
        generator = pipeline('text-generation', model=model)
        set_seed(seed)
        results = generator(prompt, max_length=15, num_return_sequences=1)
        if results:
            return results[0]['generated_text']
        else:
            return "Sorry something is wrong!"

    

def more_questions() -> bool:
    continuity = input("Do you wanna doing other completion? Type Y o N: ")
    if continuity == "N" or continuity == "n":
        return False
    elif continuity == "Y" or continuity == "y":
        return True
    else:
        print("Only type Y o N, for Yes o Not respectively")
        final = more_questions()
        return final


def main():
    prompt = input_dialog()
    final_text = create_generator(prompt=prompt, seed=42)
    print(final_text.capitalize())



if __name__ == "__main__":
    while True:
        main()
        next_question = more_questions()
        if not next_question:
            break
        