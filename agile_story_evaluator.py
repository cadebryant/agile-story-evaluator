import gradio as gr
import openai
import os
from dotenv import load_dotenv
import re
from typing import Dict, List, Tuple

# Load environment variables
load_dotenv()

class INVESTEvaluator:
    """
    Evaluates user stories against INVEST criteria:
    - Independent: Can be developed independently
    - Negotiable: Details can be negotiated
    - Valuable: Provides value to users/stakeholders
    - Estimable: Can be estimated for effort
    - Small: Appropriately sized
    - Testable: Can be tested/verified
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def analyze_story_structure(self, story: str) -> Dict[str, any]:
        """Analyze the basic structure of the user story"""
        analysis = {
            'has_persona': False,
            'has_action': False,
            'has_value': False,
            'has_acceptance_criteria': False,
            'word_count': len(story.split()),
            'sentence_count': len(re.split(r'[.!?]+', story)),
            'has_user_story_format': False
        }
        
        # Check for user story format: "As a [persona], I want [action] so that [value]"
        user_story_pattern = r'as\s+a\s+\w+.*?i\s+want\s+.*?so\s+that\s+.*'
        if re.search(user_story_pattern, story.lower()):
            analysis['has_user_story_format'] = True
            
        # Check for persona
        persona_patterns = [r'as\s+a\s+(\w+)', r'as\s+an\s+(\w+)', r'as\s+the\s+(\w+)']
        for pattern in persona_patterns:
            if re.search(pattern, story.lower()):
                analysis['has_persona'] = True
                break
                
        # Check for action (want/need)
        action_patterns = [r'i\s+want\s+', r'i\s+need\s+', r'i\s+can\s+', r'i\s+should\s+']
        for pattern in action_patterns:
            if re.search(pattern, story.lower()):
                analysis['has_action'] = True
                break
                
        # Check for value proposition
        value_patterns = [r'so\s+that\s+', r'in\s+order\s+to\s+', r'to\s+']
        for pattern in value_patterns:
            if re.search(pattern, story.lower()):
                analysis['has_value'] = True
                break
                
        # Check for acceptance criteria
        criteria_patterns = [r'given\s+', r'when\s+', r'then\s+', r'acceptance\s+criteria', r'criteria:']
        for pattern in criteria_patterns:
            if re.search(pattern, story.lower()):
                analysis['has_acceptance_criteria'] = True
                break
                
        return analysis
    
    def evaluate_invest_criteria(self, story: str) -> Dict[str, Dict]:
        """Evaluate the story against each INVEST criterion"""
        structure = self.analyze_story_structure(story)
        
        criteria = {
            'Independent': {
                'score': 0,
                'feedback': '',
                'suggestions': []
            },
            'Negotiable': {
                'score': 0,
                'feedback': '',
                'suggestions': []
            },
            'Valuable': {
                'score': 0,
                'feedback': '',
                'suggestions': []
            },
            'Estimable': {
                'score': 0,
                'feedback': '',
                'suggestions': []
            },
            'Small': {
                'score': 0,
                'feedback': '',
                'suggestions': []
            },
            'Testable': {
                'score': 0,
                'feedback': '',
                'suggestions': []
            }
        }
        
        # Independent: Check if story can stand alone
        if structure['has_user_story_format'] and not any(word in story.lower() for word in ['depends on', 'requires', 'after', 'before']):
            criteria['Independent']['score'] = 3
            criteria['Independent']['feedback'] = "Story appears to be independent"
        elif structure['has_user_story_format']:
            criteria['Independent']['score'] = 2
            criteria['Independent']['feedback'] = "Story has dependencies mentioned"
            criteria['Independent']['suggestions'].append("Consider breaking down dependencies into separate stories")
        else:
            criteria['Independent']['score'] = 1
            criteria['Independent']['feedback'] = "Story structure unclear for independence assessment"
            criteria['Independent']['suggestions'].append("Use standard user story format: 'As a [persona], I want [action] so that [value]'")
        
        # Negotiable: Check for flexibility
        rigid_terms = ['must', 'shall', 'will', 'exactly', 'precisely', 'specifically']
        if any(term in story.lower() for term in rigid_terms):
            criteria['Negotiable']['score'] = 1
            criteria['Negotiable']['feedback'] = "Story contains rigid language that limits negotiation"
            criteria['Negotiable']['suggestions'].append("Use more flexible language like 'should' or 'could'")
        elif structure['has_user_story_format']:
            criteria['Negotiable']['score'] = 3
            criteria['Negotiable']['feedback'] = "Story uses negotiable language"
        else:
            criteria['Negotiable']['score'] = 2
            criteria['Negotiable']['feedback'] = "Story format could be more negotiable"
            criteria['Negotiable']['suggestions'].append("Use user story format for better negotiation")
        
        # Valuable: Check for clear value proposition
        if structure['has_value'] and structure['has_persona']:
            criteria['Valuable']['score'] = 3
            criteria['Valuable']['feedback'] = "Story clearly states value to user"
        elif structure['has_value']:
            criteria['Valuable']['score'] = 2
            criteria['Valuable']['feedback'] = "Value stated but persona unclear"
            criteria['Valuable']['suggestions'].append("Specify who benefits from this story")
        else:
            criteria['Valuable']['score'] = 1
            criteria['Valuable']['feedback'] = "Value proposition unclear"
            criteria['Valuable']['suggestions'].append("Add 'so that [benefit]' to explain the value")
        
        # Estimable: Check for sufficient detail
        if structure['word_count'] > 20 and structure['has_acceptance_criteria']:
            criteria['Estimable']['score'] = 3
            criteria['Estimable']['feedback'] = "Story has sufficient detail for estimation"
        elif structure['word_count'] > 10:
            criteria['Estimable']['score'] = 2
            criteria['Estimable']['feedback'] = "Story has basic detail but could use acceptance criteria"
            criteria['Estimable']['suggestions'].append("Add acceptance criteria to improve estimability")
        else:
            criteria['Estimable']['score'] = 1
            criteria['Estimable']['feedback'] = "Story lacks detail for estimation"
            criteria['Estimable']['suggestions'].append("Add more detail and acceptance criteria")
        
        # Small: Check story size
        if 10 <= structure['word_count'] <= 50:
            criteria['Small']['score'] = 3
            criteria['Small']['feedback'] = "Story is appropriately sized"
        elif structure['word_count'] < 10:
            criteria['Small']['score'] = 1
            criteria['Small']['feedback'] = "Story is too small/vague"
            criteria['Small']['suggestions'].append("Add more detail to make the story meaningful")
        else:
            criteria['Small']['score'] = 2
            criteria['Small']['feedback'] = "Story might be too large"
            criteria['Small']['suggestions'].append("Consider breaking into smaller stories")
        
        # Testable: Check for testability
        if structure['has_acceptance_criteria'] and structure['has_action']:
            criteria['Testable']['score'] = 3
            criteria['Testable']['feedback'] = "Story has clear acceptance criteria"
        elif structure['has_action']:
            criteria['Testable']['score'] = 2
            criteria['Testable']['feedback'] = "Action clear but acceptance criteria missing"
            criteria['Testable']['suggestions'].append("Add Given/When/Then acceptance criteria")
        else:
            criteria['Testable']['score'] = 1
            criteria['Testable']['feedback'] = "Story lacks testable elements"
            criteria['Testable']['suggestions'].append("Add clear actions and acceptance criteria")
        
        return criteria
    
    def get_ai_analysis(self, story: str) -> str:
        """Get AI-powered analysis of the user story"""
        try:
            prompt = f"""
            Analyze this user story for Agile development:
            
            "{story}"
            
            Provide a comprehensive critique focusing on:
            1. Story structure and clarity
            2. INVEST criteria compliance
            3. Specific improvement suggestions
            4. Potential scope issues
            
            Be constructive and specific in your feedback.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an Agile coach and user story expert. Provide detailed, constructive feedback on user stories."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}. Please check your OpenAI API key."
    
    def generate_improved_story(self, story: str) -> str:
        """Generate an improved version of the user story"""
        try:
            prompt = f"""
            Improve this user story to better comply with INVEST criteria:
            
            Original: "{story}"
            
            Provide an improved version that:
            1. Uses proper user story format
            2. Is independent, negotiable, valuable, estimable, small, and testable
            3. Includes acceptance criteria
            4. Has clear scope and value proposition
            
            Format your response as:
            IMPROVED STORY:
            [improved story]
            
            ACCEPTANCE CRITERIA:
            [criteria]
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an Agile coach. Improve user stories to meet INVEST criteria."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Story improvement unavailable: {str(e)}. Please check your OpenAI API key."

def create_gradio_interface():
    """Create the Gradio web interface"""
    evaluator = INVESTEvaluator()
    
    def evaluate_story(story_text):
        if not story_text.strip():
            return "Please enter a user story to evaluate.", "", ""
        
        # Get INVEST evaluation
        criteria = evaluator.evaluate_invest_criteria(story_text)
        
        # Create detailed feedback
        feedback_parts = []
        total_score = 0
        
        for criterion, data in criteria.items():
            score = data['score']
            total_score += score
            max_score = 3
            
            # Create score visualization
            score_bars = "█" * score + "░" * (max_score - score)
            
            feedback_parts.append(f"**{criterion}**: {score_bars} ({score}/{max_score})")
            feedback_parts.append(f"*{data['feedback']}*")
            
            if data['suggestions']:
                feedback_parts.append("💡 Suggestions:")
                for suggestion in data['suggestions']:
                    feedback_parts.append(f"   • {suggestion}")
            feedback_parts.append("")
        
        # Calculate overall score
        overall_score = (total_score / (len(criteria) * 3)) * 100
        score_emoji = "🟢" if overall_score >= 80 else "🟡" if overall_score >= 60 else "🔴"
        
        feedback = f"{score_emoji} **Overall INVEST Score: {overall_score:.1f}%**\n\n" + "\n".join(feedback_parts)
        
        # Get AI analysis
        ai_analysis = evaluator.get_ai_analysis(story_text)
        
        # Get improved story
        improved_story = evaluator.generate_improved_story(story_text)
        
        return feedback, ai_analysis, improved_story
    
    # Create Gradio interface
    with gr.Blocks(title="Agile Story Evaluator", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎯 Agile Story Evaluator")
        gr.Markdown("Evaluate your user stories against INVEST criteria and get AI-powered feedback for improvement.")
        
        with gr.Row():
            with gr.Column(scale=2):
                story_input = gr.Textbox(
                    label="Enter your user story",
                    placeholder="As a [persona], I want [action] so that [value]",
                    lines=4,
                    max_lines=8
                )
                
                evaluate_btn = gr.Button("Evaluate Story", variant="primary", size="lg")
                
                gr.Markdown("### 📋 Sample Stories to Try:")
                gr.Markdown("""
                - As a customer, I want to view my order history so that I can track my purchases
                - As a user, I want a login feature
                - As a product manager, I want to see analytics so that I can make data-driven decisions
                """)
            
            with gr.Column(scale=3):
                invest_feedback = gr.Markdown(label="INVEST Evaluation")
        
        with gr.Row():
            with gr.Column():
                ai_analysis = gr.Markdown(label="🤖 AI Analysis")
            
            with gr.Column():
                improved_story = gr.Markdown(label="✨ Improved Story")
        
        # Event handlers
        evaluate_btn.click(
            fn=evaluate_story,
            inputs=[story_input],
            outputs=[invest_feedback, ai_analysis, improved_story]
        )
        
        # Auto-evaluate on text change (with debouncing)
        story_input.change(
            fn=evaluate_story,
            inputs=[story_input],
            outputs=[invest_feedback, ai_analysis, improved_story]
        )
    
    return interface

if __name__ == "__main__":
    # Create and launch the interface
    interface = create_gradio_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
