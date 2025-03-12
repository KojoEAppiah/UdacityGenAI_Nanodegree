import lancedb
import torch
from sentence_transformers import SentenceTransformer
import json
import time
from get_buyer_preferences import get_buyer_preferences
from get_personalized_description import get_personalized_description
from description import Description

print("\nCreating database...this may take a while...\n")

f = open("C:/Users/kojoe/code/gen_ai/HomeMatch/src/descriptions.json")
descriptions = json.load(f)

description_db_objects = [
    Description(
        neighborhood_name=d["Neighborhood"],
        price=int(d["Price"].replace(",", "").strip("$")),
        bedrooms=d["Bedrooms"],
        bathrooms=d["Bathrooms"],
        size=int(d["House Size"].replace(",", "").replace("sqft", "").strip()),
        description=d["Description"],
        neighborhood_description=d["Neighborhood Description"],
        vector=torch.zeros(1024),
    )
    for d in descriptions["descriptions"]
]


def create_database(data):
    db = lancedb.connect("~/lancedb")
    TABLE_NAME = "HOME_DESCRIPTIONS"
    db.drop_table(TABLE_NAME, ignore_missing=True)
    return db.create_table(
        TABLE_NAME,
        data,
        schema=Description.to_arrow_schema(),
    )


embeddings_model = SentenceTransformer("dunzhang/stella_en_1.5B_v5")

for description in description_db_objects:
    description.vector = embeddings_model.encode(description.to_string()).tolist()

table = create_database(description_db_objects)
table.create_fts_index(["description", "neighborhood_description"])

# Get buyer preferences, embed them, and send them as a query to the vector database
buyer_preferences = get_buyer_preferences()
preference_query = embeddings_model.encode(buyer_preferences)

# grab the 4 most relevant properties
results = table.search(preference_query)
relevant_properties = results.limit(3).to_list()

print("\n\n...Gathering appropriate properties based on your preferences...")
# Loop through the properties and generate personalized descriptions
personalized_descriptions = []
for relevant_property in relevant_properties:
    personalized_descriptionion = get_personalized_description(
        relevant_property, buyer_preferences
    )
    personalized_descriptions.append(personalized_descriptionion)

print(
    "\n\nBased on your preferences, here are 3 three short descriptions of some homes you might like: "
)
time.sleep(1.5)
for description in personalized_descriptions:
    print("\n------------------------------\n" + description + "\n")
    time.sleep(1.5)

selection = input(
    '\n________________________________\nWould you like to see the full description of any of these properties? If so enter 1,2, or 3. Otherwise, enter "exit" : '
)

if selection == "exit":
    print("Thank you for using HomeMatch! Goodbye!")
    exit()


def get_original_description(property):
    return f"""
Neighborhood: {property["neighborhood_name"]}
Price: ${property["price"]}
Bedrooms: {property["bedrooms"]}
Bathrooms: {property["bathrooms"]}
House Size: {property["size"]} sqft

Description: {property["description"]}

Neighborhood Description: {property["neighborhood_description"]}
        """


for i in range(3):
    if selection == str(i + 1):
        print("\n\nHere is the full description of the property you selected: ")
        print(get_original_description(relevant_properties[i]))
        print("\n\n")
        print("Thank you for using HomeMatch! Goodbye!")
        exit()
