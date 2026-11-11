# -*- coding: utf-8 -*-
import sys, json, os
from test_quiz_data import QUIZ_QUESTIONS

quiz_json_string = json.dumps(QUIZ_QUESTIONS, ensure_ascii=False)

# Read build_detail_page.py to clean it up
with open('d:/WEB 2/khKt/generate_build_detail_page.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Instead of doing string replacement that breaks, we embed the json string directly
with open('d:/WEB 2/khKt/vietnam-map/data/quiz_questions.json', 'w', encoding='utf-8') as f:
    f.write(quiz_json_string)

with open('d:/WEB 2/testweb/vietnam-map/data/quiz_questions.json', 'w', encoding='utf-8') as f:
    f.write(quiz_json_string)

print("Saved quiz_questions.json successfully!")
