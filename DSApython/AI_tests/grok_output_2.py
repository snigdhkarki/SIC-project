# Input sentences (extended with modifiers for demonstration)
input_info = 'big Ram eats banana.Hari fights lion.Sita eats apple.Gita shoots lion.' \
             'Ramesh throws laptop.Ram quickly smashes banana.Basanta eats big banana.' \
             'small Ram eats apple.Hari hits Gita.big Hari quickly falls.'
input_info = input_info[:-1]  # Remove trailing period

# Split into individual sentences
list_of_SV_sentences = input_info.split(".")

# Function to parse a sentence into components
def parse_sentence(sentence):
    words = sentence.split(" ")
    
    # Find the verb (first word ending with "s")
    V_index = -1
    for i, word in enumerate(words):
        if word.endswith("s"):
            V_index = i
            break
    if V_index == -1:
        raise ValueError("No verb found in sentence")
    
    # Find the subject (closest capitalized word before verb)
    S_index = -1
    for i in range(V_index - 1, -1, -1):
        if words[i].istitle():
            S_index = i
            break
    if S_index == -1:
        raise ValueError("No subject found in sentence")
    
    # Determine object (last word after verb, if any)
    O_index = len(words) - 1 if V_index + 1 < len(words) else -1
    O = words[O_index] if O_index != -1 else None
    
    # Extract modifiers
    adj_S = words[:S_index]  # Words before subject
    adv_V = words[S_index + 1:V_index]  # Words between subject and verb
    adj_O = words[V_index + 1:O_index] if O else []  # Words between verb and object
    
    return {
        'subject': words[S_index],
        'adj_subject': adj_S,
        'verb': words[V_index],
        'adv_verb': adv_V,
        'object': O,
        'adj_object': adj_O
    }

# Parse all sentences
parsed_sentences = [parse_sentence(sentence) for sentence in list_of_SV_sentences]

# Build dictionary of relations (word to sentence indices)
dict_of_relation = {}
for i, sentence in enumerate(list_of_SV_sentences):
    words = sentence.split(" ")
    for word in words:
        if word in dict_of_relation:
            if i not in dict_of_relation[word]:
                dict_of_relation[word].append(i)
        else:
            dict_of_relation[word] = [i]


