input_info = "Snigdh eats.Ram eats.Snigdh sits.Sita falls."
input_info = input_info[:-1]
list_of_SV_sentences= input_info.split(".")
Subject_list = ["Snigdh", "Ram", "Sita"]
Verb_list = ["eats", "sits", "falls"]
broken_list_of_SV_sentences = []
for sentence in list_of_SV_sentences:
    word_list = sentence.split(" ")
    broken_list_of_SV_sentences.append(word_list)
#print(broken_list_of_SV_sentences)
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
question = "What does Sita do?"
question = question[:-1]
question_word_list = question.split(" ")
if question_word_list[0] == "What" and question_word_list[1] == "does" and question_word_list[2] in Subject_list and question_word_list[3]== "do":
    for index in dict_of_relation[question_word_list[2]]:
        print(broken_list_of_SV_sentences[index][1])
else:
    for index in dict_of_relation[question_word_list[1]]:
        print(broken_list_of_SV_sentences[index][0])
