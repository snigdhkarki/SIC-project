# Natural Language Question Answering System (NLQA)

This project implements a **simple question-answering system** that extracts subject-verb-object (SVO) relationships from sentences and answers structured questions based on stored relations. It uses **NLTK**, **TextBlob**, and Python's built-in string operations to process and analyze sentences.

---

# 🚀 Features

✅ Extracts **subjects, verbs, and objects** from a list of sentences  
✅ Stores sentence relationships in a **dictionary for fast lookup**  
✅ Answers **questions about actions, subjects, and objects**  
✅ Converts **verbs into their V5 form** (3rd-person singular present)  
✅ Uses **NLTK for tokenization and TextBlob for verb conjugation**  

---

# 📜 How It Works

## 1️⃣ Sentence Processing
The system takes a list of sentences with subjects, verbs, and objects.

It breaks them down into words and stores relationships in a dictionary.

## 2️⃣ Dictionary Creation
Every word (subject, verb, or object) is mapped to the sentences in which it appears.

## 3️⃣ Question Answering
The system supports questions like:

✅ "What does Hari do?"

✅ "What is done to Gita?"

✅ "Who does eat apple?"

✅ "Explain all occurring lion."

## 4️⃣ Verb Normalization
Uses NLTK and TextBlob to convert past participle verbs into V5 (e.g., "eaten" → "eats").

# 🏗️ Example Usage & Output
### Example Input Sentences
"Ram eats banana. Hari fights lion. Sita eats apple. Gita shoots lion."

### Example Question
question = "What does Sita do?"

### Output
eats


# 🔥 Future Improvements

🔹 Support more complex sentence structures

🔹 Implement lemmatization-based dictionary lookup

🔹 Improve handling of irregular verbs

🔹 Add context-based answers

## 📜 License
This project is open-source and available under the MIT License.

## 🤝 Contributing
We welcome contributions! If you find a bug or want to add a new feature, feel free to submit a pull request.
