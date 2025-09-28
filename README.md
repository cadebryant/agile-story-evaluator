# Agile Story Evaluator

A Python/Gradio AI application that evaluates Agile user stories against the INVEST criteria and provides constructive feedback for improvement.

## Features

- **INVEST Criteria Evaluation**: Analyzes stories for Independence, Negotiability, Value, Estimability, Size, and Testability
- **AI-Powered Analysis**: Uses OpenAI GPT to provide detailed critique and suggestions
- **Story Improvement**: Generates improved versions of user stories
- **Interactive Web Interface**: Clean, user-friendly Gradio interface
- **Real-time Feedback**: Instant evaluation as you type

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Copy `env_example.txt` to `.env`
   - Add your OpenAI API key to the `.env` file
   - Get your API key from: https://platform.openai.com/api-keys

## Usage

### Quick Start
```bash
python run_app.py
```

### Alternative Methods
```bash
# Run main application directly
python agile_story_evaluator.py

# Run demo without API key
python demo_evaluator.py
```

The application will start a web server (usually at http://localhost:7860). Open this URL in your browser to use the interface.

### Demo Mode
If you don't have an OpenAI API key, you can still see the core INVEST evaluation functionality:
```bash
python demo_evaluator.py
```

## INVEST Criteria

The application evaluates stories against these criteria:

- **Independent**: Can be developed without dependencies on other stories
- **Negotiable**: Details can be discussed and refined
- **Valuable**: Provides clear value to users or stakeholders
- **Estimable**: Has sufficient detail for effort estimation
- **Small**: Appropriately sized (not too large or too small)
- **Testable**: Can be verified through testing

## Sample Stories

Try these examples to see the evaluator in action:

- "As a customer, I want to view my order history so that I can track my purchases"
- "As a user, I want a login feature"
- "As a product manager, I want to see analytics so that I can make data-driven decisions"

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection (for AI analysis)

## License

This project is open source and available under the MIT License.
