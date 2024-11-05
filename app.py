from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('models/model.pkl')

# Define role required skills
ROLE_SKILLS = {
    "Product Manager": ["project management", "communication", "strategy"],
    "Technical Lead": ["programming", "system design", "cloud computing"],
    "UI/UX Designer": ["UI design", "UX research", "wireframing"],
    "Financial Analyst": ["budgeting", "forecasting", "financial modeling"]
}


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    innovations = data['innovations']
    innovators = data['innovators']

    predictions = []
    for innovation in innovations:
        roles = innovation["roles"]
        for role in roles:
            required_skills = ROLE_SKILLS.get(role, [])
            for innovator in innovators:
                location_match = int(innovation["location"] == innovator["location"])
                interest_match = len(set([c['category_name'] for c in innovation['categories']])
                                     .intersection([i['category_name'] for i in innovator['interests']]))
                skill_match = len(set(required_skills).intersection([s['skill_name'] for s in innovator['skills']]))

                # Prepare data point for prediction
                X_new = pd.DataFrame([{
                    "location_match": location_match,
                    "interest_match": interest_match,
                    "skill_match": skill_match
                }])
                suitable = model.predict(X_new)[0]

                predictions.append({
                    "innovation_id": innovation["id"],
                    "innovator_id": innovator["id"],
                    "role": role,
                    "location_match": location_match,
                    "interest_match": interest_match,
                    "skill_match": skill_match,
                    "suitable": int(suitable)
                })

    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
