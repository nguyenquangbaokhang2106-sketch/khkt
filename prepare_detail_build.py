import sys, json, os

with open('d:/WEB 2/khKt/test_quiz_data.py', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('QUIZ_QUESTIONS = [')
end_idx = text.rfind(']') + 1
quiz_code = text[start_idx:end_idx]

print("Quiz questions block length:", len(quiz_code))
