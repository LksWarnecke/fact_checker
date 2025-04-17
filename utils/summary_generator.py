import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_prompt(topic, values):
    return f"""
You are a helpful assistant analyzing global trends.
Write a short paragraph (3-5 sentences) summarizing the improvement in {topic} over the past 100 years, based on the following data:

- In 1920: {values.get(1920)}  
- In 1970: {values.get(1970)}  
- In 2020: {values.get(2020)}  

Mention any significant trends, improvements, or milestones. Be factual and optimistic.
"""

def generate_why_it_matters_prompt(topic, values):
    return f"""
You are an insightful assistant helping people understand global improvements.
Explain why the improvement in {topic} over the past 100 years matters. Provide an explanation of its significance and the impact it has had on global society, based on the following data:

- In 1920: {values.get(1920)}  
- In 1970: {values.get(1970)}  
- In 2020: {values.get(2020)}  

Your explanation should focus on the positive impact and why these improvements are crucial for society.
"""

def get_summary(topic, values):
    prompt = generate_prompt(topic, values)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def get_why_it_matters(topic, values):
    prompt = generate_why_it_matters_prompt(topic, values)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()