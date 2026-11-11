import re, json

with open('d:/WEB 2/khKt/test_quiz_data.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract QUIZ_QUESTIONS
start_idx = text.find('QUIZ_QUESTIONS = [')
end_idx = text.rfind(']') + 1
quiz_json_str = text[start_idx:end_idx]
print(f"Extracted quiz data, length: {len(quiz_json_str)}")
