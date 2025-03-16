# Extended Input Sentences with Adjectives/Adverbs
input_info = '''
Quick Ram eats ripe banana. Happy Hari fiercely fights wild lion. 
Sita slowly eats red apple. Gita skillfully shoots angry lion. 
Ramesh carelessly throws expensive laptop. Ram violently smashes rotten banana. 
Basanta joyfully eats yellow banana. Hungry Ram eagerly eats sweet apple. 
Hari angrily hits gentle Gita. Tired Hari suddenly falls. 
Clever monkey playfully climbs tall tree. Old man patiently feeds hungry birds. 
Loud speaker continuously plays annoying sound. Small child eagerly opens big gift. 
Bright sun quickly melts thin ice. Storm violently shakes old house.
'''
input_info = input_info.strip().replace('\n', '')[:-1]  # Clean input
list_of_SV_sentences = input_info.split(".")
broken_list_of_SV_sentences = [s.strip().split(" ") for s in list_of_SV_sentences if s]

# Build word-to-sentence index dictionary
dict_of_relation = {}
for sentence_index, sentence in enumerate(broken_list_of_SV_sentences):
    for word in sentence:
        if word not in dict_of_relation:
            dict_of_relation[word] = []
        if sentence_index not in dict_of_relation[word]:
            dict_of_relation[word].append(sentence_index)

# Test Questions (20+)
test_questions = [
    "What does Hari do?",
    "Who fights wild lion?",
    "What does quick Ram eat?",
    "What does Gita skillfully shoot?",
    "Who violently smashes rotten banana?",
    "What is done to expensive laptop?",
    "What does hungry Ram do?",
    "How does Sita eat red apple?",
    "Who eagerly opens big gift?",
    "What does old man feed?",
    "Who is hit by Hari?",
    "What is climbed by clever monkey?",
    "What suddenly happens to tired Hari?",
    "What joyfully eats yellow banana?",
    "What violently shakes old house?",
    "Explain all occuring eats.",
    "What carelessly throws expensive laptop?",
    "Who patiently feeds hungry birds?",
    "What quickly melts thin ice?",
    "What does loud speaker play?",
    "Who is fed by old man?",
    "How does storm shake old house?"
]

def match_structure(sentence, components):
    # Helper to check if sentence matches question components
    ptr = 0
    # Match subject with adjectives
    for subj_word in components['subject']:
        if ptr >= len(sentence) or sentence[ptr] != subj_word:
            return False
        ptr += 1
    # Match adverbs before verb
    while ptr < len(sentence) and sentence[ptr] in components['adverbs']:
        ptr += 1
    # Match verb
    if ptr >= len(sentence) or sentence[ptr] not in components['verbs']:
        return False
    ptr += 1
    # Match adverbs after verb
    while ptr < len(sentence) and sentence[ptr] in components['adverbs']:
        ptr += 1
    # Match object with adjectives
    for obj_word in components['object']:
        if ptr >= len(sentence) or sentence[ptr] != obj_word:
            return False
        ptr += 1
    return True

for question in test_questions:
    print(f"\nQ: {question}")
    q_words = question[:-1].split(" ") if question.endswith('?') else question.split(" ")
    q_type = None
    components = {
        'subject': [],
        'verbs': [],
        'object': [],
        'adverbs': [],
        'adjectives': []
    }

    # Question Pattern Recognition
    if q_words[0] == "Explain":
        q_type = 8
        verb = q_words[3]
        print("A: All sentences with action '" + verb + "':")
        for idx in dict_of_relation.get(verb, []):
            print(" -", " ".join(broken_list_of_SV_sentences[idx]))
    
    elif "is done to" in question:
        obj = q_words[-1]
        print(f"A: Actions done to {obj}:")
        for idx in dict_of_relation.get(obj, []):
            sent = broken_list_of_SV_sentences[idx]
            if len(sent) >= 3 and sent[-1] == obj:
                print(" -", " ".join(sent))
    
    elif q_words[0] in ("Who", "What"):
        # Extract components with adjectives/adverbs
        current_part = []
        for word in q_words[1:]:
            if word in ["does", "did", "do", "to", "by"]:
                if current_part:
                    if components['subject'] == []:
                        components['subject'] = current_part
                    elif components['verbs'] == []:
                        components['verbs'] = current_part
                    current_part = []
                continue
            current_part.append(word)
        if current_part:
            components['object'] = current_part
        
        # Handle passive voice
        if "by" in q_words:
            obj = q_words[-1]
            print(f"A: {obj} performs these actions:")
            for idx in dict_of_relation.get(obj, []):
                sent = broken_list_of_SV_sentences[idx]
                if sent[0] == obj:
                    print(" -", " ".join(sent))
        
        # Find matching sentences
        else:
            candidates = set(range(len(broken_list_of_SV_sentences)))
            for word in components['subject'] + components['verbs'] + components['object']:
                if word in dict_of_relation:
                    candidates &= set(dict_of_relation[word])
            
            print("A:", end=" ")
            found = False
            for idx in candidates:
                sent = broken_list_of_SV_sentences[idx]
                if match_structure(sent, components):
                    print(" ".join(sent))
                    found = True
            if not found:
                print("No matching actions found")

    # Add more question type handlers here...
    else:
        print("A: Question pattern not recognized")