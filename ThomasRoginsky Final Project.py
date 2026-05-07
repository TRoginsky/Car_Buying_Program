#ThomasRoginsky Final Project

# imports the os module, which provides a way of using operating system dependent functionality, such as running shell commands
import os 
os.system("curl -o topbrands.txt https://raw.githubusercontent.com/TRoginsky/Car_Buying_Program/refs/heads/main/topbrands.txt")

os.system("curl -o models_by_body_style.txt https://raw.githubusercontent.com/TRoginsky/Car_Buying_Program/refs/heads/main/models_by_body_style.txt")


# creates a function to read the brands from the file and allow the user to select one or none
def choose_brand_from_file(filename="topbrands.txt"):
    input("\nWelcome to the car locating assistance program (CLAP), where we aim to find the right car for you!"
          "\nPress the 'Enter' key on your keyboard to view the Top Luxury Brands") 

    # reads the brands from the file into a list, stripping whitespace and ignoring empty lines
    with open(filename, "r") as f:
        brands = [line.strip() for line in f if line.strip()]

    # prints the list of brands with numbers for selection
    print("\nTop Luxury Brands List:")
    for i, brand in enumerate(brands, start=1):
        print(f"{i}. {brand}")

    # creates a lowercase version of the brands list for case-insensitive comparison
    brands_lower = [b.lower() for b in brands]

    # prompts the user to select a brand by number, name, or indicate no preference, and validates the input
    while True:
        choice = input("\nPick a brand by typing the number, brand name, or 'no' if you don't have a preference: ").strip()

        # checks if the user indicated no preference
        if choice.lower() in ("no", "n", "none"):
            return "No brand preference selected."

        # checks if the user input is a digit and corresponds to a valid brand number, and returns the selected brand
        if choice.isdigit():
            idx = int(choice) - 1

            # checks if index is w/i the valid range, otherwise prompts the user to enter a valid number
            if 0 <= idx < len(brands):
                return brands[idx]
            print(f"Please enter a number between 1 and {len(brands)}.")
            continue

        # checks if the user input matches a brand name in the list (case-insensitive), and returns the selected brand
        if choice.lower() in brands_lower:
            return brands[brands_lower.index(choice.lower())]

        print("Invalid choice. Enter a listed number, a listed brand name, or 'no'.")

        # closes the file to free up system resources and ensure that any changes made to the file are saved properly.
        filename.close() 

# creates a function to recommend a body style based on the number of people in the car, with input validation for a range of 1-15
def recommend_body_style_by_people():

    # using a while loop to check the correctness of the input
    while True:
        try:
            people = int(input("\nEnter the total people are usually in the car (including the driver, max of 15)? "))
            if 1 <= people <= 15:
                break
            if people < 1:
                print("\nWho's driving this thing?!?!" \
                      "\n*heavy sigh* " \
                      "\nPlease enter a number the number of people in the car that is at least 1.")
            else:
                print("\nPlease enter a number of people that is no more than 15. This is a car, not a bus program.")

        # catches error if input is not a valid integer
        except ValueError:
            print("\nPlease enter a whole number... since we don't sell cars to people who want to transport half of a person. " \
                  "\n*heavy sigh*")

   # recommends a body style based on the number of people, with specific categories for different ranges of passengers
    if people <= 2:
        body_style = "Coupe"
    elif people <= 5:
        body_style = "Sedan"
    elif people <= 7:
        body_style = "SUV (3-row recommended)"
    elif people >= 8:
        body_style = "Minivan"
    else:
        body_style = "Full-size Van"

    # returns the number of people and the recommended body style as a tuple
    return people, body_style

# creates a function to ask the user if they need off-road capability, with input validation for yes/no responses
def ask_offroad_need():
   
   # using a while loop to check the correctness of the input, and prompting the user until they provide a valid response
    while True:
        choice = input("\nWill your vehicle need off-road capability? Type either 'yes' or 'no': ").strip().lower()
        if choice in ("yes", "y"):
            return "Yes"
        if choice in ("no", "n"):
            return "No"
        print("Please answer yes or no.")

