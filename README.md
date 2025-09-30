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
short_description: Story evaluator
---

# 🎯 Agile Story Evaluator

A powerful AI application that evaluates Agile user stories against the INVEST criteria and provides constructive feedback for improvement.

## 🚀 Live Application

**Try it now:** [https://agile-story-evaluator-production.up.railway.app/](https://agile-story-evaluator-production.up.railway.app/)

## ✨ Features

- **INVEST Criteria Evaluation**: Analyzes stories for Independence, Negotiability, Value, Estimability, Size, and Testability
- **AI-Powered Analysis**: Uses OpenAI GPT for detailed critique and suggestions
- **Story Improvement**: Generates improved versions of user stories
- **Interactive Interface**: Clean, user-friendly Gradio interface
- **Real-time Feedback**: Instant evaluation as you type
- **CAPTCHA Protection**: Prevents automated abuse
- **Rate Limiting**: Ensures fair usage

## 🎯 How to Use

1. **Enter your user story** in the text box
2. **Solve the math CAPTCHA** to verify you're human
3. **Click "Evaluate Story"** to get instant analysis
4. **Review the INVEST scores** and detailed feedback
5. **Get AI analysis** for comprehensive insights
6. **See improved story suggestions** for better scope and clarity

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

## 🛡️ Security Features

- **CAPTCHA Protection**: Math-based verification to prevent bot abuse
- **Rate Limiting**: 10 requests per minute, 100 per hour per user
- **Input Validation**: Comprehensive story structure analysis
- **Secure Deployment**: Railway platform with environment variable protection

## 📄 License

This project is open source and available under the MIT License.