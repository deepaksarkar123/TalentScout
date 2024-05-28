import os
from dotenv import load_dotenv
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Load environment variables from the .env file
# load_dotenv()

# Get the API key from environment variables (if needed in the future)
# API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

# Ensure the API key is set (optional check for future use)
# if not API_KEY:
    #st.warning("Google Generative AI API key not found in environment variables")

# Configure the VADER sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

def ask_questions():
    questions = [
        {
            "question": "Mr. Wisely asked, 'How do you decide which tree is the best fit for you?'",
            "options": [
                "I want a tree whose leaves and branches match my own principles and values.",
                "I look for a tree that offers lots of room to grow and plenty of opportunities to learn new things.",
                "The tree must have a cozy, supportive environment where I can feel at home."
            ]
        },
        {
            "question": "Mr. Wisely asked, 'How do you balance the need for a safe tree with the desire for adventurous opportunities?'",
            "options": [
                "I prefer a safe tree where I can be steady and secure.",
                "I seek out trees that offer thrilling growth opportunities, even if they come with risks.",
                "I look for a tree that offers both safety and some room for adventure, depending on the season of my life."
            ]
        },
        {
            "question": "Mr. Wisely asked, 'What would make you turn down a tree after exploring it?'",
            "options": [
                "If the tree doesn’t align with my long-term goals or personal growth.",
                "If the tree doesn’t meet my expectations for comfort or resources.",
                "If I feel that the tree’s atmosphere or values don’t match mine."
            ]
        },
        {
            "question": "Mr. Wisely questioned, 'What would you do if you got a better offer shortly after moving to a new tree?'",
            "options": [
                "I value loyalty and the commitment I’ve made to my new friends, so I would likely stay.",
                "I would carefully consider the new offer, thinking about my long-term goals.",
                "I would have an open chat with my new friends to discuss any concerns or possibilities."
            ]
        },
        {
            "question": "Mr. Wisely asked, 'How do you choose when you have multiple trees to consider?'",
            "options": [
                "I look at all trees at once to find the best overall fit.",
                "I often choose the first tree that meets my key needs.",
                "I wait to hear from my top choice, weighing each tree carefully."
            ]
        }
    ]
    return questions

