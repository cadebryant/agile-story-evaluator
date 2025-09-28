---
title: Agile Story Evaluator
emoji: 🎯
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
short_description: Evaluate user stories against INVEST criteria with AI feedback
---

# 🎯 Agile Story Evaluator

A powerful AI application that evaluates Agile user stories against the INVEST criteria and provides constructive feedback for improvement.

## ✨ Features

- **INVEST Criteria Evaluation**: Analyzes stories for Independence, Negotiability, Value, Estimability, Size, and Testability
- **AI-Powered Analysis**: Uses OpenAI GPT for detailed critique and suggestions
- **Story Improvement**: Generates improved versions of user stories
- **Interactive Interface**: Clean, user-friendly Gradio interface
- **Real-time Feedback**: Instant evaluation as you type

## 🚀 How to Use

1. **Enter your user story** in the text box
2. **Click "Evaluate Story"** or let it auto-evaluate
3. **Review the INVEST scores** and feedback
4. **Get AI analysis** for detailed insights
5. **See improved story suggestions**

## 📋 Sample Stories to Try

- "As a customer, I want to view my order history so that I can track my purchases"
- "As a user, I want a login feature"
- "As a product manager, I want to see analytics so that I can make data-driven decisions"

## 🔧 INVEST Criteria

The application evaluates stories against these criteria:

- **Independent**: Can be developed without dependencies on other stories
- **Negotiable**: Details can be discussed and refined
- **Valuable**: Provides clear value to users or stakeholders
- **Estimable**: Has sufficient detail for effort estimation
- **Small**: Appropriately sized (not too large or too small)
- **Testable**: Can be verified through testing

## 🛠️ Setup for Development

```bash
# Clone the repository
git clone https://github.com/cadebryant/agile-story-evaluator.git
cd agile-story-evaluator

# Install dependencies
pip install -r requirements.txt

# Set up OpenAI API key (optional for AI features)
# Create .env file with: OPENAI_API_KEY=your_key_here

# Run locally
python app.py
```

## 📄 License

This project is open source and available under the MIT License.