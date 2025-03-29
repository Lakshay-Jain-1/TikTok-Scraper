import os
import json
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  

class RefinedData(BaseModel):
    refined_queries: list[str]
    refined_hashtags: list[str]

def clean_gemini_response(response_text: str) -> str:
    """Cleans Gemini AI's response by removing markdown formatting (triple backticks)."""
    return response_text.strip().removeprefix("```json").removesuffix("```").strip()

def refine_query_and_hashtags(queries, hashtags):
    """Enhances queries and hashtags using Gemini AI."""

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    Enhance the following search queries and hashtags for better SEO and relevancy.
    Fix any typos and suggest better alternatives.

    Queries: {queries}
    Hashtags: {hashtags}

    Respond in JSON format:
    {{
      "refined_queries": list[str],
      "refined_hashtags": list[str]
    }}
    """

    response = model.generate_content(prompt)

    try:
        # Clean the response before parsing
        cleaned_response = clean_gemini_response(response.text)
        
        # Use model_validate_json instead of parse_raw
        data = RefinedData.model_validate_json(cleaned_response)
        
        return [data.refined_queries, [ x[1:] for x in data.refined_hashtags]]
       

    except Exception as e:
       return [queries, hashtags]

