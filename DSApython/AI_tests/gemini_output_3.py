input_info = 'Ram eats banana.Hari fights lion.Sita eats apple.\
Gita shoots lion.Ramesh throws laptop.Ram smashes banana.\
Basanta eats banana.Ram eats apple.Hari hits Gita.Hari falls.\
Red Ram eats banana.Smart Hari fights lion.Tall Sita eats apple.\
Clever Gita shoots lion.Lazy Ramesh throws laptop.Strong Ram smashes banana.\
Kind Basanta eats banana.Young Ram eats apple.Brave Hari hits Gita.Quick Hari falls.\
Ram quickly eats banana.Hari bravely fights lion.Sita silently eats apple.\
Gita accurately shoots lion.Ramesh carelessly throws laptop.Ram powerfully smashes banana.\
Basanta happily eats banana.Ram hungrily eats apple.Hari angrily hits Gita.Hari rapidly falls.\
Red Ram quickly eats banana.Smart Hari bravely fights lion.Tall Sita silently eats apple.\
Clever Gita accurately shoots lion.Lazy Ramesh carelessly throws laptop.Strong Ram powerfully smashes banana.\
Kind Basanta happily eats banana.Young Ram hungrily eats apple.Brave Hari angrily hits Gita.Quick Hari rapidly falls.'
input_info = input_info[:-1]
list_of_SV_sentences= input_info.split(".")
broken_list_of_SV_sentences = []
for sentence in list_of_SV_sentences:
 word_list = sentence.split(" ")
 broken_list_of_SV_sentences.append(word_list)

dict_of_relation = {}

def identify_sentence_structure(sentence_words):
    structure = []
    word_index = 0
    #Adjective Check
    if word_index < len(sentence_words) and sentence_words[word_index] not in ['Ram', 'Hari', 'Sita', 'Gita', 'Ramesh', 'Basanta']: #simplistic adj check
        structure.append(('adj', sentence_words[word_index]))
        word_index += 1
    #Subject check
    if word_index < len(sentence_words) and sentence_words[word_index] in ['Ram', 'Hari', 'Sita', 'Gita', 'Ramesh', 'Basanta']:
        structure.append(('subject', sentence_words[word_index]))
        word_index += 1
    #Adverb check
    if word_index < len(sentence_words) and sentence_words[word_index][-2:] == 'ly': #simplistic adverb check
        structure.append(('adv', sentence_words[word_index]))
        word_index += 1
    elif word_index < len(sentence_words) and sentence_words[word_index][-3:] == 'ily': #handling happily
        structure.append(('adv', sentence_words[word_index]))
        word_index += 1
    #Verb Check
    if word_index < len(sentence_words) and sentence_words[word_index] not in ['Ram', 'Hari', 'Sita', 'Gita', 'Ramesh', 'Basanta', 'banana','lion','apple','laptop','Gita']: #simplistic verb check
        structure.append(('verb', sentence_words[word_index]))
        word_index += 1
    #Adjective Check before object
    if word_index < len(sentence_words) and sentence_words[word_index] not in ['Ram', 'Hari', 'Sita', 'Gita', 'Ramesh', 'Basanta','eats','fights','shoots','throws','smashes','hits','falls','eaten','shot','hit','fallen','eating','fighting','shooting','throwing','smashing','hitting','falling']: #simplistic adj check
        structure.append(('adj_object', sentence_words[word_index]))
        word_index += 1
    #Object Check
    if word_index < len(sentence_words) and word_index < len(sentence_words):
        structure.append(('object', sentence_words[word_index]))
        word_index += 1
    return structure

structured_sentences = []
for sentence in broken_list_of_SV_sentences:
    structured_sentences.append(identify_sentence_structure(sentence))

for structure_list in structured_sentences:
    for word_tuple in structure_list:
        role = word_tuple[0]
        word = word_tuple[1]
        if word not in dict_of_relation:
            dict_of_relation[word] = {}
        if role not in dict_of_relation[word]:
            dict_of_relation[word][role] = []
        sentence_index = structured_sentences.index(structure_list)
        dict_of_relation[word][role].append(sentence_index)

