import pandas as pd
import random

# Define role required skills
ROLE_SKILLS = {
    "Product Manager": ["project management", "communication", "strategy"],
    "Technical Lead": ["programming", "system design", "cloud computing"],
    "UI/UX Designer": ["UI design", "UX research", "wireframing"],
    "Financial Analyst": ["budgeting", "forecasting", "financial modeling"]
}

def create_synthetic_data(num_innovations=10, num_innovators=20):
    data = []
    roles = list(ROLE_SKILLS.keys())

    for innovation_id in range(1, num_innovations + 1):
        innovation_location = random.choice(["Kampala", "Mbarara", "Gulu"])
        innovation_categories = random.sample(
            ["FinTech", "HealthTech", "AgriTech", "EdTech"], k=2
        )

        for role in roles:
            required_skills = ROLE_SKILLS[role]
            for innovator_id in range(1, num_innovators + 1):
                innovator_location = random.choice(["Kampala", "Mbarara", "Gulu"])
                innovator_interests = random.sample(
                    ["FinTech", "HealthTech", "AgriTech", "EdTech"], k=2
                )
                innovator_skills = random.sample(
                    ["project management", "communication", "strategy",
                     "programming", "system design", "cloud computing",
                     "UI design", "UX research", "wireframing",
                     "budgeting", "forecasting", "financial modeling"],
                    k=3
                )

                # Feature engineering
                location_match = int(innovation_location == innovator_location)
                interest_match = len(set(innovation_categories).intersection(innovator_interests))
                skill_match = len(set(required_skills).intersection(innovator_skills))

                # Define suitability based on arbitrary conditions
                suitable = 1 if (location_match and interest_match >= 1 and skill_match >= 1) else 0

                # Append to dataset
                data.append({
                    "innovation_id": innovation_id,
                    "innovator_id": innovator_id,
                    "role": role,
                    "location_match": location_match,
                    "interest_match": interest_match,
                    "skill_match": skill_match,
                    "suitable": suitable
                })

    # Convert to DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv('../data/synthetic_training_data.csv', index=False)
    print("Synthetic data saved to '../data/synthetic_training_data.csv'.")

# Run the function to generate and save data
create_synthetic_data()
