def get_buyer_preferences():
    questions = [
    "What size (in sqft) home are you looking for? ",
    "How much are you looking to pay? ",
    "How many bedrooms would you like? ",
    "How many bathrooms? ",
    "Amenities? "
    ]
    
    print("\nWelcome to HomeMatch! Please answer the following questions to help us find the perfect home for you.\n\n")
    
    selection = input(
        "Which would you like to do?\n 1. Enter your preferences individually      or \n 2. Enter a description of what you are looking for\n(please enter 1 or 2):  "
    )
    
    if int(selection) == 2:
        preferences = input("Please describe what you are looking for and press enter: "  )
        return preferences
    
    live_answers = []
    if int(selection) == 1:
        for question in questions:
           live_answers.append(input(question))

        size = live_answers[0]
        price = live_answers[1]
        bedrooms = live_answers[2]
        bathrooms = live_answers[3]
        amenities = live_answers[4]

        preferences = f"a {size} sqft house with {bathrooms} bathrooms, {bedrooms} bedrooms, {amenities}, and a price under {price}"
        return preferences