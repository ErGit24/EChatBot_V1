import json
import random

# Funktion til at indlæse JSON-data fra en fil
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

# Funktion til at gemme JSON-data til en fil
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Funktion til at få svar på et spørgsmål
def get_answer(question, json_files, last_joke_index):
    question_lower = question.lower()

    for json_file_path in json_files:
        knowledge_base = load_json(json_file_path)

        # Tjek om spørgsmålet handler om sjove facts
        if 'fun fact' in question_lower or 'fun facts' in question_lower:
            fun_facts = knowledge_base.get('fun fact', [])
            return random.choice(fun_facts) if fun_facts else None, None

        # Tjek om spørgsmålet handler om jokes
        elif 'joke' in question_lower:
            jokes = knowledge_base.get('joke', [])
            if jokes:
                # Hvis det sidste joke-indeks ikke er sat eller overstiger antallet af jokes, få et nyt tilfældigt
                new_joke_index = random.choice(list(range(len(jokes)))) \
                    if last_joke_index is None or last_joke_index >= len(jokes) else (last_joke_index + 1) % len(jokes)
                return jokes[new_joke_index], new_joke_index
            else:
                return None, None

        # Tjek om det præcise spørgsmål er til stede som nøgler
        elif question_lower in knowledge_base:
            return knowledge_base[question_lower], None
        # Hvis ikke, tjek om der er en numerisk nøgle, der matcher spørgsmålet
        elif question_lower.isnumeric() and int(question_lower) in knowledge_base:
            return knowledge_base[int(question_lower)], None

    return None, None

# Funktion til at lærer chatbotten
def teach_bot(question, answer, json_files, last_joke_index):
    print("Tilgængelige JSON-filer:")
    for i, file in enumerate(json_files, start=1):
        print(f"{i}. {file}")

    choice = input("Vælg JSON-filen indtast det tilsvarende nummer: ")
    selected_json_file = json_files[int(choice) - 1]

    knowledge_base = load_json(selected_json_file)
    knowledge_base[question.lower()] = answer
    save_json(selected_json_file, knowledge_base)

# Hovedfunktionen
def main():
    json_files = ['knowledge_base.json', 'knowledge_math.json', 'knowledge_fun_facts.json',
                  'knowledge_humor.json', 'knowledge_life.json']

    last_joke_index = None
    asked_for_joke = False

    try:
        while True:
            user_input = input("You: ")

            # Tjek om brugeren ønsker at afslutte
            if user_input.lower() == 'exit':
                print("Afslutter chatbotten. Hav en fantastisk dag!")
                break

            # Tjek om brugeren spørger efter sjove facts
            if 'fun fact' in user_input.lower() or 'fun facts' in user_input.lower():
                fun_fact = get_answer('fun fact', json_files, last_joke_index)[0]
                if fun_fact is not None:
                    print(f"Bot: {fun_fact}")
                    asked_for_joke = False  # Nulstil flaget ved levering af en sjov faktum
            # Tjek om brugeren spørger efter en vittighed
            elif 'joke' in user_input.lower():
                joke, last_joke_index = get_answer('joke', json_files, last_joke_index)
                if joke is not None:
                    print(f"Bot: {joke}")
                    asked_for_joke = True  # Sæt flaget ved levering af en vittighed
            # Tjek om brugeren vil have en anden vittighed
            elif "tell me another one" in user_input.lower() and asked_for_joke:
                joke, last_joke_index = get_answer('joke', json_files, last_joke_index)
                if joke is not None:
                    print(f"Bot: {joke}")
            else:
                existing_answer, _ = get_answer(user_input, json_files, last_joke_index)
                if existing_answer is not None:
                    print(f"Bot: {existing_answer}")
                    asked_for_joke = False  # Nulstil flaget ved levering af et eksisterende svar
                else:
                    # Hvis botten ikke kender svaret, spørg brugeren, om de vil lære det
                    print("Bot: Jeg kender ikke svaret. Vil du lære mig det?")
                    teach_choice = input("You: (Indtast 'ja' for at undervise, ellers tryk Enter): ")
                    if teach_choice.lower() == 'ja':
                        answer = input("You: Hvad er det korrekte svar? ")
                        teach_bot(user_input, answer, json_files, last_joke_index)
                        asked_for_joke = False  # Nulstil flaget ved læringen af et nyt svar
                    else:
                        print("Bot: Okay, lad mig vide, hvis der er noget andet.")
                        asked_for_joke = False  # Nulstil flaget, når brugeren vælger ikke at lærer

    except KeyboardInterrupt:
        print("\nAfslutter chatbotten. Hav en fantastisk dag!")


if __name__ == "__main__":
    main()
