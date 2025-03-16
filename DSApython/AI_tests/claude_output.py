input_info = 'Ram eats banana.Hari fights lion.Sita eats apple.\
Gita shoots lion.Ramesh throws laptop.Ram smashes banana.\
Basanta eats banana.Ram eats apple.Hari hits Gita.Hari falls.\
Clever Ram quickly eats banana.Ram eats yellow banana.\
Strong Hari angrily fights lion.Sita carefully eats ripe apple.\
Tall Gita shoots fierce lion.Young Ramesh throws old laptop.\
Hungry Ram violently smashes rotten banana.Smart Basanta quietly eats fresh banana.'

input_info = input_info[:-1]
list_of_sentences = input_info.split(".")

# Enhanced data structure to store sentence components
sentence_components = []

for sentence in list_of_sentences:
    words = sentence.split(" ")
    
    # Default structure for components
    components = {
        "subject_adj": None,
        "subject": None,
        "adverb": None,
        "verb": None,
        "object_adj": None,
        "object": None,
        "original": sentence
    }
    
    # Parse sentence based on word count
    if len(words) == 3:  # Simple S+V+O
        components["subject"] = words[0]
        components["verb"] = words[1]
        components["object"] = words[2]
    elif len(words) == 2:  # Simple S+V
        components["subject"] = words[0]
        components["verb"] = words[1]
    elif len(words) == 4:
        # Could be: adj+S+V+O or S+V+adj+O or S+adv+V+O
        if words[1] in ["eats", "fights", "shoots", "throws", "smashes", "hits", "falls"]:
            # First word is adjective for subject
            components["subject_adj"] = words[0]
            components["subject"] = words[1]
            components["verb"] = words[2]
            components["object"] = words[3]
        elif words[2] in ["eats", "fights", "shoots", "throws", "smashes", "hits", "falls"]:
            # Third word is verb, so second word is adverb or first word is subject
            components["subject"] = words[0]
            components["adverb"] = words[1]
            components["verb"] = words[2]
            components["object"] = words[3]
        else:
            # Last pattern: S+V+adj+O
            components["subject"] = words[0]
            components["verb"] = words[1]
            components["object_adj"] = words[2]
            components["object"] = words[3]
    elif len(words) == 5:
        # Could be: adj+S+adv+V+O or S+adv+V+adj+O or adj+S+V+adj+O
        if words[2] in ["eats", "fights", "shoots", "throws", "smashes", "hits", "falls"]:
            # adj+S+V+adj+O
            components["subject_adj"] = words[0]
            components["subject"] = words[1]
            components["verb"] = words[2]
            components["object_adj"] = words[3]
            components["object"] = words[4]
        elif words[3] in ["eats", "fights", "shoots", "throws", "smashes", "hits", "falls"]:
            # adj+S+adv+V+O
            components["subject_adj"] = words[0]
            components["subject"] = words[1]
            components["adverb"] = words[2]
            components["verb"] = words[3]
            components["object"] = words[4]
        else:
            # S+adv+V+adj+O
            components["subject"] = words[0]
            components["adverb"] = words[1]
            components["verb"] = words[2]
            components["object_adj"] = words[3]
            components["object"] = words[4]
    elif len(words) == 6:
        # adj+S+adv+V+adj+O
        components["subject_adj"] = words[0]
        components["subject"] = words[1]
        components["adverb"] = words[2]
        components["verb"] = words[3]
        components["object_adj"] = words[4]
        components["object"] = words[5]
    
    sentence_components.append(components)

# Create index mapping for efficient search
index_map = {}
for i, components in enumerate(sentence_components):
    # Index by all components
    for key, value in components.items():
        if value and key != "original":
            if value not in index_map:
                index_map[value] = []
            index_map[value].append(i)