def answer_question(question, dict_of_relation, list_of_SV_sentences, structured_sentences):
    question = question[:-1]
    question_word_list = question.split(" ")
    question_word_list.extend(["","","","","","","",""])

    if question_word_list[0] == "Explain" and question_word_list[1] == "all" and question_word_list[2] == "occuring":
        verb_to_explain = question_word_list[3]
        if verb_to_explain in dict_of_relation and 'verb' in dict_of_relation[verb_to_explain]:
            for index in dict_of_relation[verb_to_explain]['verb']:
                print(list_of_SV_sentences[index])
        else:
            print(f"No sentences found with verb '{verb_to_explain}'")

    elif question_word_list[0] == "What" and question_word_list[1]=="is" and question_word_list[2] == "done" and question_word_list[3] =="to":
        object_of_question = question_word_list[4]
        if object_of_question in dict_of_relation and 'object' in dict_of_relation[object_of_question]:
            for index in dict_of_relation[object_of_question]['object']:
                print(list_of_SV_sentences[index])
        else:
            print(f"No sentences found with object '{object_of_question}'")

    elif question_word_list[0] == "What" and question_word_list[1] =="does" and question_word_list[3] =="do" and question_word_list[4] =="to":
        subject_of_question = question_word_list[2]
        object_of_question = question_word_list[5]
        if subject_of_question in dict_of_relation and 'subject' in dict_of_relation[subject_of_question] and object_of_question in dict_of_relation and 'object' in dict_of_relation[object_of_question]:
            subject_indices = set(dict_of_relation[subject_of_question]['subject'])
            object_indices = set(dict_of_relation[object_of_question]['object'])
            sentences_with_both = list(subject_indices.intersection(object_indices))
            for sentence_index in sentences_with_both:
                print(list_of_SV_sentences[sentence_index])
        else:
            print(f"No sentences found with subject '{subject_of_question}' and object '{object_of_question}'")

    elif question_word_list[0] == "What" and question_word_list[1] == "does" and question_word_list[3] == "do":
        subject_of_question = question_word_list[2]
        if subject_of_question in dict_of_relation and 'subject' in dict_of_relation[subject_of_question]:
            for index in dict_of_relation[subject_of_question]['subject']:
                print(list_of_SV_sentences[index])
        else:
            print(f"No sentences found with subject '{subject_of_question}'")

    elif (question_word_list[0] == "What" or question_word_list[0] == "Who") and question_word_list[1] == "does":
        subject_of_question = question_word_list[2]
        verb_of_question = question_word_list[3]
        if subject_of_question in dict_of_relation and 'subject' in dict_of_relation[subject_of_question] and verb_of_question in dict_of_relation and 'verb' in dict_of_relation[verb_of_question]:
            subject_indices = set(dict_of_relation[subject_of_question]['subject'])
            verb_indices = set(dict_of_relation[verb_of_question]['verb'])
            sentences_with_both = list(subject_indices.intersection(verb_indices))
            for sentence_index in sentences_with_both:
                print(list_of_SV_sentences[sentence_index])
        else:
            print(f"No sentences found with subject '{subject_of_question}' and verb '{verb_of_question}'")

    elif (question_word_list[0] == "What" or question_word_list[0] == "Who") and question_word_list[1] == "is" and (question_word_list[2][-2:] == "ed" or question_word_list[2][-2:] == "en" or question_word_list[2][-1] == "s" or question_word_list[2][-3:] == "ing"):
        verb_base = ""
        question_verb = question_word_list[2]
        if question_verb[-2:] == "ed":
            verb_base = question_verb[:-2]
        elif question_verb[-2:] == "en":
            verb_base = question_verb[:-2]
        elif question_verb[-3:] == "ing":
            verb_base = question_verb[:-3]
        elif question_verb[-1] == "s":
            verb_base = question_verb[:-1]
        else:
            verb_base = question_verb

        if verb_base+"s" in dict_of_relation and 'verb' in dict_of_relation[verb_base+"s"]: #check for verb in base + s form
            for index in dict_of_relation[verb_base+"s"]['verb']:
                print(' '.join(broken_list_of_SV_sentences[index]))
        elif verb_base in dict_of_relation and 'verb' in dict_of_relation[verb_base]: #check for verb in base form
            for index in dict_of_relation[verb_base]['verb']:
                print(' '.join(broken_list_of_SV_sentences[index]))
        else:
            print(f"No sentences found with verb form like '{question_verb}'")

    elif (question_word_list[0] == "What" or question_word_list[0] == "Who") and len(question_word_list) == 2: #handles "Who/What V?" and "Who/What is Ven/Ved?" type questions
        query_word = question_word_list[1]
        if query_word in dict_of_relation and 'verb' in dict_of_relation[query_word]: #handles "Who/What V?"
            for index in dict_of_relation[query_word]['verb']:
                print(' '.join(broken_list_of_SV_sentences[index]))
        elif query_word[-2:] == "ed" or query_word[-2:] == "en" or query_word[-1] == "s" or query_word[-3:] == "ing": # handles "Who/What is Ven/Ved?" type questions
            verb_base = ""
            if query_word[-2:] == "ed":
                verb_base = query_word[:-2]
            elif query_word[-2:] == "en":
                verb_base = query_word[:-2]
            elif query_word[-3:] == "ing":
                verb_base = query_word[:-3]
            elif query_word[-1] == "s":
                verb_base = query_word[:-1]
            else:
                verb_base = query_word

            if verb_base+"s" in dict_of_relation and 'verb' in dict_of_relation[verb_base+"s"]: # Check for verb existence in base form + "s"
                for index in dict_of_relation[verb_base+"s"]['verb']:
                    print(' '.join(broken_list_of_SV_sentences[index]))
            elif verb_base in dict_of_relation and 'verb' in dict_of_relation[verb_base]: # Check for verb existence in base form
                for index in dict_of_relation[verb_base]['verb']:
                    print(' '.join(broken_list_of_SV_sentences[index]))
            else:
                print(f"No sentences found with verb form like '{query_word}'")
        else:
            print(f"No sentences found related to '{query_word}'")

    else:
        print("Question type not understood")


