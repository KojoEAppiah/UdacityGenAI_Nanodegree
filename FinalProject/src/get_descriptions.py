from openai import OpenAI


openai_client = OpenAI(
    base_url = "https://openai.vocareum.com/v1", #os.environ["OPENAI_API_BASE"]
    api_key = "voc-773311951266772589854675381736bc788.33953517" #os.environ["OPENAI_API_KEY"]
)

example_description = """
Neighborhood: Green Oaks
Price: $800,000
Bedrooms: 3
Bathrooms: 2
House Size: 2,000 sqft

Description: Welcome to this eco-friendly oasis nestled in the heart of Green Oaks. This charming 3-bedroom, 2-bathroom home boasts energy-efficient features such as solar panels and a well-insulated structure. Natural light floods the living spaces, highlighting the beautiful hardwood floors and eco-conscious finishes. The open-concept kitchen and dining area lead to a spacious backyard with a vegetable garden, perfect for the eco-conscious family. Embrace sustainable living without compromising on style in this Green Oaks gem.

Neighborhood Description: Green Oaks is a close-knit, environmentally-conscious community with access to organic grocery stores, community gardens, and bike paths. Take a stroll through the nearby Green Oaks Park or grab a cup of coffee at the cozy Green Bean Cafe. With easy access to public transportation and bike lanes, commuting is a breeze.
"""

prompt_template = f"{example_description} \n ------------------ \nProvide 5 descriptions of houses like the example above. Be sure to put some variety into the different fields. For example, perhaps a different Neighborhood, different price, different number of bathrooms, different number of bedrooms, and different sizes.  Please include variety in the overall appeal and price range as well, and don't forget to generate a neighborhood description for each"


def generate_home_description(prompt_template):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are a real estate agent.  You are creating descriptions of residential properties."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_template
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
    
print(generate_home_description(prompt_template))