# Function to process a single question
def process_question(question, list_of_SV_sentences, parsed_sentences, dict_of_relation):
    # Clean the question: remove trailing '?' and extra spaces
    question = question.strip()
    if question.endswith('?'):
        question = question[:-1]
    if not question:
        return
    
    # Split into words and pad the list for consistent indexing
    question_word_list = question.split(" ")
    while len(question_word_list) < 10:
        question_word_list.append("")

    # Process different question types
    if question_word_list[0] in ["Who", "What"] and len(question_word_list) >= 3 and question_word_list[2] not in ["does", "is"]:
        # "Who V O?" or "What V O?" (e.g., "Who eats banana?")
        V, O = question_word_list[1], question_word_list[2]
        for index in set(dict_of_relation.get(V, [])) & set(dict_of_relation.get(O, [])):
            parsed = parsed_sentences[index]
            if parsed['verb'] == V and parsed['object'] == O:
                print(parsed['subject'])

    elif question_word_list[0] == "What" and question_word_list[1] == "does" and question_word_list[3] == "do" and question_word_list[4] == "to":
        # "What does S do to O?" (e.g., "What does Hari do to Gita?")
        S, O = question_word_list[2], question_word_list[5]
        for index in set(dict_of_relation.get(S, [])) & set(dict_of_relation.get(O, [])):
            parsed = parsed_sentences[index]
            if parsed['subject'] == S and parsed['object'] == O:
                print(parsed['verb'])

    elif question_word_list[0] == "What" and question_word_list[1] == "does" and question_word_list[3] == "do":
        # "What does S do?" (e.g., "What does Hari do?")
        S = question_word_list[2]
        for index in dict_of_relation.get(S, []):
            parsed = parsed_sentences[index]
            if parsed['subject'] == S:
                print(f"{parsed['verb']}{' ' + parsed['object'] if parsed['object'] else ''}")

    elif question_word_list[0] == "What" and question_word_list[1] == "is" and question_word_list[2] == "done" and question_word_list[3] == "to":
        # "What is done to O?" (e.g., "What is done to banana?")
        O = question_word_list[4]
        for index in dict_of_relation.get(O, []):
            parsed = parsed_sentences[index]
            if parsed['object'] == O:
                print(parsed['verb'])

    elif question_word_list[0] in ["Who", "What"] and question_word_list[1] == "does" and question_word_list[4] == "":
        # "Who/What does S V?" (e.g., "What does Ram eat?")
        S, V = question_word_list[2], question_word_list[3]
        for index in set(dict_of_relation.get(S, [])) & set(dict_of_relation.get(V, [])):
            parsed = parsed_sentences[index]
            if parsed['subject'] == S and parsed['verb'] == V:
                print(parsed['object'] or "")

    elif question_word_list[0] in ["Who", "What"] and question_word_list[1] == "is" and (question_word_list[2].endswith("ed") or question_word_list[2].endswith("en") or question_word_list[2].endswith("t")):
        # "Who/What is Ven/Ved?" (e.g., "Who is eaten?")
        verb = question_word_list[2]
        if verb.endswith("ed") or verb.endswith("en"):
            V = verb[:-2] + "s"
        else:
            V = verb + "s" if not verb.endswith("s") else verb
        for index in dict_of_relation.get(V, []):
            parsed = parsed_sentences[index]
            if parsed['verb'] == V:
                print(parsed['subject'])

    elif question_word_list[0] == "Explain" and question_word_list[1] == "all" and question_word_list[2] == "occuring":
        # "Explain all occurring V." (e.g., "Explain all occurring eats.")
        V = question_word_list[3]
        for index in dict_of_relation.get(V, []):
            print(list_of_SV_sentences[index])

    # New question types for modifiers
    elif question_word_list[0] == "What" and question_word_list[1] == "kind" and question_word_list[2] == "of" and question_word_list[4] != "does":
        # "What kind of S V O?" (e.g., "What kind of Ram eats banana?")
        S, V, O = question_word_list[3], question_word_list[4], question_word_list[5]
        for index in set(dict_of_relation.get(S, [])) & set(dict_of_relation.get(V, [])) & set(dict_of_relation.get(O, [])):
            parsed = parsed_sentences[index]
            if parsed['subject'] == S and parsed['verb'] == V and parsed['object'] == O:
                print(" ".join(parsed['adj_subject']) or "none")

    elif question_word_list[0] == "How" and question_word_list[1] == "does":
        # "How does S V O?" (e.g., "How does Ram smashes banana?")
        S, V, O = question_word_list[2], question_word_list[3], question_word_list[4]
        for index in set(dict_of_relation.get(S, [])) & set(dict_of_relation.get(V, [])) & set(dict_of_relation.get(O, [])):
            parsed = parsed_sentences[index]
            if parsed['subject'] == S and parsed['verb'] == V and parsed['object'] == O:
                print(" ".join(parsed['adv_verb']) or "none")

    elif question_word_list[0] == "What" and question_word_list[1] == "kind" and question_word_list[2] == "of" and question_word_list[4] == "does":
        # "What kind of O does S V?" (e.g., "What kind of banana does Ram eat?")
        O, S, V = question_word_list[3], question_word_list[5], question_word_list[6]
        for index in set(dict_of_relation.get(S, [])) & set(dict_of_relation.get(V, [])) & set(dict_of_relation.get(O, [])):
            parsed = parsed_sentences[index]
            if parsed['subject'] == S and parsed['verb'] == V and parsed['object'] == O:
                print(" ".join(parsed['adj_object']) or "none")

# List of 20 predefined questions
questions = [
    "Who eats banana?",
    "What does Hari do?",
    "What kind of Ram eats banana?",
    "What kind of banana does Basanta eat?",
    "How does Ram smashes banana?",
    "What is done to banana?",
    "What does Ram eat?",
    "Who fights lion?",
    "What kind of lion does Hari fight?",
    "Explain all occurring eats.",
    "What does Sita do?",
    "Who throws laptop?",
    "What kind of banana does Ram smash?",
    "How does Hari fall?",
    "What kind of Hari falls?",
    "What does Gita do to lion?",
    "Who hits Gita?",
    "What is done to apple?",
    "Who smashes banana?",
    "What does Basanta do?"
]

# Loop to process and test each question
for q in questions:
    print(f"Question: {q}")
    process_question(q, list_of_SV_sentences, parsed_sentences, dict_of_relation)
    print()  # Blank line for readability between question-answer pairs