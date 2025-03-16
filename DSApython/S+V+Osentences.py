input_info = 'Ram eats banana.Hari fights lion.Sita eats apple.\
Gita shoots lion.Ramesh throws laptop.Ram smashes banana.\
Basanta eats banana.Ram eats apple.Hari hits Gita.Hari falls.'
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
question = "What does Hari do?"
question = question[:-1]
question_word_list = question.split(" ")
question_word_list.extend(["","","",""])
if question_word_list[0] == "Explain" and question_word_list[1] == "all" and question_word_list[2] == "occuring":
    for index in dict_of_relation[question_word_list[3]]:
        print(list_of_SV_sentences[index])
elif question_word_list[0] == "What" and question_word_list[1]=="is" and question_word_list[2] == "done" and question_word_list[3] =="to":
    for index in dict_of_relation[question_word_list[4]]:
        print(list_of_SV_sentences[index])
elif question_word_list[0] == "What" and question_word_list[1] =="does" and question_word_list[3] =="do" and question_word_list[4] =="to":
    sentences_with_both = list(set(dict_of_relation[question_word_list[2]]) & set(dict_of_relation[question_word_list[5]]))
    for sentence_index in sentences_with_both:
        if broken_list_of_SV_sentences[sentence_index][0] == question_word_list[2]:
            print(list_of_SV_sentences[sentence_index])
elif question_word_list[0] == "What" and question_word_list[1] == "does" and question_word_list[3] == "do":
    for index in dict_of_relation[question_word_list[2]]:
        print(list_of_SV_sentences[index])
elif (question_word_list[0] == "What" or question_word_list[0] == "Who") and question_word_list[1] == "does":
    sentences_with_both = list(set(dict_of_relation[question_word_list[2]]) & set(dict_of_relation[question_word_list[3]]))
    for sentence_index in sentences_with_both:
        if broken_list_of_SV_sentences[sentence_index][0] == question_word_list[2]:
            print(list_of_SV_sentences[sentence_index])
elif (question_word_list[0] == "What" or question_word_list[0] == "Who") and question_word_list[1] == "is" and (question_word_list[2][-2:] == "ed" or question_word_list[2][-2:] == "en" or question_word_list[2][-1] == "t"):
    if question_word_list[2][-2:] == "ed":
        verb = question_word_list[2][:-2]
        
    elif question_word_list[2][-2:] == "en":
        verb = question_word_list[2][:-2]
    else:
        verb = question_word_list[2]
    for index in dict_of_relation[verb+"s"]:
        print(broken_list_of_SV_sentences[index][2])
    
else:
    for index in dict_of_relation[question_word_list[1]]:
        print(broken_list_of_SV_sentences[index][0])

