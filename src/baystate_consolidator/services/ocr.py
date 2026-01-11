import os
from typing import Dict, Any
import openai


class OCRService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def extract_product_data(self, image_url: str) -> Dict[str, Any]:
        prompt = """
        Extract the following information from the product image:
        - Ingredients list (full text)
        - Net Weight
        - Nutrition Facts (summary)
        Return as JSON.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url,
                                },
                            },
                        ],
                    }
                ],
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if content:
                import json

                return json.loads(content)
        except Exception as e:
            print(f"OCR Error: {e}")

        return {}