# creates a function to load the car models from a file and organize them by body style, with details on brand, model, and off-road capability
def load_models(filename="models_by_body_style.txt"):
    
    # initializes an empty dictionary to store the models organized by body style
    models = {}

    # reads the models from the file, stripping whitespace and ignoring empty lines
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # splits each line into components based on commas, and assigns them to variables for off-road capability, body style, brand, and model
            offroad, body_style, brand, model = line.split(",")
            offroad = offroad.strip()
            body_style = body_style.strip()
            brand = brand.strip()
            model = model.strip()

            # adds the model information to the dictionary under the appropriate body style, creating a list of models for each body style
            models.setdefault(body_style, []).append({
                "brand": brand,
                "model": model,
                "offroad": offroad.lower() == "yes"})
    
    # closes the file to free up system resources and ensure that any changes made to the file are saved properly.
    filename.close()
    return models

# function to recommend car models based on the user's preferences for body style, brand, and off-road capability, using the loaded models from the file
def recommend_models_from_file(body_style, selected_brand, offroad_needed, models_dict, top_n=1):
    
    # finds the key in the models dict that matches the recommended body style
    if "SUV" in body_style:
        key = "SUV"
    elif "Sedan" in body_style:
        key = "Sedan"
    elif "Coupe" in body_style:
        key = "Coupe"
    elif "Minivan" in body_style:
        key = "Minivan"
    else:
        key = "Van"

    # retrieves the list of models for the identified body style from the models dictionary
    options = models_dict.get(key, [])

    # filters the options based on the user's need for off-road capability
    if offroad_needed == "Yes":
        options = [m for m in options if m.get("offroad")]


    # loop looking for matches to the user's selected brand
    if "No brand preference" not in selected_brand:
        brand_matches = [m for m in options if m["brand"].lower() == selected_brand.lower()]
        if brand_matches:
            return brand_matches[:top_n]

    # otherwise return general options
    return options[:top_n]

# function to generate a final vehicle recommendation based on the user's profile and the models available in the dictionary
def generate_vehicle_recommendation(profile, models_dict):

    # calls the recommend_models_from_file function to get a list of recommended models based on the user's input
    models = recommend_models_from_file(
        profile["recommended_body_style"],
        profile["brand"],
        "Yes" if profile["needs_offroad"] else "No",
        models_dict,
        top_n=1
    )

    # formats the recommendation string to include the user's preferences and the top model suggestion
    recommendation = (
        "\n====== FINAL VEHICLE RECOMMENDATION ======\n"
        f"Brand Preference: {profile['brand']}\n"
        f"Passengers: {profile['passengers']}\n"
        f"Recommended Body Style: {profile['recommended_body_style']}\n"
        f"Off-road Capability: {'Yes' if profile['needs_offroad'] else 'No'}\n"
        "\nTop Model Suggestion:\n"
    )

    # handling cases where no models are found based on the user's input & database availability
    if not models:
        recommendation += "  • No models are currently found in our database for your preferences.\n"
    else:
        for m in models:
            recommendation += f"  • {m['brand']} {m['model']}\n"

    recommendation += "========================================\n"
    return recommendation

# main function to run the car recommendation program
def main():

    # while loop to call the functions in sequence
    while True:
        selected_brand = choose_brand_from_file()
        people, body_style = recommend_body_style_by_people()
        offroad_needed = ask_offroad_need()

        print("\nPlease verify your following inputs:" \
            "\nAs a brand, you selected:", selected_brand,
            "\nUsual total number of people in the car:", people,
            "\nOff-road capability needed:", offroad_needed)
        
        # checks if user wants to see the recommendation or start over, and handles the input accordingly
        confirm = input("\nPress Enter to see our recommendation, or type 'x' to start over: ").strip().lower()

        if confirm == "x":
            print("\nRestarting program...\n")
            continue

        models_dict = load_models("models_by_body_style.txt")

        profile = {
            "brand": selected_brand,
            "passengers": people,
            "recommended_body_style": body_style,
            "needs_offroad": offroad_needed == "Yes"
        }

        # prints the final vehicle recommendation and ends the program
        print(generate_vehicle_recommendation(profile, models_dict))
        break

# checks if the script is being run directly (as the main program) and calls the main function to start the program
if __name__ == "__main__":
    main()



