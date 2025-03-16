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

for sentence in sentence_components:
    print(sentence)

# Create index mapping for efficient search
index_map = {}
for i, components in enumerate(sentence_components):
    # Index by all components
    for key, value in components.items():
        if value and key != "original":
            if value not in index_map:
                index_map[value] = []
            index_map[value].append(i)

def get_full_subject(comp):
    """Helper function to get full subject with adjective if present"""
    if comp["subject_adj"]:
        return f"{comp['subject_adj']} {comp['subject']}"
    return comp["subject"]

def get_full_object(comp):
    """Helper function to get full object with adjective if present"""
    if comp["object_adj"]:
        return f"{comp['object_adj']} {comp['object']}"
    return comp["object"]

def process_question(question):
    question = question.strip()
    if not question.endswith("?"):
        question += "?"
    
    question_words = question[:-1].split(" ")
    question_words.extend(["", "", "", "", "", "", ""])  # Extend to avoid index errors
    
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
        for i, comp in enumerate(sentence_components):
            obj_full = get_full_object(comp)
            # Check if the object or full object (with adj) contains our target
            if comp["object"] == obj or obj in obj_full.split():
                results.append(comp["original"])
    
    # Handle "What does S do to O?"
    elif question_words[0] == "What" and question_words[1] == "does" and question_words[3] == "do" and question_words[4] == "to":
        subj = question_words[2]
        obj = question_words[5]
        
        # Handle case where subject might have an adjective in the question
        for i, comp in enumerate(sentence_components):
            subject_full = get_full_subject(comp)
            object_full = get_full_object(comp)
            
            # Check for subject match (either exact or with adjective)
            subject_match = False
            if comp["subject"] == subj:
                subject_match = True
            elif comp["subject_adj"] and subj == f"{comp['subject_adj']} {comp['subject']}":
                subject_match = True
            
            # Check for object match
            object_match = False
            if comp["object"] == obj:
                object_match = True
            elif comp["object_adj"] and obj in object_full:
                object_match = True
                
            if subject_match and object_match:
                results.append(comp["original"])
    
    # Handle "What does S do?"
    elif question_words[0] == "What" and question_words[1] == "does" and question_words[3] == "do":
        subj = question_words[2]
        
        # Handle cases with adjectives in subject
        for i, comp in enumerate(sentence_components):
            subject_full = get_full_subject(comp)
            
            # Check for subject match (either exact or with adjective)
            if comp["subject"] == subj or subject_full == subj or subj in subject_full:
                results.append(comp["original"])
    
    # Handle "Who/What does S V?"
    elif (question_words[0] == "What" or question_words[0] == "Who") and question_words[1] == "does":
        subj = question_words[2]
        verb = question_words[3]
        
        # Handle cases with adjectives in subject
        for i, comp in enumerate(sentence_components):
            subject_full = get_full_subject(comp)
            
            # Check for subject and verb match
            subject_match = comp["subject"] == subj or subject_full == subj or subj in subject_full
            verb_match = comp["verb"] == verb
            
            if subject_match and verb_match:
                if comp["object"]:
                    results.append(get_full_object(comp))
    
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
                    results.append(get_full_object(comp))
    
    # Handle "Who adv V O?" or "Who V adj O?"
    elif (question_words[0] == "Who" or question_words[0] == "What"):
        # Check if second word might be an adverb
        possible_adverb = question_words[1]
        possible_verb = question_words[2]
        possible_adj_or_obj = question_words[3]
        
        # Case: "Who quickly eats banana?"
        if possible_verb in index_map and possible_adverb:
            for i, comp in enumerate(sentence_components):
                if comp["verb"] == possible_verb and comp["adverb"] == possible_adverb:
                    # Check if object matches if provided
                    object_match = True
                    if possible_adj_or_obj and comp["object"] != possible_adj_or_obj:
                        # Check if it could be an object with adjective
                        if comp["object_adj"] and f"{comp['object_adj']} {comp['object']}" != f"{possible_adj_or_obj} {question_words[4]}":
                            object_match = False
                    
                    if object_match:
                        results.append(get_full_subject(comp))
        # Case: "Who eats banana?" (simple verb object)
        elif possible_adverb in index_map:
            verb = possible_adverb
            obj = possible_verb
            
            for i, comp in enumerate(sentence_components):
                if comp["verb"] == verb:
                    # Check if object matches if provided
                    object_match = True
                    if obj and comp["object"] != obj:
                        # Check if it could be an object with adjective
                        full_obj = get_full_object(comp)
                        if obj not in full_obj:
                            object_match = False
                    
                    if object_match:
                        results.append(get_full_subject(comp))
    
    # Handle "What is violently smashed?" - looking for objects with specific adverb+verb
    elif question_words[0] == "What" and question_words[1] == "is" and question_words[2] in index_map:
        adverb = question_words[2]
        passive_verb = question_words[3] if len(question_words) > 3 else ""
        
        # Convert passive to active verb form if needed
        active_verb = None
        if passive_verb:
            if passive_verb.endswith("ed"):
                active_verb = passive_verb[:-2] + "s"
            elif passive_verb.endswith("en"):
                active_verb = passive_verb[:-2] + "s"
        
        if active_verb or adverb:
            for i, comp in enumerate(sentence_components):
                adverb_match = not adverb or comp["adverb"] == adverb
                verb_match = not active_verb or comp["verb"] == active_verb
                
                if adverb_match and verb_match and comp["object"]:
                    results.append(get_full_object(comp))
    
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