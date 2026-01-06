 emr_application_.py
# Sunrise Hospital EMR System

import pandas as pd
import matplotlib.pyplot as plt25

import requests

# -----------------------------
# Fetch and clean patient data
# -----------------------------
def fetch_and_clean_data(url):
    """
    Fetch patient data from an API and clean it for analysis.
    Adds simulated age and condition data.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)

        # Rename patients for realism
        custom_names = [
            "Amani Mwangi", "Neema Hassan", "Juma Odhiambo", "Zawadi Nyerere",
            "Baraka Kimani", "Fatuma Ali", "Hassan Abdallah",
            "Rehema Mussa", "Joseph Kibet", "Salma Suleiman"
        ]
        df["name"] = custom_names

        df["email"] = df["email"].str.lower()

        # Simulated ages
        df["age"] = [25, 34, 45, 52, 29, 41, 38, 60, 33, 48]

        # Simulated medical conditions
        df["condition"] = [
            "Flu", "Hypertension", "Diabetes", "Fever",
            "Flu", "Hypertension", "Diabetes", "Hypertension",
            "Fever", "Flu"
        ]

        return df

    except requests.exceptions.RequestException as err:
        print(f"Error fetching data: {err}")
        return pd.DataFrame()


# -----------------------------
# Filter patients by age range
# -----------------------------
def filter_by_age(df, min_age, max_age):
    try:
        return df[(df["age"] >= min_age) & (df["age"] <= max_age)]
    except KeyError:
        print("Age column not found.")
        return pd.DataFrame()


# -----------------------------
# Analyze data
# -----------------------------
def analyze_data(df):
    if df.empty:
        return {
            "total_patients": 0,
            "unique_domains": 0,
            "condition_counts": {},
            "mean_age": 0
        }

    total_patients = len(df)
    unique_domains = df["email"].str.split("@", expand=True)[1].nunique()
    condition_counts = df["condition"].value_counts().to_dict()
    mean_age = round(df["age"].mean(), 2)

    return {
        "total_patients": total_patients,
        "unique_domains": unique_domains,
        "condition_counts": condition_counts,
        "mean_age": mean_age
    }


# -----------------------------
# Visualizations
# -----------------------------
def visualize_data(analysis, df, filtered=False):
    if not analysis["condition_counts"]:
        print("No data to visualize.")
        return

    # Bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(
        analysis["condition_counts"].keys(),
        analysis["condition_counts"].values(),
        color=["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    )
    plt.xlabel("Condition")
    plt.ylabel("Number of Patients")
    plt.title("Condition Prevalence – Sunrise Hospital")
    plt.tight_layout()
    plt.savefig("conditions_plot.png")
    plt.close()

    # Pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(
        analysis["condition_counts"].values(),
        labels=analysis["condition_counts"].keys(),
        autopct="%1.1f%%",
        colors=["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    )
    plt.title("Condition Distribution")
    plt.savefig("conditions_pie.png")
    plt.close()

    # Age histogram
    plt.figure(figsize=(8, 6))
    plt.hist(df["age"], bins=6, color="#64B5CD", edgecolor="black")
    plt.xlabel("Age")
    plt.ylabel("Number of Patients")
    plt.title("Age Distribution" + (" (Filtered)" if filtered else ""))
    filename = "filtered_age_distribution.png" if filtered else "age_distribution.png"
    plt.savefig(filename)
    plt.close()


# -----------------------------
# Save analysis to file
# -----------------------------
def save_analysis(analysis, filename):
    try:
        with open(filename, "w") as file:
            file.write("Sunrise Hospital EMR Analysis Summary\n")
            file.write("-----------------------------------\n")
            file.write(f"Total Patients: {analysis['total_patients']}\n")
            file.write(f"Unique Email Domains: {analysis['unique_domains']}\n")
            file.write(f"Mean Age: {analysis['mean_age']}\n")
            file.write("Condition Frequencies:\n")
            for condition, count in analysis["condition_counts"].items():
                file.write(f"- {condition}: {count}\n")
    except IOError as err:
        print(f"File error: {err}")


# -----------------------------
# Get age range input
# -----------------------------
def get_age_range():
    while True:
        try:
            min_age = int(input("Enter minimum age: "))
            max_age = int(input("Enter maximum age: "))
            if min_age < 0 or max_age < min_age:
                print("Invalid age range. Try again.")
                continue
            return min_age, max_age
        except ValueError:
            print("Please enter valid numbers.")


# -----------------------------
# Main menu
# -----------------------------
def main():
    url = "https://invalid-api-url.com/users"

    patient_data = pd.DataFrame()
    filtered_data = pd.DataFrame()

    print("\nWelcome to the Sunrise Hospital EMR System")

    while True:
        print("\nMenu Options:")
        print("1. Fetch patient data")
        print("2. Filter patients by age")
        print("3. View analysis and visualizations")
        print("4. Exit")

        choice = input("Enter choice (1-4): ")

        if choice == "1":
            patient_data = fetch_and_clean_data(url)
            filtered_data = pd.DataFrame()
            if not patient_data.empty:
                print("Patient data loaded successfully.")
            else:
                print("Failed to load patient data.")

        elif choice == "2":
            if patient_data.empty:
                print("Fetch data first.")
                continue
            min_age, max_age = get_age_range()
            filtered_data = filter_by_age(patient_data, min_age, max_age)
            print(filtered_data[["name", "age", "condition"]])

        elif choice == "3":
            if patient_data.empty:
                print("Fetch data first.")
                continue
            df = filtered_data if not filtered_data.empty else patient_data
            analysis = analyze_data(df)
            visualize_data(analysis, df, filtered=not filtered_data.empty)
            output_file = "filtered_analysis_summary.txt" if not filtered_data.empty else "analysis_summary.txt"
            save_analysis(analysis, output_file)

            print("\nAnalysis Summary")
            print(f"Total Patients: {analysis['total_patients']}")
            print(f"Unique Email Domains: {analysis['unique_domains']}")
            print(f"Mean Age: {analysis['mean_age']}")
            print("Condition Frequencies:")
            for c, n in analysis["condition_counts"].items():
                print(f"- {c}: {n}")

        elif choice == "4":
            print("Exiting EMR System. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