def process_question(question):
    question = question.strip()
    if not question.endswith("?"):
        question += "?"
    
    question_words = question[:-1].split(" ")
    question_words.extend(["", "", "", "", "", ""])  # Extend to avoid index errors
    
    results = []
    
    # Handle "Explain all occurring V"
    if question_words[0] == "Explain" and question_words[1] == "all" and question_words[2] == "occurring":
        verb = question_words[3]
        if verb in index_map:
            for idx in index_map[verb]:
                results.append(sentence_components[idx]["original"])
    
    # Handle "What is done to O?"
    elif question_words[0] == "What" and question_words[1] == "is" and question_words[2] == "done" and question_words[3] == "to":
        obj = question_words[4]
        if obj in index_map:
            for idx in index_map[obj]:
                if sentence_components[idx]["object"] == obj:
                    results.append(sentence_components[idx]["original"])
        
        # Also check for object with adjective
        for i, comp in enumerate(sentence_components):
            if comp["object"] == obj and comp["object_adj"]:
                if comp["original"] not in results:
                    results.append(comp["original"])
    
    # Handle "What does S do to O?"
    elif question_words[0] == "What" and question_words[1] == "does" and question_words[3] == "do" and question_words[4] == "to":
        subj = question_words[2]
        obj = question_words[5]
        
        # Find sentences with both subject and object
        for i, comp in enumerate(sentence_components):
            if comp["subject"] == subj and comp["object"] == obj:
                results.append(comp["original"])
    
    # Handle "What does S do?"
    elif question_words[0] == "What" and question_words[1] == "does" and question_words[3] == "do":
        subj = question_words[2]
        if subj in index_map:
            for idx in index_map[subj]:
                if sentence_components[idx]["subject"] == subj:
                    results.append(sentence_components[idx]["original"])
    
    # Handle "Who/What does S V?"
    elif (question_words[0] == "What" or question_words[0] == "Who") and question_words[1] == "does":
        subj = question_words[2]
        verb = question_words[3]
        
        for i, comp in enumerate(sentence_components):
            if comp["subject"] == subj and comp["verb"] == verb:
                if comp["object"]:
                    results.append(comp["object"])
                    # Include adjective if present
                    if comp["object_adj"]:
                        last_idx = len(results) - 1
                        results[last_idx] = f"{comp['object_adj']} {results[last_idx]}"
    
    # Handle "Who/What is Ved/Ven?"
    elif (question_words[0] == "What" or question_words[0] == "Who") and question_words[1] == "is" and (
            question_words[2].endswith("ed") or 
            question_words[2].endswith("en") or 
            question_words[2].endswith("t")):
        
        # Handle passive voice by finding the base verb
        passive_verb = question_words[2]
        base_verb = None
        
        if passive_verb.endswith("ed"):
            base_verb = passive_verb[:-2]
        elif passive_verb.endswith("en"):
            base_verb = passive_verb[:-2]
        elif passive_verb.endswith("t"):
            base_verb = passive_verb[:-1]
        
        # Add "s" to convert to third person singular present
        if base_verb:
            active_verb = base_verb + "s"
            
            for i, comp in enumerate(sentence_components):
                if comp["verb"] == active_verb and comp["object"]:
                    obj_text = comp["object"]
                    if comp["object_adj"]:
                        obj_text = f"{comp['object_adj']} {obj_text}"
                    results.append(obj_text)
    
    # Handle "Who/What V O?"
    elif (question_words[0] == "What" or question_words[0] == "Who") and question_words[1] in index_map:
        verb = question_words[1]
        obj = question_words[2] if len(question_words) > 2 and question_words[2] else None
        
        for i, comp in enumerate(sentence_components):
            if comp["verb"] == verb:
                if not obj or comp["object"] == obj:
                    subj_text = comp["subject"]
                    if comp["subject_adj"]:
                        subj_text = f"{comp['subject_adj']} {subj_text}"
                    results.append(subj_text)
    
    # Handle "Who/What V?"
    elif (question_words[0] == "What" or question_words[0] == "Who") and question_words[1] in index_map:
        verb = question_words[1]
        
        for i, comp in enumerate(sentence_components):
            if comp["verb"] == verb:
                subj_text = comp["subject"]
                if comp["subject_adj"]:
                    subj_text = f"{comp['subject_adj']} {subj_text}"
                results.append(subj_text)
    
    return results

# Example usage
questions = [
    "Who eats banana?",
    "What does Ram eat?",
    "What does Hari do to lion?",
    "What does Hari do?",
    "What is done to banana?",
    "Who falls?",
    "What is eaten?",
    "Explain all occurring eats",
    
    # New questions for enhanced structures
    "Who quickly eats banana?",
    "What does Clever Ram eat?",
    "What does Ram eat yellow?",
    "What is violently smashed?",
    "Who eats fresh banana?",
    "What does Strong Hari angrily do?",
    "What does Smart Basanta do?"
]

print("Testing various questions:")
for q in questions:
    print(f"\nQuestion: {q}")
    answers = process_question(q)
    if answers:
        for answer in answers:
            print(f"Answer: {answer}")
    else:
        print("No answer found.")