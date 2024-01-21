import json
import random


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}


def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def get_answer(question, json_files, last_joke_index):
    question_lower = question.lower()

    for json_file_path in json_files:
        knowledge_base = load_json(json_file_path)

        # Check if the question is related to fun facts
        if 'fun fact' in question_lower or 'fun facts' in question_lower:
            fun_facts = knowledge_base.get('fun fact', [])
            return random.choice(fun_facts) if fun_facts else None, None

        # Check if the question is related to jokes
        elif 'joke' in question_lower:
            jokes = knowledge_base.get('joke', [])
            if jokes:
                # If last joke index is not set or exceeds the number of jokes, get a new random one
                new_joke_index = random.choice(list(range(len(jokes)))) \
                    if last_joke_index is None or last_joke_index >= len(jokes) else (last_joke_index + 1) % len(jokes)
                return jokes[new_joke_index], new_joke_index
            else:
                return None, None

        # Check if the exact question is present in keys
        elif question_lower in knowledge_base:
            return knowledge_base[question_lower], None
        # If not, check if there is a numerical key matching the question
        elif question_lower.isnumeric() and int(question_lower) in knowledge_base:
            return knowledge_base[int(question_lower)], None

    return None, None


def teach_bot(question, answer, knowledge_base, json_file_path):
    knowledge_base[question.lower()] = answer  # Convert question to lowercase when storing
    save_json(json_file_path, knowledge_base)


def main():
    json_files = ['knowledge_base.json', 'knowledge_math.json', 'knowledge_fun_facts.json',
                  'knowledge_humor.json', 'knowledge_life.json']

    last_joke_index = None  # Initialize the last joke index to None
    asked_for_joke = False  # Flag to track whether the user has asked for a joke

    try:
        while True:
            user_input = input("You: ")

            if user_input.lower() == 'exit':
                print("Exiting the Chat bot. Have a great day!")
                break

            if 'fun fact' in user_input.lower() or 'fun facts' in user_input.lower():
                fun_fact = get_answer('fun fact', ['knowledge_fun_facts.json'], last_joke_index)[0]
                if fun_fact is not None:
                    print(f"Bot: {fun_fact}")
                    asked_for_joke = False  # Reset the flag when providing a fun fact
            elif 'joke' in user_input.lower():
                joke, last_joke_index = get_answer('joke', ['knowledge_humor.json'], last_joke_index)
                if joke is not None:
                    print(f"Bot: {joke}")
                    asked_for_joke = True  # Set the flag when providing a joke
            elif "tell me another one" in user_input.lower() and asked_for_joke:
                joke, last_joke_index = get_answer('joke', ['knowledge_humor.json'], last_joke_index)
                if joke is not None:
                    print(f"Bot: {joke}")
            else:
                existing_answer, _ = get_answer(user_input, json_files, last_joke_index)
                if existing_answer is not None:
                    print(f"Bot: {existing_answer}")
                    asked_for_joke = False  # Reset the flag when providing an existing answer
                else:
                    json_file_path = input("You: In which JSON file do you want to store this information? ")
                    knowledge_base = load_json(json_file_path)
                    answer = input("You: What's the correct answer? ")
                    teach_bot(user_input, answer, knowledge_base, json_file_path)
                    asked_for_joke = False  # Reset the flag when teaching a new answer
    except KeyboardInterrupt:
        print("\nExiting the Chat bot. Have a great day!")


if __name__ == "__main__":
    main()
