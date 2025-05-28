# # language_model.py
# from langdetect import detect
# import os
# import pickle

# # Function to detect language (e.g., Nepali for multilingual processing)
# def detect_language(text):
#     lang = detect(text)
#     return lang

# # Function to save the language detection model (here it's just a simple function)
# def save_model(model, model_name):
#     model_path = os.path.join('trained_model', 'language_model', f'{model_name}_topic_model.pkl')
#     os.makedirs(os.path.dirname(model_path), exist_ok=True)
#     with open(model_path, 'wb') as f:
#         pickle.dump(model, f)
#     print(f"Language detection model saved at {model_path}")

# # Function to process each article
# def process_article(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         article_text = f.read().strip()
#     language = detect(article_text)
#     return language

# # Example usage: Process all articles in news_articles folder
# if __name__ == "__main__":
#     raw_data_folder = '../articles'
#     for filename in os.listdir(raw_data_folder):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(raw_data_folder, filename)
#             language = process_article(file_path)
#             print(f"Processed {filename} with detected language: {language}")



# import os
# import pickle
# import logging
# from langdetect import detect, LangDetectException

# # Set up logging for better tracking of activities
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Function to detect language (e.g., Nepali for multilingual processing)
# def detect_language(text):
#     try:
#         lang = detect(text)
#         return lang
#     except LangDetectException as e:
#         logging.error(f"Error detecting language: {e}")
#         return None

# # Function to save the language detection model (here it's just a simple function)
# def save_model(model, model_name):
#     model_path = os.path.join('trained_model', 'language_model', f'{model_name}_topic_model.pkl')
#     try:
#         os.makedirs(os.path.dirname(model_path), exist_ok=True)
#         with open(model_path, 'wb') as f:
#             pickle.dump(model, f)
#         logging.info(f"Language detection model saved at {model_path}")
#     except Exception as e:
#         logging.error(f"Error saving model: {e}")

# # Function to process each article and detect language
# def process_article(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             article_text = f.read().strip()
#         language = detect_language(article_text)
#         if language:
#             logging.info(f"Processed {file_path} with detected language: {language}")
#         else:
#             logging.warning(f"Language detection failed for {file_path}")
#         return language
#     except Exception as e:
#         logging.error(f"Error processing file {file_path}: {e}")
#         return None

# # Function to process all articles in a given folder
# def process_all_articles(raw_data_folder):
#     if not os.path.exists(raw_data_folder):
#         logging.error(f"Folder {raw_data_folder} does not exist.")
#         return

#     for filename in os.listdir(raw_data_folder):
#         file_path = os.path.join(raw_data_folder, filename)
#         if filename.endswith('.txt') and os.path.isfile(file_path):
#             language = process_article(file_path)

# # Example usage: Process all articles in the 'articles' folder
# if __name__ == "__main__":
#     raw_data_folder = '../articles'  # Make sure this path is correct
#     process_all_articles(raw_data_folder)



# import os
# import logging
# from langdetect import detect

# # Setup logging
# logging.basicConfig(filename='language_detection.log', level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# # Function to detect language (e.g., Nepali for multilingual processing)
# def detect_language(text):
#     lang = detect(text)
#     return lang

# # Function to save detected languages to a file
# def save_language_output(languages, output_file):
#     try:
#         # Create the directory if it doesn't exist
#         os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
#         with open(output_file, 'w', encoding='utf-8') as f:
#             for filename, lang in languages.items():
#                 f.write(f"{filename}: {lang}\n")
        
#         logging.info(f"Language detection output saved at {output_file}")
#     except Exception as e:
#         logging.error(f"Error saving language detection output: {e}")

# # Function to process each article
# def process_article(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         article_text = f.read().strip()
#     language = detect(article_text)
#     return language

# # Main processing loop for all articles in the folder
# def process_articles_and_save_languages(raw_data_folder, output_file):
#     detected_languages = {}
    
#     for filename in os.listdir(raw_data_folder):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(raw_data_folder, filename)
#             language = process_article(file_path)
#             detected_languages[filename] = language
#             logging.info(f"Processed {filename} with detected language: {language}")
    
#     save_language_output(detected_languages, output_file)

# # Example usage
# if __name__ == "__main__":
#     raw_data_folder = '../articles'  # Path to your articles folder
#     output_file = os.path.join('trained_model', 'language_model', 'detected_languages.txt')  # Path to save the output
    
#     # Process the articles and save the detected languages to the output file
#     process_articles_and_save_languages(raw_data_folder, output_file)



import os
import logging
from langdetect import detect
import re

# Setup logging
logging.basicConfig(filename='language_detection.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to detect language (e.g., Nepali for multilingual processing)
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except Exception as e:
        logging.error(f"Error detecting language: {e}")
        return "unknown"

# Function to save detected languages to a file (keeping original structure)

# Function to save detected languages to a file in human-readable format
def save_language_output(languages, output_file):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            for filename, lang in languages.items():
                # Remove extension and replace underscores with spaces
                title = os.path.splitext(filename)[0].replace('_', ' ')
                # Add colon after truncated leading underscores (if any)
                title = re.sub(r'^(\s*):', '', title)
                # Capitalize first letter of each sentence
                cleaned_title = title.strip().capitalize()

                f.write(f"{cleaned_title}\n\n")  # Add double newline for readability

        logging.info(f"Cleaned language titles saved at {output_file}")
        print(f"Language prediction file saved at: {output_file}")

    except Exception as e:
        logging.error(f"Error saving language detection output: {e}")
        print(f"Error saving language detection output: {e}")


# Function to process each article
def process_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        article_text = f.read().strip()
    return detect_language(article_text)

# Main processing loop for all articles in the folder
def process_articles_and_save_languages(raw_data_folder):
    detected_languages = {}
    
    for filename in os.listdir(raw_data_folder):
        if filename.endswith('.txt'):  # Only process .txt files
            file_path = os.path.join(raw_data_folder, filename)
            language = process_article(file_path)
            detected_languages[filename] = language
            logging.info(f"Processed {filename} with detected language: {language}")
    
    # Define the output path, removing the extra 'nlp' from the path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    base_path = os.path.join(root_dir, 'models', 'trained_model', 'language_model')  # Corrected path
    
    # Output file path where language prediction will be saved
    output_file = os.path.join(base_path, 'detected_languages.txt')
    
    save_language_output(detected_languages, output_file)

# Example usage
if __name__ == "__main__":
    raw_data_folder = '../articles'  # Path to your articles folder
    
    # Process the articles and save the detected languages to the output file
    process_articles_and_save_languages(raw_data_folder)
