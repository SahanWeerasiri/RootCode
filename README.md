
# Sri Lanka Tourism Recommendation System

## Overview

This project is a recommendation system that suggests tourism destinations in Sri Lanka based on user preferences such as bucket list destinations and activities they enjoy. The model uses machine learning techniques to analyze user data and recommend top N destinations.

## Requirements

To run this model, you need the following dependencies:

- Python 3.6+
- NumPy
- Scikit-learn
- TensorFlow/Keras (for deep learning)
- Pandas
- Pickle (for saving/loading model)
- Re (for text cleaning)
- NLTK (optional for more advanced text processing)
- Logging (for application logs)

You can install the required packages using:

```bash
pip install numpy pandas scikit-learn tensorflow
```

## Model Files

1. **recommendation_model.pkl**: This file contains the trained model and data for the recommendation system. It includes vectorizers, encoders, and the trained ML/DL model.

2. **example_user_recommendations.txt**: Output file where user recommendations will be saved.

## User Data Structure

The model processes user data, including bucket list destinations and preferred activities, and compares it against the available tourism destinations.

### Example User Data:
```python
example_user = {
    'User ID': 10001,
    'Name': 'John Doe',
    'Email': 'john.doe@example.com',
    'Preferred Activities': ['hiking', 'beach visits', 'tea tasting'],
    'Bucket list destinations Sri Lanka': ['Sigiriya', 'Yala National Park', 'Galle Fort']
}
```

- **Preferred Activities**: A list of activities the user enjoys.
- **Bucket list destinations Sri Lanka**: Places the user wishes to visit in Sri Lanka.

## Steps to Use the Model

### 1. Load the Model

To use the recommendation system, first, load the saved model from the pickle file:

```python
import pickle

# Load the saved model
with open('recommendation_model.pkl', 'rb') as f:
    loaded_model_data = pickle.load(f)
```

### 2. Process User Data

User data is cleaned and preprocessed. The bucket list places are matched against the model’s dataset using vectorizers to ensure accuracy.

The function `process_user_data(user_data, model_data)` will handle:
- Cleaning the bucket list destinations.
- Matching user preferences with the places in the model's dataset.
- Encoding user activities for further processing.

### 3. Generate Recommendations

Use the `recommend_places(user_data, model_data, top_n=5)` function to generate top N recommendations for the user.

Example:

```python
example_user = {
    'User ID': 10001,
    'Name': 'John Doe',
    'Email': 'john.doe@example.com',
    'Preferred Activities': ['hiking', 'beach visits', 'tea tasting'],
    'Bucket list destinations Sri Lanka': ['Sigiriya', 'Yala National Park', 'Galle Fort']
}

# Get recommendations for the user
example_recommendations = recommend_places(example_user, loaded_model_data)

# Print recommendations
print("Recommendations for John Doe:")
for place, score in example_recommendations:
    print(f"{place}: {score:.4f}")
```

### 4. Save the Output

The results can be saved to a text file using the following code:

```python
with open('example_user_recommendations.txt', 'w') as f:
    f.write("Recommendations for John Doe:
")
    for place, score in example_recommendations:
        f.write(f"{place}: {score:.4f}
")

    f.write("
User Details:
")
    json.dump(example_user, f, indent=2)
```

### 5. Logging

The script includes logging for tracking and debugging purposes. Modify the `logging` settings as needed.

---

## Additional Information

### Model Data

- **places_name_tfidf**: TF-IDF matrix for place names.
- **places_combined_tfidf**: TF-IDF matrix combining place name and description.
- **name_vectorizer**: Vectorizer used for encoding place names.
- **combined_vectorizer**: Vectorizer for combined features (name + description).
- **model**: The trained machine learning or deep learning model that predicts the best matching destinations based on user preferences.

### Parameters

- `top_n`: Specifies how many recommendations you want to generate. The default is 5.

---

### Example Output

```
Recommendations for John Doe:
Yala National Park: 0.9123
Sigiriya: 0.8712
Galle Fort: 0.8571
Ella: 0.8435
Nuwara Eliya: 0.8124
```

This README should help you understand and use the recommendation system effectively.
