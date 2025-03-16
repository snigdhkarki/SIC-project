input_info = 'Ram eats banana.Hari fights lion.Sita eats apple.\
Gita shoots lion.Ramesh throws laptop.Ram smashes banana.\
Basanta eats banana.Ram eats apple.Hari hits Gita.Hari falls.\
Clever Ram quickly eats banana.Ram eats yellow banana.\
Strong Hari angrily fights lion.Sita carefully eats ripe apple.\
Tall Gita shoots fierce lion.Young Ramesh throws old laptop.\
Hungry Ram violently smashes rotten banana.Smart Basanta quietly eats fresh banana.'

input_info = input_info[:-1]
list_of_sentences = input_info.split(".")

# List of known verbs to help with parsing
known_verbs = ["eats", "fights", "shoots", "throws", "smashes", "hits", "falls"]
known_subjects = ["Ram", "Hari", "Sita", "Gita", "Ramesh", "Basanta"]

# Enhanced data structure to store sentence components
sentence_components = []

for sentence in list_of_sentences:
    if not sentence.strip():  # Skip empty sentences
        continue
        
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
    
    # Identify the verb first as it's the most reliable component
    verb_index = -1
    for i, word in enumerate(words):
        if word in known_verbs:
            verb_index = i
            components["verb"] = word
            break
    
    if verb_index == -1:
        print(f"Warning: No verb found in sentence: {sentence}")
        continue
    
    # Now identify subject and object based on verb position
    # Words before verb are subject (and possibly subject_adj and adverb)
    # Words after verb are object (and possibly object_adj)
    
    # Parse subject area (before verb)
    if verb_index > 0:
        # Check if we have a known subject
        subject_found = False
        for i in range(verb_index):
            if words[i] in known_subjects:
                components["subject"] = words[i]
                subject_found = True
                
                # Words before subject are subject adjectives
                if i > 0:
                    components["subject_adj"] = words[i-1]
                
                # Words between subject and verb are adverbs
                if i + 1 < verb_index:
                    components["adverb"] = words[i+1]
                break
        
        # If no known subject, take the word right before the verb as subject
        if not subject_found:
            # If multiple words before verb, first is likely adj, last is subject
            if verb_index > 1:
                components["subject_adj"] = words[0]
                components["subject"] = words[verb_index-1]
            else:
                components["subject"] = words[verb_index-1]
    
    # Parse object area (after verb)
    if verb_index < len(words) - 1:
        # Last word is the object
        components["object"] = words[-1]
        
        # If there are words between verb and object, they are object adjectives
        if verb_index + 1 < len(words) - 1:
            components["object_adj"] = words[verb_index+1]
    
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
            # Check if the object matches exactly or with adjective
            if comp["object"] == obj:
                results.append(comp["original"])
            elif comp["object_adj"] and obj == comp["object"]:
                results.append(comp["original"])
    
    # Handle "What does S do to O?"
    elif question_words[0] == "What" and question_words[1] == "does" and question_words[3] == "do" and question_words[4] == "to":
        subj = question_words[2]
        obj = question_words[5]
        
        for i, comp in enumerate(sentence_components):
            # Check if subject and object match
            if (comp["subject"] == subj or get_full_subject(comp) == subj) and comp["object"] == obj:
                results.append(comp["original"])
    
    # Handle "What does S do?"
    elif question_words[0] == "What" and question_words[1] == "does" and question_words[3] == "do":
        subj = question_words[2]
        
        for i, comp in enumerate(sentence_components):
            # Check if the subject matches exactly or with adjective
            if comp["subject"] == subj or get_full_subject(comp) == subj:
                results.append(comp["original"])
    
    # Handle "Who/What does S V?"
    elif (question_words[0] == "What" or question_words[0] == "Who") and question_words[1] == "does":
        subj = question_words[2]
        verb = question_words[3]
        
        for i, comp in enumerate(sentence_components):
            # Check if subject and verb match
            if (comp["subject"] == subj or get_full_subject(comp) == subj) and comp["verb"] == verb:
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
    
    # Handle "Who V O?" or "What V O?"
    elif (question_words[0] == "Who" or question_words[0] == "What") and question_words[1] in known_verbs:
        verb = question_words[1]
        obj = question_words[2] if len(question_words) > 2 else None
        
        for i, comp in enumerate(sentence_components):
            if comp["verb"] == verb:
                if not obj or comp["object"] == obj:
                    results.append(get_full_subject(comp))
    
    # Handle "Who adv V O?" or specific questions with adverbs
    elif (question_words[0] == "Who" or question_words[0] == "What"):
        # Check if second word is an adverb
        adverb = question_words[1]
        verb = question_words[2] if len(question_words) > 2 else None
        
        if verb in known_verbs:
            for i, comp in enumerate(sentence_components):
                if comp["verb"] == verb and comp["adverb"] == adverb:
                    results.append(get_full_subject(comp))
    
    # Handle "What is adv Ved?" (What is violently smashed?)
    if question_words[0] == "What" and question_words[1] == "is" and question_words[3].endswith(("ed", "en")):
        adverb = question_words[2]
        passive_verb = question_words[3]
        
        # Convert to active form
        if passive_verb.endswith("ed"):
            active_verb = passive_verb[:-2] + "s"
        elif passive_verb.endswith("en"):
            active_verb = passive_verb[:-2] + "s"
        else:
            active_verb = None
            
        if active_verb:
            for i, comp in enumerate(sentence_components):
                if comp["verb"] == active_verb and comp["adverb"] == adverb:
                    results.append(get_full_object(comp))
    
    return results

# Print parsed sentences for verification
print("Parsed sentence components:")
for comp in sentence_components:
    print(comp)

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

print("\nTesting various questions:")
for q in questions:
    print(f"\nQuestion: {q}")
    answers = process_question(q)
    if answers:
        for answer in answers:
            print(f"Answer: {answer}")
    else:
        print("No answer found.")