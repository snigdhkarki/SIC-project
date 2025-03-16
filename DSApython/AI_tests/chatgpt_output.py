# Define known subjects for our input sentences.
known_subjects = {"Ram", "Hari", "Sita", "Gita", "Ramesh", "Basanta"}

input_info = ('Ram eats banana. Hari fights lion. Sita eats apple. '
              'Gita shoots lion. Ramesh throws laptop. Ram smashes banana. '
              'Basanta eats banana. Ram eats apple. Hari hits Gita. Hari falls. '
              # Some example sentences with adjectives/adverbs:
              'Happy Ram eats banana. Ram eats ripe banana. '
              'Sita quickly eats apple. Angry Hari slowly fights lion. '
              'Basanta quickly eats ripe banana.')
input_info = input_info.strip()
list_of_sentences = [s.strip() for s in input_info.split(".") if s.strip()]

# Function to extract S, V, and O from a sentence's word list.
def extract_SVO(word_list):
    info = {"subject": None, "verb": None, "object": None,
            "mod_subject": [], "adv": None, "mod_object": []}
    # Identify subject: first occurrence of a known subject.
    subject_idx = None
    for i, token in enumerate(word_list):
        if token in known_subjects:
            subject_idx = i
            info["subject"] = token
            # If any tokens before subject, treat them as subject adjectives/modifiers.
            if i > 0:
                info["mod_subject"] = word_list[:i]
            break
    if subject_idx is None:
        # If no known subject is found, assume first word is subject.
        subject_idx = 0
        info["subject"] = word_list[0]

    # Determine verb.
    # We assume verb comes right after subject or after an intervening adverb.
    verb_idx = subject_idx + 1
    if verb_idx < len(word_list):
        # Check if this token looks like an adverb (heuristic: ends with 'ly').
        if word_list[verb_idx].endswith("ly"):
            info["adv"] = word_list[verb_idx]
            verb_idx += 1
        if verb_idx < len(word_list):
            info["verb"] = word_list[verb_idx]
        else:
            info["verb"] = None
    else:
        info["verb"] = None

    # Determine object.
    # For sentences with no object (e.g. S+V) the length might be subject_idx+2 or less.
    # Otherwise, we assume the last token is the object.
    if len(word_list) > verb_idx + 1:
        # If there is a token before the last token that looks like a modifier (e.g., adjective for object)
        # we store it in mod_object.
        if len(word_list) - verb_idx > 1:
            # All tokens after verb except the very last are considered modifiers for the object.
            info["mod_object"] = word_list[verb_idx+1:-1]
        info["object"] = word_list[-1]
    else:
        info["object"] = None

    return info

# Build a list of parsed sentences and a dictionary mapping core words to sentence indices.
parsed_sentences = []
dict_of_relation = {}

for idx, sentence in enumerate(list_of_sentences):
    tokens = sentence.split()
    parsed = extract_SVO(tokens)
    parsed_sentences.append(parsed)
    
    # For each core element, map the word (in its canonical form) to the sentence index.
    for role in ["subject", "verb", "object"]:
        word = parsed[role]
        if word:
            if word in dict_of_relation:
                if idx not in dict_of_relation[word]:
                    dict_of_relation[word].append(idx)
            else:
                dict_of_relation[word] = [idx]
                
    # Also index any adverbs or modifiers if needed.
    if parsed["adv"]:
        adv = parsed["adv"]
        if adv in dict_of_relation:
            if idx not in dict_of_relation[adv]:
                dict_of_relation[adv].append(idx)
        else:
            dict_of_relation[adv] = [idx]
    for mod in (parsed["mod_subject"] + parsed["mod_object"]):
        if mod in dict_of_relation:
            if idx not in dict_of_relation[mod]:
                dict_of_relation[mod].append(idx)
        else:
            dict_of_relation[mod] = [idx]

# Debug: Print parsed sentences (optional)
# for i, info in enumerate(parsed_sentences):
#     print(f"Sentence {i}: {info}")

# Example question answering
question = "What does Hari do?"  # You can try with various questions.
question = question.strip(" ?")
question_word_list = question.split()
# Extend the list to guarantee index access in our tests.
question_word_list.extend(["", "", "", ""])

if question_word_list[0] == "Explain" and question_word_list[1] == "all" and question_word_list[2] == "occuring":
    # E.g., "Explain all occuring eats" will print all sentences with that verb.
    for idx in dict_of_relation.get(question_word_list[3], []):
        print(list_of_sentences[idx])
elif question_word_list[0] == "What" and question_word_list[1]=="is" and question_word_list[2] == "done" and question_word_list[3] =="to":
    # E.g., "What is done to banana"
    for idx in dict_of_relation.get(question_word_list[4], []):
        print(list_of_sentences[idx])
elif question_word_list[0] == "What" and question_word_list[1]=="does" and question_word_list[3]=="do" and len(question_word_list) >= 6:
    # E.g., "What does Ram do to apple" (pattern: S+V+...+O)
    sentences_with_both = list(set(dict_of_relation.get(question_word_list[2], [])) & set(dict_of_relation.get(question_word_list[5], [])))
    for idx in sentences_with_both:
        # additional check: subject must match
        if parsed_sentences[idx]["subject"] == question_word_list[2]:
            print(list_of_sentences[idx])
elif question_word_list[0] == "What" and question_word_list[1] == "does" and question_word_list[3] == "do":
    # E.g., "What does Hari do?"
    for idx in dict_of_relation.get(question_word_list[2], []):
        print(list_of_sentences[idx])
elif (question_word_list[0] in ["What", "Who"]) and question_word_list[1] == "does":
    # E.g., "Who does Ram eat?" or "What does Ram eat?"
    sentences_with_both = list(set(dict_of_relation.get(question_word_list[2], [])) & set(dict_of_relation.get(question_word_list[3], [])))
    for idx in sentences_with_both:
        if parsed_sentences[idx]["subject"] == question_word_list[2]:
            print(list_of_sentences[idx])
elif (question_word_list[0] in ["What", "Who"]) and question_word_list[1] == "is" and (
      question_word_list[2].endswith("ed") or question_word_list[2].endswith("en") or question_word_list[2].endswith("t")):
    # E.g., "What is eaten?" — derive base form (simple heuristic).
    if question_word_list[2].endswith("ed"):
        verb = question_word_list[2][:-2]
    elif question_word_list[2].endswith("en"):
        verb = question_word_list[2][:-2]
    else:
        verb = question_word_list[2]
    # In our dictionary we may have the verb in present form, so we try verb + "s" if needed.
    for idx in dict_of_relation.get(verb+"s", []):
        # For these questions we print the object.
        if parsed_sentences[idx]["object"]:
            print(parsed_sentences[idx]["object"])
else:
    # Default: Assume pattern like "Who eats?" meaning S+V.
    for idx in dict_of_relation.get(question_word_list[1], []):
        print(parsed_sentences[idx]["subject"])
