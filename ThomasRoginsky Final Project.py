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

def recommend_body_style_by_people():
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
        except ValueError:
            print("\nPlease enter a whole number... since we don't sell cars to people who want to transport half of a person. " \
                  "\n*heavy sigh*")

   
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

    return people, body_style

def ask_offroad_need():
   
    while True:
        choice = input("\nWill your vehicle need off-road capability? Type either 'yes' or 'no': ").strip().lower()
        if choice in ("yes", "y"):
            return "Yes"
        if choice in ("no", "n"):
            return "No"
        print("Please answer yes or no.")

def load_models(filename="models_by_body_style.txt"):
    
    models = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            offroad, body_style, brand, model = line.split(",")
            offroad = offroad.strip()
            body_style = body_style.strip()
            brand = brand.strip()
            model = model.strip()

            models.setdefault(body_style, []).append({
                "brand": brand,
                "model": model,
                "offroad": offroad.lower() == "yes"})

    return models

def recommend_models_from_file(body_style, selected_brand, offroad_needed, models_dict, top_n=1):
    
    # Normalize body style label to match file keys
    # Your body_style strings include extra text like "SUV (3-row recommended)"
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

    options = models_dict.get(key, [])

    
    if offroad_needed == "Yes":
        options = [m for m in options if m.get("offroad")]


    # If user chose a brand, try to prioritize matching brand
    if "No brand preference" not in selected_brand:
        brand_matches = [m for m in options if m["brand"].lower() == selected_brand.lower()]
        if brand_matches:
            return brand_matches[:top_n]

    # Otherwise return general options
    return options[:top_n]

def generate_vehicle_recommendation(profile, models_dict):
    models = recommend_models_from_file(
        profile["recommended_body_style"],
        profile["brand"],
        "Yes" if profile["needs_offroad"] else "No",
        models_dict,
        top_n=1
    )

    recommendation = (
        "\n====== FINAL VEHICLE RECOMMENDATION ======\n"
        f"Brand Preference: {profile['brand']}\n"
        f"Passengers: {profile['passengers']}\n"
        f"Recommended Body Style: {profile['recommended_body_style']}\n"
        f"Off-road Capability: {'Yes' if profile['needs_offroad'] else 'No'}\n"
        "\nTop Model Suggestion:\n"
    )

    if not models:
        recommendation += "  • No models are currently found in our database for your preferences.\n"
    else:
        for m in models:
            recommendation += f"  • {m['brand']} {m['model']}\n"

    recommendation += "========================================\n"
    return recommendation


def main():
    while True:
        selected_brand = choose_brand_from_file()
        people, body_style = recommend_body_style_by_people()
        offroad_needed = ask_offroad_need()

        print("\nPlease verify your following inputs:" \
            "\nAs a brand, you selected:", selected_brand,
            "\nUsual total number of people in the car:", people,
            "\nOff-road capability needed:", offroad_needed)
        
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

        print(generate_vehicle_recommendation(profile, models_dict))
        break

if __name__ == "__main__":
    main()



