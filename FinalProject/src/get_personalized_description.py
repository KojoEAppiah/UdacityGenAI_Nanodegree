from openai import OpenAI
import os

openai_client = OpenAI(
    base_url = "https://openai.vocareum.com/v1", #os.environ["OPENAI_API_BASE"]
    api_key = "voc-773311951266772589854675381736bc788.33953517" #os.environ["OPENAI_API_KEY"]
)


def get_personalized_description(property, user_preferences):

    property_description = f"""
        Neighborhood: {property["neighborhood_name"]}
        Price: ${property["price"]}
        Bedrooms: {property["bedrooms"]}
        Bathrooms: {property["bathrooms"]}
        House Size: {property["size"]} sqft

        Description: {property["description"]}
        Neighborhood Description: {property["neighborhood_description"]}
"""

    prompt = f"{property_description} \n ------------------- \n Summarize the property above in a way that would appeal to a potential buyer with the following preferences: \n{user_preferences}\n Emphasize the qualities of the property that fit what the buyer is looking for.  Do not lie.  Do not say that the price is different than what is listed above. Be concise, and be honest (do not lie about the price or any of the other features).  Produce one paragraph no more than a few sentences long, nothing else."
    
    return generate_personalized_description(prompt)

def generate_personalized_description(prompt):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are a real estate agent.  You are attempting to sell a property to an potential buyer."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            temperature=1,
            max_completion_tokens=1260,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # The response is a JSON object containing more information than the generated review. We want to return only the message content
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"