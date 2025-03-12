I used the code in get_descriptions.py to generate the initial listings.
I then sent them one by one through get_json_from_gpt to save some work.  I overwrote the .txt with the json.

The HomeMatch.py application will load the descriptions into a Description object (which is a LanceDB model).

We then create embedding vectors for each description, and store them along with the rest of their info in the Vector DB.

Then we gather user preferences and, if they choose to enter in attributes individually, we format their answers into a natural language string.
We then create an embedding from the preferences and use that embedding to query the vector database.
We gather the 3 most relevant listings and display them to the user.

Necessary modules can be found in requirements.txt