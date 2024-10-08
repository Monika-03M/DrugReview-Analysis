"""
Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OGx-INS8jg2uvFeR1F1KvKBdUs7_wgKN
"""
import nltk
nltk.download('vader_lexicon')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
import os

def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']

def categorize_sentiment(score):
    if score < -0.05:
        return 'Negative'
    elif score > 0.05:
        return 'Positive'
    else:
        return 'Neutral'

def visualize_sentiment_for_drug(drugname, review, save_to=None):
    df = pd.read_csv('datasets/drug_data.csv')
    
    # Clean the data
    df['review'] = df['review'].astype(str)
    df['review'] = df['review'].fillna('')
    df['review'] = df['review'].apply(lambda x: x.strip())
    
    # Filter the data for the given drugname
    drug_data = df[df['drugname'].str.lower() == drugname.lower()]
    
    # Calculate sentiment for the input review
    sentiment_score = get_sentiment(review)
    sentiment_category = categorize_sentiment(sentiment_score)
    
    results = {
        "drug_name": drugname,
        "review_text": review,
        "sentiment_score": sentiment_score,
        "sentiment_category": sentiment_category,
        "sentiment_distribution": None,
        "visualization_path": None,
        "message": None
    }
    
    if sentiment_category == 'Negative':
        if len(drug_data) == 0:
            results["message"] = f"No reviews found for {drugname}"
            return results

        # Calculate sentiment distribution
        sentiment_counts = drug_data['sentiment_class'].value_counts()
        results["sentiment_distribution"] = sentiment_counts.to_dict()
        
        # Plot a pie chart
        plt.figure(figsize=(4, 4))
        plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
        plt.title(f'Sentiment Distribution for {drugname}')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        if save_to:
            plt.savefig(save_to)  # Save the plot to a file if save_to is provided
            plt.close()  # Close the plot to avoid displaying it when not needed
            results["visualization_path"] = save_to
        else:
            plt.show()  # Display the plot if not saving it
    else:
        results["message"] = "The review is not negative. No visualization generated."
    
    return results
    
    

'''#Main loop for user input
drug_name = input("Enter the drug name (or 'quit' to exit): ")

review = input("Enter your review: ")

results = visualize_sentiment_for_drug(drug_name, review)

# Print the results
print(f"\nResults for {results['drug_name']}:")
print(f"Review: {results['review_text']}")
print(f"Sentiment score: {results['sentiment_score']:.2f}")
print(f"Sentiment category: {results['sentiment_category']}")

if results['sentiment_category'] == 'Negative' and results['sentiment_distribution']:
    print("\nSentiment distribution:")
    for category, count in results['sentiment_distribution'].items():
        print(f"{category}: {count} ({count/sum(results['sentiment_distribution'].values())*100:.1f}%)")
    
    if results["visualization_path"]:
        print(f"Visualization saved to: {results['visualization_path']}")
else:
    print(results.get("message", "No further analysis was performed."))'''




'''def search_drugs_by_condition(condition):
    # Base URL for OpenFDA Drug Label API
    BASE_URL = 'https://api.fda.gov/drug/label.json'

    # Make the API request with the condition as a search term
    query = f'indications_and_usage:"{condition}"'
    response = requests.get(f'{BASE_URL}?search={query}&limit=50')  # Increase limit to get more results

    if response.status_code == 200:
        data = response.json()
        drugs = []
        for result in data.get('results', []):
            openfda = result.get('openfda', {})
            brand_names = openfda.get('brand_name', [])
            if brand_names:
                drugs.append(brand_names[0])
            if len(drugs) == 5:  # Stop once we have 5 drugs
                break

        return drugs if drugs else "Not found for the given condition"
    else:
        return f"Error: {response.status_code}"
        return []
'''

'''# Example usage
condition = input("Enter the condition: ")
top_drugs = search_drugs_by_condition(condition)
print(f"Top drugs for {condition}: {top_drugs}")'''