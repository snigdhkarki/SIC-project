# List of known subjects.
known_subjects = {"Ram", "Hari", "Sita", "Gita", "Ramesh", "Basanta"}

# Input sentences include one sentence for each required form:
# a) adj+S+V+O: "Happy Ram eats banana."
# b) S+V+adj+O: "Ram eats ripe banana."
# c) S+adv+V+O: "Sita quickly eats apple."
# d) adj+S+adv+V+O: "Angry Hari slowly fights lion."
# e) S+adv+V+adj+O: "Basanta quickly eats ripe banana."
# f) adj+S+V+adj+O: "Sad Gita shoots fierce lion."
# g) adj+S+adv+V+adj+O: "Joyful Ramesh eagerly throws heavy laptop."
input_info = (
    "Happy Ram eats banana. "            
    "Ram eats ripe banana. "              
    "Sita quickly eats apple. "           
    "Angry Hari slowly fights lion. "     
    "Basanta quickly eats ripe banana. "  
    "Sad Gita shoots fierce lion. "       
    "Joyful Ramesh eagerly throws heavy laptop."
)

# Clean and split the input sentences.
input_info = input_info.strip()
list_of_sentences = [s.strip() for s in input_info.split(".") if s.strip()]

# Function to extract core components and modifiers.
def extract_SVO(word_list):
    info = {"subject": None, "verb": None, "object": None,
            "mod_subject": [], "adv": None, "mod_object": []}
    # Identify the subject: first occurrence of a known subject.
    subject_idx = None
    for i, token in enumerate(word_list):
        if token in known_subjects:
            subject_idx = i
            info["subject"] = token
            # Words before subject are subject modifiers.
            if i > 0:
                info["mod_subject"] = word_list[:i]
            break
    if subject_idx is None:
        subject_idx = 0
        info["subject"] = word_list[0]
    
    # Identify the verb: normally right after the subject or after an adverb.
    verb_idx = subject_idx + 1
    if verb_idx < len(word_list):
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
    if len(word_list) > verb_idx + 1:
        # Tokens between verb and last token are object modifiers.
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
    
    # Index the adverb if present.
    if parsed["adv"]:
        dict_of_relation.setdefault(parsed["adv"], []).append(idx)
    # Index modifiers for subject and object.
    for mod in (parsed["mod_subject"] + parsed["mod_object"]):
        dict_of_relation.setdefault(mod, []).append(idx)

# For debugging, show parsed sentences.
print("Parsed Sentences:")
for i, ps in enumerate(parsed_sentences):
    print(f"{i}: {ps}")
print("\n--- Question Answers ---\n")

# Define a list of questions in various forms.
questions = [
    "What does Ram do?",                     # Original: What does S do?
    "Who does Hari fight?",                   # Original: Who does S V?
    "What is done to banana?",                # Original: What is done to O?
    "Explain all occuring eats",              # Original: Explain all occuring <verb>
    "What does Basanta do to banana?",        # Original: What does S do to O?
    "Who does Sita eat?",                     # Original: Who does S V?
    "What does Ramesh do?",                   # Original: What does S do?
    "Who does Gita shoot?",                   # Original: Who does S V?
    "Who eats ripe banana?",                  # New: includes adjective in object.
    "What eats fierce lion?"                  # New: "What" version returning sentence info.
]

# Process each question.
for question in questions:
    print("Question:", question)
    # Remove trailing punctuation and split.
    question = question.strip(" ?")
    question_word_list = question.split()
    # Extend to guarantee safe indexing.
    question_word_list.extend(["", "", "", "", ""])
    
    # Case 1: "Explain all occuring <verb>"
    if (question_word_list[0] == "Explain" and question_word_list[1] == "all" and 
        question_word_list[2] == "occuring"):
        verb = question_word_list[3]
        for idx in dict_of_relation.get(verb, []):
            print(" -", list_of_sentences[idx])
    
    # Case 2: "What is done to <object>"
    elif (question_word_list[0] == "What" and question_word_list[1]=="is" and 
          question_word_list[2] == "done" and question_word_list[3] =="to"):
        obj = question_word_list[4]
        for idx in dict_of_relation.get(obj, []):
            print(" -", list_of_sentences[idx])
    
    # Case 3: "What does <subject> do to <object>"  
    elif (question_word_list[0] == "What" and question_word_list[1]=="does" and 
          question_word_list[3]=="do" and len(question_word_list) >= 6 and question_word_list[5] != ""):
        subject = question_word_list[2]
        obj = question_word_list[5]
        sentences_with_both = set(dict_of_relation.get(subject, [])) & set(dict_of_relation.get(obj, []))
        for idx in sentences_with_both:
            if parsed_sentences[idx]["subject"] == subject:
                print(" -", list_of_sentences[idx])
    
    # Case 4: "What does <subject> do?"  
    elif (question_word_list[0] == "What" and question_word_list[1] == "does" and 
          question_word_list[3] == "do"):
        subject = question_word_list[2]
        for idx in dict_of_relation.get(subject, []):
            print(" -", list_of_sentences[idx])
    
    # Case 5: "Who/What does <subject> <verb>?" e.g., "Who does Hari fight?"
    elif (question_word_list[0] in ["What", "Who"] and question_word_list[1] == "does"):
        subject = question_word_list[2]
        verb = question_word_list[3]
        sentences_with_both = set(dict_of_relation.get(subject, [])) & set(dict_of_relation.get(verb, []))
        for idx in sentences_with_both:
            if parsed_sentences[idx]["subject"] == subject:
                print(" -", list_of_sentences[idx])
    
    # New Case 6: "Who/What <verb> <modifier(s)> <object>" 
    # For example: "Who eats ripe banana?" or "What eats fierce lion?"
    elif (question_word_list[0] in ["Who", "What"] and question_word_list[1] != "does"):
        qverb = question_word_list[1]
        # Assume the last token is the object core.
        qobj = question_word_list[-2] if question_word_list[-1] == "" else question_word_list[-1]
        # Any tokens between the verb and the object core are adjectives (object modifiers).
        qmods = question_word_list[2:-1] if question_word_list[-1] != "" else question_word_list[2:-2]
        
        # Intersection: sentences that have the verb and object core.
        sentences_set = set(dict_of_relation.get(qverb, [])) & set(dict_of_relation.get(qobj, []))
        # Further intersect with each modifier.
        for mod in qmods:
            if mod:  # skip empty tokens
                sentences_set &= set(dict_of_relation.get(mod, []))
        
        for idx in sentences_set:
            # Double-check: does the sentence have the verb and object exactly?
            if parsed_sentences[idx]["verb"] == qverb and parsed_sentences[idx]["object"] == qobj:
                # If question is "Who ...", answer with the subject.
                if question_word_list[0] == "Who":
                    print(" -", parsed_sentences[idx]["subject"])
                else:
                    # For "What ..." print the full sentence.
                    print(" -", list_of_sentences[idx])
    
    # Default case: Assume pattern like "Who <verb>?" (print subject(s)).
    else:
        verb = question_word_list[1]
        for idx in dict_of_relation.get(verb, []):
            print(" -", parsed_sentences[idx]["subject"])
    
    print()  # Blank line between questions
