from fastapi import FastAPI
from dotenv import load_dotenv
import google.generativeai as genai
import os
import requests



# configs
load_dotenv()
llm_api_key = os.getenv("LLM_API_KEY")
if not llm_api_key:
    raise ValueError("請先設定 GEMINI_API_KEY 環境變數")

config = {
	"model":"gemini-2.5-flash",
	"endpoint":"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
	"llm_api_key":llm_api_key
}



# def get_llm_answer(model:str, endpoint:str, llm_api_key:str, prompt:str):
def get_llm_answer(config:dict, prompt:str):
	headers = {
	    "Content-Type": "application/json",
	    "x-goog-api-key": config['llm_api_key']
	}

	data = {
		"contents": [
	        {
	            "parts": [
	                {
	                    "text": prompt
	                }
	            ]
	        }
	    ]
	}

	response = requests.post(config['endpoint'], headers=headers, json=data)

	if response.status_code == 200:
		result = response.json()
		text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
		print("Generated text:", text)
		return {"message":text}
	else:
		print("Request failed:", response.status_code)
		print(response.text)
		return {"message":"error"}


prompt = "人工智慧是什麼"
print(get_llm_answer(config, prompt))











# app = FastAPI()

# genai.configure(api_key=llm_api_key)
# model = genai.GenerativeModel("gemini-2.5-flash")
# prompt = "用簡單的話解釋什麼是人工智慧"
# response = model.generate_content(prompt)
# print("=== Gemini Response ===")
# print(response.text)

# if __name__ == "__main__":
# 	uvcorn.run("main:app", host="0.0.0.0", port=8101, reload=True)