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
# print(broken_list_of_SV_sentences)
dict_of_relation = {}
for sentence in broken_list_of_SV_sentences:
 for word in sentence:
  sentence_index = broken_list_of_SV_sentences.index(sentence)
 if word in dict_of_relation.keys():
  if sentence_index not in dict_of_relation[word]:
   dict_of_relation[word].append(sentence_index)
 else:
  dict_of_relation[word] = [sentence_index]
# print(dict_of_relation)

def answer_question(question, dict_of_relation, list_of_SV_sentences, broken_list_of_SV_sentences):
 question = question[:-1]
 question_word_list = question.split(" ")
 question_word_list.extend(["","","","","","","",""]) # Pad for safety

 if question_word_list[0] == "Explain" and question_word_list[1] == "all" and question_word_list[2] == "occuring":
  if question_word_list[3] in dict_of_relation: # Check if verb exists in dict
   for index in dict_of_relation[question_word_list[3]]:
    print(list_of_SV_sentences[index])
  else:
   print(f"No sentences found with verb '{question_word_list[3]}'")

 elif question_word_list[0] == "What" and question_word_list[1]=="is" and question_word_list[2] == "done" and question_word_list[3] =="to":
  if question_word_list[4] in dict_of_relation: # Check if object exists
   for index in dict_of_relation[question_word_list[4]]:
    print(list_of_SV_sentences[index])
  else:
   print(f"No sentences found with object '{question_word_list[4]}'")

 elif question_word_list[0] == "What" and question_word_list[1] =="does" and question_word_list[3] =="do" and question_word_list[4] =="to":
  if question_word_list[2] in dict_of_relation and question_word_list[5] in dict_of_relation: # Check if both S and O exist
   sentences_with_both = list(set(dict_of_relation[question_word_list[2]]) & set(dict_of_relation[question_word_list[5]]))
   for sentence_index in sentences_with_both:
    if broken_list_of_SV_sentences[sentence_index][0] == question_word_list[2] or broken_list_of_SV_sentences[sentence_index][1] == question_word_list[2]: #Handle adj+S cases.
     print(list_of_SV_sentences[sentence_index])
  else:
   print(f"No sentences found with subject '{question_word_list[2]}' and object '{question_word_list[5]}'")

 elif question_word_list[0] == "What" and question_word_list[1] == "does" and question_word_list[3] == "do":
  if question_word_list[2] in dict_of_relation: # Check if subject exists
   for index in dict_of_relation[question_word_list[2]]:
    if broken_list_of_SV_sentences[index][0] == question_word_list[2] or broken_list_of_SV_sentences[index][1] == question_word_list[2]: #Handle adj+S cases.
     print(list_of_SV_sentences[index])
  else:
   print(f"No sentences found with subject '{question_word_list[2]}'")

 elif (question_word_list[0] == "What" or question_word_list[0] == "Who") and question_word_list[1] == "does":
  if question_word_list[2] in dict_of_relation and question_word_list[3] in dict_of_relation: # Check if both S and V exist
   sentences_with_both = list(set(dict_of_relation[question_word_list[2]]) & set(dict_of_relation[question_word_list[3]]))
   for sentence_index in sentences_with_both:
    if broken_list_of_SV_sentences[sentence_index][0] == question_word_list[2] or broken_list_of_SV_sentences[sentence_index][1] == question_word_list[2]: #Handle adj+S cases.
     print(list_of_SV_sentences[sentence_index])
  else:
   print(f"No sentences found with subject '{question_word_list[2]}' and verb '{question_word_list[3]}'")

 elif (question_word_list[0] == "What" or question_word_list[0] == "Who") and question_word_list[1] == "is" and (question_word_list[2][-2:] == "ed" or question_word_list[2][-2:] == "en" or question_word_list[2][-1] == "s" or question_word_list[2][-3:] == "ing"): # added "is vs Ven/Ved/Ving"
  verb_ اصل = ""
  if question_word_list[2][-2:] == "ed":
   verb_اصل = question_word_list[2][:-2]
  elif question_word_list[2][-2:] == "en":
   verb_اصل = question_word_list[2][:-2]
  elif question_word_list[2][-3:] == "ing":
   verb_اصل = question_word_list[2][:-3]
  elif question_word_list[2][-1] == "s":
   verb_اصل = question_word_list[2][:-1]
  else:
   verb_اصل = question_word_list[2]

  if verb_اصل+"s" in dict_of_relation: # Check for verb existence in base form + "s"
   for index in dict_of_relation[verb_اصل+"s"]: # assuming verb is mostly in V or Vs form in sentences.
    print(' '.join(broken_list_of_SV_sentences[index])) # Print full sentence, handles cases with adj/adv
  elif verb_اصل in dict_of_relation: # Check for verb existence in base form
   for index in dict_of_relation[verb_اصل]:
    print(' '.join(broken_list_of_SV_sentences[index]))
  else:
   print(f"No sentences found with verb form like '{question_word_list[2]}'")


 elif (question_word_list[0] == "What" or question_word_list[0] == "Who") and len(question_word_list) == 2: # handles "Who/What V?" and "Who/What is Ven/Ved?" type questions
  if question_word_list[1] in dict_of_relation: # handles "Who/What V?"
   for index in dict_of_relation[question_word_list[1]]:
    print(' '.join(broken_list_of_SV_sentences[index])) # Print full sentence
  elif question_word_list[1][-2:] == "ed" or question_word_list[1][-2:] == "en" or question_word_list[1][-1] == "s" or question_word_list[1][-3:] == "ing": # handles "Who/What is Ven/Ved?" type questions
   verb_اصل = ""
   if question_word_list[1][-2:] == "ed":
    verb_اصل = question_word_list[1][:-2]
   elif question_word_list[1][-2:] == "en":
    verb_اصل = question_word_list[1][:-2]
   elif question_word_list[1][-3:] == "ing":
    verb_اصل = question_word_list[1][:-3]
   elif question_word_list[1][-1] == "s":
    verb_اصل = question_word_list[1][:-1]
   else:
    verb_اصل = question_word_list[1]

   if verb_اصل+"s" in dict_of_relation: # Check for verb existence in base form + "s"
    for index in dict_of_relation[verb_اصل+"s"]:
     print(' '.join(broken_list_of_SV_sentences[index])) # Print full sentence
   elif verb_اصل in dict_of_relation: # Check for verb existence in base form
    for index in dict_of_relation[verb_اصل]:
     print(' '.join(broken_list_of_SV_sentences[index]))
   else:
    print(f"No sentences found with verb form like '{question_word_list[1]}'")
  else:
   print(f"No sentences found related to '{question_word_list[1]}'")


 else:
  print("Question type not understood")

# Example questions - original questions still work
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
 answer_question(q, dict_of_relation, list_of_SV_sentences, broken_list_of_SV_sentences)
 print("-" * 20)

# New questions for extended sentences - testing new questions based on new structures
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
 answer_question(q, dict_of_relation, list_of_SV_sentences, broken_list_of_SV_sentences)
 print("-" * 20)