def display_questions(questions):
    st.title("Firefly Forest")

    # Display the story introduction
    st.markdown("""
    <style>
        .intro {
            font-size: 18px;
            line-height: 1.6;
        }
        .question {
            font-weight: bold;
            margin-top: 20px;
        }
        .option {
            margin-left: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="intro">
    In the magical forest, there lived a squirrel named Aspen. One day, while looking for the perfect tree to live in, Aspen reached out to the wise old owl, Mr. Wisely, for help in choosing the right tree.
    </div>
    """, unsafe_allow_html=True)

    responses = []

    # Question 1
    st.markdown("<div class='question'>Mr. Wisely asked, 'How do you decide which tree is the best fit for you'? Aspen said:</div>", unsafe_allow_html=True)
    option = st.radio(
        "",
        [
            "I want a tree whose leaves and branches match my own principles and values.",
            "I look for a tree that offers lots of room to grow and plenty of opportunities to learn new things.",
            "The tree must have a cozy, supportive environment where I can feel at home."
        ],
        key="question_1",
        index=None
    )
    responses.append({"question": "How do you decide which tree is the best fit for you?", "answer": option})

    st.markdown("""
    <div class="intro">
    As they continued their journey, Mr. Wisely asked,
    </div>
    """, unsafe_allow_html=True)

    # Question 2
    st.markdown("<div class='question'>Aspen, 'How do you balance the need for a safe tree with the desire for adventurous opportunities'? Aspen answered:</div>", unsafe_allow_html=True)
    option = st.radio(
        "",
        [
            "I prefer a safe tree where I can be steady and secure.",
            "I seek out trees that offer thrilling growth opportunities, even if they come with risks.",
            "I look for a tree that offers both safety and some room for adventure, depending on the season of my life."
        ],
        key="question_2",
        index=None
    )
    responses.append({"question": "How do you balance the need for a safe tree with the desire for adventurous opportunities?", "answer": option})

    st.markdown("""
    <div class="intro">
    By noon, Aspen had explored and rejected several trees. Aspen was pondering whether to give up searching for the dream tree.
    </div>
    """, unsafe_allow_html=True)

    # Question 3
    st.markdown("<div class='question'>At this time, Mr. Wisely asked, 'What would make you turn down a tree after exploring it'? Now hungry and thirsty Aspen murmured:</div>", unsafe_allow_html=True)
    option = st.radio(
        "",
        [
            "If the tree doesn’t align with my long-term goals or personal growth.",
            "If the tree doesn’t meet my expectations for comfort or resources.",
            "If I feel that the tree’s atmosphere or values don’t match mine."
        ],
        key="question_3",
        index=None
    )
    responses.append({"question": "What would make you turn down a tree after exploring it?", "answer": option})

    st.markdown("""
    <div class="intro">
    Exhausted by evening, Aspen began wondering if at all the dream tree will ever be found.
    </div>
    """, unsafe_allow_html=True)

    # Question 4
    st.markdown("<div class='question'>Sensing the frustration, the wise old owl questioned Aspen, 'What would you do if you got a better offer shortly after moving to a new tree?' Unsure of finding the new home, Aspen answered:</div>", unsafe_allow_html=True)
    option = st.radio(
        "",
        [
            "I value loyalty and the commitment I’ve made to my new home, so I would likely stay.",
            "I would carefully consider the new offer, thinking about my long-term goals.",
            "I would have an open thought on any concerns or possibilities."
        ],
        key="question_4",
        index=None
    )
    responses.append({"question": "What would you do if you got a better offer shortly after moving to a new tree?", "answer": option})

    st.markdown("""
    <div class="intro">
    Finally, they discussed how to handle choosing between multiple trees.
    </div>
    """, unsafe_allow_html=True)

    # Question 5
    st.markdown("<div class='question'>Mr. Wisely enquired, 'How do you choose when you have multiple trees to consider?' Aspen thought for a while and said:</div>", unsafe_allow_html=True)
    option = st.radio(
        "",
        [
            "I look at all trees at once to find the best overall fit.",
            "I often choose the first tree that meets my key needs.",
            "I wait to hear from my top choice, weighing each tree carefully."
        ],
        key="question_5",
        index=None
    )
    responses.append({"question": "How do you choose when you have multiple trees to consider?", "answer": option})

    return responses

def analyze_sentiment(responses):
    st.title("Sentiment Analysis of Responses")
    
    for response in responses:
        if response["answer"] is not None:
            sentiment = sentiment_analyzer.polarity_scores(response["answer"])
            sentiment_label = "Positive" if sentiment['compound'] >= 0.45 else "Negative" if sentiment['compound'] <= 0.35 else "Neutral"
            st.write(f"**Question:** {response['question']}")
            st.write(f"**Answer:** {response['answer']}")
            st.write(f"**Sentiment:** {sentiment_label} (Compound Score: {sentiment['compound']:.2f})")
            st.markdown("---")

def summarize_sentiment(responses):
    st.title("Sentiment Analysis Summary")
    
    total_score = 0
    valid_responses = 0
    for response in responses:
        if response["answer"] is not None:
            sentiment = sentiment_analyzer.polarity_scores(response["answer"])
            total_score += sentiment['compound']
            valid_responses += 1

    if valid_responses > 0:
        avg_score = total_score / valid_responses
        overall_sentiment = "Positive" if avg_score >= 0.45 else "Negative" if avg_score <= 0.35 else "Neutral"
    
        st.write(f"**Overall Sentiment:** {overall_sentiment}")
        st.write(f"**Average Compound Score:** {avg_score:.2f}")
    else:
        st.write("No valid responses to analyze.")

    st.markdown("### Rationale:")
    st.markdown("""
    - **Positive:** Indicates an optimistic and positive outlook in responses.
    - **Neutral:** Indicates a balanced and non-extreme viewpoint in responses.
    - **Negative:** Indicates a pessimistic or critical viewpoint in responses.
    """)

def main():
    questions = ask_questions()
    responses = display_questions(questions)
    analyze_sentiment(responses)
    summarize_sentiment(responses)

if __name__ == "__main__":
    main()