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
input_info = input_info.strip().replace('\n', '')[:-1]
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
    q_words = question.rstrip('?').split()
    components = {
        'subject': [],
        'verb': [],
        'object': [],
        'adverbs': [],
        'type': None
    }
    
    if q_words[0].lower() == 'explain':
        components['type'] = 'explain'
        components['verb'] = q_words[-1]
        return components
        
    if q_words[0].lower() in ('who', 'what'):
        if 'by' in q_words:
            components['type'] = 'passive'
            components['object'] = q_words[q_words.index('by')+1:]
            components['verb'] = [q_words[q_words.index('is')+1]] if 'is' in q_words else []
            return components
            
        if 'does' in q_words:
            subj_start = q_words.index('does') + 1
            verb_pos = q_words.index('do') if 'do' in q_words else -1
            if verb_pos != -1:
                components['subject'] = q_words[subj_start:verb_pos]
                components['verb'] = [q_words[verb_pos]]
                obj_start = q_words.index('to') + 1 if 'to' in q_words else verb_pos + 1
                components['object'] = q_words[obj_start:]
            else:
                components['verb'] = [q_words[subj_start]]
                components['object'] = q_words[subj_start+1:]
            components['type'] = 'standard'
        elif 'is' in q_words:
            components['type'] = 'passive_done'
            components['object'] = [q_words[-1]]
        else:
            # Handle direct questions like "Who fights wild lion?"
            components['verb'] = [q_words[1]]
            components['object'] = q_words[2:]
            components['type'] = 'direct'
    
    elif q_words[0].lower() == 'how':
        components['type'] = 'how'
        components['adverbs'] = [q_words[3]]
        components['verb'] = [q_words[4]]
    
    return components

def get_base_verb(verb):
    verb = verb.lower()
    if verb.endswith('s'):
        return verb[:-1]
    if verb.endswith(('ed', 'en')):
        return verb[:-2]
    return verb

def find_matching_sentences(components):
    if not components['verb'] and components['type'] not in ['passive', 'explain']:
        return []
        
    if components['type'] == 'explain':
        return [s for s in list_of_SV_sentences if components['verb'] in s.lower()]
        
    if components['type'] == 'passive':
        base_verb = get_base_verb(components['verb'][0]) if components['verb'] else ''
        matches = []
        for idx, sentence in enumerate(broken_list_of_SV_sentences):
            if base_verb and (base_verb in [get_base_verb(w) for w in sentence]):
                if components['object'][0].lower() in [w.lower() for w in sentence]:
                    matches.append(' '.join(sentence))
        return matches
        
    if components['type'] == 'how':
        return [s for s in list_of_SV_sentences 
               if components['adverbs'][0] in s.lower() 
               and components['verb'][0] in s.lower()]
        
    # Handle direct questions and standard queries
    base_verb = get_base_verb(components['verb'][0]) if components['verb'] else ''
    possible_verbs = {components['verb'][0].lower(), base_verb} if components['verb'] else set()
    
    matches = []
    for sentence in list_of_SV_sentences:
        sent_lower = sentence.lower()
        verb_match = any(v in sent_lower for v in possible_verbs) if possible_verbs else True
        subj_match = all(word.lower() in sent_lower for word in components['subject'])
        obj_match = all(word.lower() in sent_lower for word in components['object'])
        
        if verb_match and subj_match and obj_match:
            matches.append(sentence)
    
    return matches

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