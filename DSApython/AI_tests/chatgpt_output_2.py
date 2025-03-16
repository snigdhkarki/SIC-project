# List of known subjects.
known_subjects = {"Ram", "Hari", "Sita", "Gita", "Ramesh", "Basanta"}

# Input sentences include one sentence for each required form.
input_info = (
    "Happy Ram eats banana. "            # (a) adj+S+V+O
    "Ram eats ripe banana. "              # (b) S+V+adj+O
    "Sita quickly eats apple. "           # (c) S+adv+V+O
    "Angry Hari slowly fights lion. "     # (d) adj+S+adv+V+O
    "Basanta quickly eats ripe banana. "  # (e) S+adv+V+adj+O
    "Sad Gita shoots fierce lion. "       # (f) adj+S+V+adj+O
    "Joyful Ramesh eagerly throws heavy laptop."  # (g) adj+S+adv+V+adj+O
)

# Clean and split the input sentences.
input_info = input_info.strip()
list_of_sentences = [s.strip() for s in input_info.split(".") if s.strip()]

# Function to extract Subject, Verb, and Object along with modifiers.
def extract_SVO(word_list):
    info = {"subject": None, "verb": None, "object": None,
            "mod_subject": [], "adv": None, "mod_object": []}
    # Find the subject: first token in known_subjects.
    subject_idx = None
    for i, token in enumerate(word_list):
        if token in known_subjects:
            subject_idx = i
            info["subject"] = token
            # All words before the subject are subject modifiers.
            if i > 0:
                info["mod_subject"] = word_list[:i]
            break
    if subject_idx is None:
        subject_idx = 0
        info["subject"] = word_list[0]
    
    # Identify the verb: normally right after the subject or after an adverb.
    verb_idx = subject_idx + 1
    if verb_idx < len(word_list):
        # If the token looks like an adverb (ends with "ly"), store it.
        if word_list[verb_idx].endswith("ly"):
            info["adv"] = word_list[verb_idx]
            verb_idx += 1
        if verb_idx < len(word_list):
            info["verb"] = word_list[verb_idx]
        else:
            info["verb"] = None
    else:
        info["verb"] = None

    # Identify the object.
    # If there are extra tokens after the verb, assume the last token is the object.
    if len(word_list) > verb_idx + 1:
        # Tokens between the verb and the object are object modifiers.
        if len(word_list) - verb_idx > 1:
            info["mod_object"] = word_list[verb_idx+1:-1]
        info["object"] = word_list[-1]
    elif len(word_list) == verb_idx + 1:
        info["object"] = word_list[-1]
    else:
        info["object"] = None

    return info

# Parse each sentence and build a dictionary mapping core words to sentence indices.
parsed_sentences = []
dict_of_relation = {}

for idx, sentence in enumerate(list_of_sentences):
    tokens = sentence.split()
    parsed = extract_SVO(tokens)
    parsed_sentences.append(parsed)
    
    # Index core elements (subject, verb, object).
    for role in ["subject", "verb", "object"]:
        word = parsed[role]
        if word:
            dict_of_relation.setdefault(word, []).append(idx)
    
    # Also index the adverb if present.
    if parsed["adv"]:
        dict_of_relation.setdefault(parsed["adv"], []).append(idx)
    # Index any modifiers for subject and object.
    for mod in (parsed["mod_subject"] + parsed["mod_object"]):
        dict_of_relation.setdefault(mod, []).append(idx)

# Define a list of questions with different forms.
questions = [
    "What does Ram do?",                     # Pattern: What does S do? (should return sentences with Ram)
    "Who does Hari fight?",                   # Pattern: Who does S V? (should return sentence with Hari fighting lion)
    "What is done to banana?",                # Pattern: What is done to O? (should return sentences containing 'banana')
    "Explain all occuring eats",              # Pattern: Explain all occuring V (verb: eats)
    "What does Basanta do to banana?",        # Pattern: What does S do to O? (Basanta and banana intersection)
    "Who does Sita eat?",                     # Pattern: Who does S V? (Sita's sentences)
    "What does Ramesh do?",                   # Pattern: What does S do? (Ramesh' sentence)
    "Who does Gita shoot?"                    # Pattern: Who does S V? (Gita's sentence)
]

print("Parsed Sentences:")
for i, ps in enumerate(parsed_sentences):
    print(f"{i}: {ps}")
print("\n--- Question Answers ---\n")

# Process each question.
for question in questions:
    print("Question:", question)
    # Remove trailing punctuation and split.
    question = question.strip(" ?")
    question_word_list = question.split()
    # Extend the list so that we can safely index.
    question_word_list.extend(["", "", "", "", ""])
    
    # Case: "Explain all occuring <verb>"
    if (question_word_list[0] == "Explain" and question_word_list[1] == "all" and 
        question_word_list[2] == "occuring"):
        verb = question_word_list[3]
        for idx in dict_of_relation.get(verb, []):
            print(" -", list_of_sentences[idx])
    # Case: "What is done to <object>" 
    elif (question_word_list[0] == "What" and question_word_list[1]=="is" and 
          question_word_list[2] == "done" and question_word_list[3] =="to"):
        obj = question_word_list[4]
        for idx in dict_of_relation.get(obj, []):
            print(" -", list_of_sentences[idx])
    # Case: "What does <subject> do to <object>"  
    elif (question_word_list[0] == "What" and question_word_list[1]=="does" and 
          question_word_list[3]=="do" and len(question_word_list) >= 6 and question_word_list[5] != ""):
        subject = question_word_list[2]
        obj = question_word_list[5]
        # Intersection of sentences that contain both the subject and object.
        sentences_with_both = list(set(dict_of_relation.get(subject, [])) & set(dict_of_relation.get(obj, [])))
        for idx in sentences_with_both:
            if parsed_sentences[idx]["subject"] == subject:
                print(" -", list_of_sentences[idx])
    # Case: "What does <subject> do?"  
    elif (question_word_list[0] == "What" and question_word_list[1] == "does" and 
          question_word_list[3] == "do"):
        subject = question_word_list[2]
        for idx in dict_of_relation.get(subject, []):
            print(" -", list_of_sentences[idx])
    # Case: "Who/What does <subject> <verb>?" e.g., "Who does Hari fight?" or "What does Gita shoot?"
    elif (question_word_list[0] in ["What", "Who"] and question_word_list[1] == "does"):
        subject = question_word_list[2]
        verb = question_word_list[3]
        sentences_with_both = list(set(dict_of_relation.get(subject, [])) & set(dict_of_relation.get(verb, [])))
        for idx in sentences_with_both:
            if parsed_sentences[idx]["subject"] == subject:
                print(" -", list_of_sentences[idx])
    # Default: Assume a pattern like "Who eats?" where the question word (e.g., "Who") is followed by a verb.
    else:
        verb = question_word_list[1]
        for idx in dict_of_relation.get(verb, []):
            print(" -", parsed_sentences[idx]["subject"])
    
    print()  # Blank line between questions