questions = [
 "What does Hari do?",
 "Who eats banana?",
 "What is done to banana?",
 "What does Ram do to banana?",
 "Explain all occuring eats.",
 "Who shoots?",
 "Who is shot?",
 "Explain all occuring fights."
]

print("--- Original Questions ---")
for q in questions:
 print(f"Question: {q}")
 answer_question(q, dict_of_relation, list_of_SV_sentences, structured_sentences)
 print("-" * 20)

new_questions = [
 "What does Red Ram do?", # adj+S+V+O
 "Who bravely fights?", # S+adv+V+O
 "What does Sita silently do?", # S+adv+V+O
 "What is eaten?", # Who/What is Ven/Ved?
 "Who falls rapidly?", # S+adv+V
 "Explain all occuring eats", # Explain all occuring V.
 "What does Smart Hari do to lion?", # adj+S+V+O, What does S do to O?
 "What is laptop done to?", # What is done to O?
 "Who hits Gita?", # S+V+O, Who V O?
 "Who is brave?", # Who is adj? - New Question type. handled by Who/What is Ven/Ved? and V? type questions
 "What does Basanta happily do?", # adj+S+adv+V+O
 "What does Young Ram hungrily do to apple?", # adj+S+adv+V+O, What does S do to O?
 "What is quickly done to banana?", # adv+V+O, What is done to O? - not exactly fitting input but testing 'done to O'
 "Who accurately shoots lion?" # adv+V+O, Who V O? - not exactly fitting input but testing 'Who V O?'
]

print("\n--- New Questions ---")
for q in new_questions:
 print(f"Question: {q}")
 answer_question(q, dict_of_relation, list_of_SV_sentences, structured_sentences)
 print("-" * 20)