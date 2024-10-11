import requests
from typing import AnyStr,Type
from gentopia.tools.basetool import BaseTool
from pydantic import BaseModel, Field

class NewsHeadlineArgs(BaseModel):
    category: str = Field("general", description="Category of news, e.g., 'technology', 'sports', 'economy', etc.")
    country: str = Field("us", description="Country code for the news (e.g., 'us' for the United States, 'in' for India).")

class NewsHeadline(BaseTool):
    """
    Agent that fetches the top news headlines based on the specified category and country.
    """
    name = "news_headline_agent"
    description = "Fetches top news headlines from a specified category and country."

    args_schema: Type[BaseModel] = NewsHeadlineArgs

    def _run(self, category: AnyStr, country: AnyStr) -> str:
        api_key = "cd388f013e014e64a211a5c9e3973712"  # Replace with your actual NewsAPI key
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('status') == 'ok':
                headlines = [article['title'] for article in data['articles'][:5]]  # Limit to 5 headlines
                return f"Here are the top {category} news headlines in {country.upper()}:\n" + "\n".join(headlines)
            else:
                return "Failed to fetch news: " + data.get('message', 'Unknown error.')
        except Exception as e:
            return f"An error occurred while fetching news: {str(e)}"

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented for this tool yet.")
