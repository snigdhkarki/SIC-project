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
list_of_SV_sentences = [s.strip() for s in input_info.split(".") if s]
broken_list_of_SV_sentences = [s.split(" ") for s in list_of_SV_sentences]

# Build word-to-sentence index dictionary
dict_of_relation = {}
for sentence_index, sentence in enumerate(broken_list_of_SV_sentences):
    for word in sentence:
        if word not in dict_of_relation:
            dict_of_relation[word] = []
        if sentence_index not in dict_of_relation[word]:
            dict_of_relation[word].append(sentence_index)

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
    "Explain all occurring eats.",
    "What carelessly throws expensive laptop?",
    "Who patiently feeds hungry birds?",
    "What quickly melts thin ice?",
    "What does loud speaker play?",
    "Who is fed by old man?",
    "How does storm shake old house?"
]

def extract_components(question):
    q_words = question.lower().rstrip('?.').split()
    components = {
        'subject': [],
        'verb': [],
        'object': [],
        'adverbs': [],
        'adjectives': [],
        'type': None
    }
    
    if q_words[0] == 'explain' and q_words[1] == 'all' and q_words[2] == 'occurring':
        components['type'] = 'explain_verb'
        components['verb'] = q_words[3]
        return components
    
    if q_words[0] in ('who', 'what'):
        if 'by' in q_words:
            components['type'] = 'passive'
            components['object'] = q_words[q_words.index('by')+1:]
            components['verb'] = q_words[q_words.index('is')+1] if 'is' in q_words else []
            return components
        
        if q_words[1] == 'does':
            subj_start = 2
            verb_pos = q_words.index('do') - 1
            components['subject'] = q_words[subj_start:verb_pos]
            components['verb'] = [q_words[verb_pos]]
            if 'to' in q_words:
                obj_start = q_words.index('to') + 1
                components['object'] = q_words[obj_start:]
            components['type'] = 'standard'
        elif q_words[1] == 'is':
            components['type'] = 'passive_done'
            components['object'] = q_words[-1:]
        elif 'how' in q_words:
            components['type'] = 'how'
            components['adverbs'] = [q_words[q_words.index('does')+2]]
    elif q_words[0] == 'how':
        components['type'] = 'how'
        components['adverbs'] = [q_words[3]]
        components['verb'] = [q_words[4]]
    
    return components

def get_base_verb(verb):
    if verb.endswith('s'):
        return verb[:-1]
    if verb.endswith(('ed', 'en')):
        return verb[:-2]
    return verb

def find_matching_sentences(components):
    candidates = set(range(len(broken_list_of_SV_sentences)))
    
    # Handle passive voice
    if components['type'] == 'passive':
        verb_base = get_base_components['verb'][0]
        active_verb = verb_base + 's'
        object_matches = []
        for idx in dict_of_relation.get(components['object'][0], []):
            sentence = broken_list_of_SV_sentences[idx]
            if active_verb in sentence:
                subj = ' '.join(sentence[:sentence.index(active_verb)])
                object_matches.append(subj)
        return list(set(object_matches))
    
    # Handle explain verb type
    if components['type'] == 'explain_verb':
        matches = []
        for idx in dict_of_relation.get(components['verb'], []):
            matches.append(' '.join(broken_list_of_SV_sentences[idx]))
        return matches
    
    # Handle adverb questions
    if components['type'] == 'how':
        matches = []
        for idx, sentence in enumerate(broken_list_of_SV_sentences):
            if components['adverbs'][0] in sentence and components['verb'][0] in sentence:
                matches.append(' '.join(sentence))
        return matches
    
    # Standard query handling
    possible_verbs = [components['verb'][0], components['verb'][0] + 's']
    matches = []
    for idx in candidates:
        sentence = broken_list_of_SV_sentences[idx]
        sentence_lower = [word.lower() for word in sentence]
        
        # Check subject
        subj_match = all(word.lower() in sentence_lower for word in components['subject'])
        
        # Check verb
        verb_match = any(v in sentence_lower for v in possible_verbs)
        
        # Check object
        obj_match = all(word.lower() in sentence_lower for word in components['object'])
        
        if subj_match and verb_match and obj_match:
            matches.append(' '.join(sentence))
    
    return matches

# Test all questions
for question in test_questions:
    print(f"\nQ: {question}")
    components = extract_components(question)
    matches = find_matching_sentences(components)
    
    if not matches:
        print("A: No matching actions found")
    else:
        print("A:")
        for match in matches:
            print(f" - {match}")