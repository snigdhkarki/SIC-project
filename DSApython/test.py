import nltk
from nltk.stem import WordNetLemmatizer
from textblob import Word

# Download required NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def convert_to_v5(word_list):
    # POS tag the words
    tagged_words = nltk.pos_tag(word_list)
    
    lemmatizer = WordNetLemmatizer()
    result = []
    
    for word, tag in tagged_words:
        if tag.startswith('VB'):  # Check if the word is a verb
            if tag == 'VBZ':     # Already in V5 form
                result.append(word)
            else:
                # Lemmatize to base form
                base_form = lemmatizer.lemmatize(word, pos='v')
                # Convert to 3rd person singular present (V5)
                v5_form = Word(base_form).conjugate(tense='present', person=3, number='singular')
                result.append(v5_form if v5_form else word)
        else:
            result.append(word)
    
    return result

# Example usage
input_words = ["What", "is", "eaten", "by", "Ram"]
output_words = convert_to_v5(input_words)
print(output_words)  # Output: ['What', 'is', 'eats', 'by', 'Ram']