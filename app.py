#!/usr/bin/env python3
"""
Railway deployment version of Agile Story Evaluator
"""

import os
import time
import random
import gradio as gr
from collections import defaultdict
from agile_story_evaluator import INVESTEvaluator as BaseINVESTEvaluator, create_gradio_interface as base_create_gradio_interface

class INVESTEvaluator(BaseINVESTEvaluator):
    """Railway deployment version with rate limiting"""
    
    def __init__(self):
        super().__init__()
        
        # Rate limiting
        self.usage_tracker = defaultdict(list)
        self.max_requests_per_minute = 10
        self.max_requests_per_hour = 100
    
    def check_rate_limit(self, user_id: str = "anonymous") -> bool:
        """Check if user has exceeded rate limits"""
        current_time = time.time()
        
        # Clean old entries
        self.usage_tracker[user_id] = [
            timestamp for timestamp in self.usage_tracker[user_id]
            if current_time - timestamp < 3600  # Keep last hour
        ]
        
        # Check limits
        recent_requests = [
            timestamp for timestamp in self.usage_tracker[user_id]
            if current_time - timestamp < 60  # Last minute
        ]
        
        if len(recent_requests) >= self.max_requests_per_minute:
            return False
        
        if len(self.usage_tracker[user_id]) >= self.max_requests_per_hour:
            return False
        
        # Record this request
        self.usage_tracker[user_id].append(current_time)
        return True

def create_gradio_interface():
    """Create the Gradio web interface with rate limiting and CAPTCHA"""
    evaluator = INVESTEvaluator()
    
    def generate_captcha():
        """Generate a simple math CAPTCHA"""
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(['+', '-', '*'])
        
        if operation == '+':
            answer = num1 + num2
            question = f"{num1} + {num2} = ?"
        elif operation == '-':
            # Ensure positive result
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
            question = f"{num1} - {num2} = ?"
        else:  # multiplication
            answer = num1 * num2
            question = f"{num1} × {num2} = ?"
        
        return question, answer  # Return both question and answer
    
    def verify_captcha(user_answer, correct_answer):
        """Verify CAPTCHA answer"""
        try:
            user_int = int(str(user_answer).strip())
            return user_int == correct_answer
        except (ValueError, TypeError):
            return False
    
    def evaluate_story(story_text, captcha_answer, captcha_state):
        if not story_text.strip():
            new_question, new_answer = generate_captcha()
            new_state = {"question": new_question, "answer": new_answer}
            return "Please enter a user story to evaluate.", "", "", new_question, new_state
        
        # Verify CAPTCHA first - use the correct answer from state
        if not verify_captcha(captcha_answer, captcha_state["answer"]):
            new_question, new_answer = generate_captcha()
            new_state = {"question": new_question, "answer": new_answer}
            return "❌ CAPTCHA verification failed. Please solve the math problem correctly.", "", "", new_question, new_state
        
        # Check rate limiting
        if not evaluator.check_rate_limit():
            new_question, new_answer = generate_captcha()
            new_state = {"question": new_question, "answer": new_answer}
            return "⚠️ Rate limit exceeded. Please wait before making more requests.", "", "", new_question, new_state
        
        # Use the base evaluation logic
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
        
        # Generate new CAPTCHA for next evaluation
        new_question, new_answer = generate_captcha()
        captcha_state["question"] = new_question
        captcha_state["answer"] = new_answer
        
        return feedback, ai_analysis, improved_story, new_question, captcha_state
    
    # Create Gradio interface with modern theme
    with gr.Blocks(
        title="Agile Story Evaluator", 
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="gray",
            neutral_hue="slate"
        ),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        }
        .feature-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            margin: 1rem 0;
            border: 1px solid rgba(102, 126, 234, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        .captcha-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
            padding: 1.5rem;
            border: 2px solid #dee2e6;
            margin: 1rem 0;
        }
        .evaluate-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
        }
        .evaluate-btn:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        }
        .results-section, .ai-section, .improved-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            border-left: 4px solid #667eea;
            min-height: 200px;
        }
        .gradio-textbox {
            border-radius: 8px !important;
            border: 2px solid #e9ecef !important;
            transition: border-color 0.3s ease !important;
        }
        .gradio-textbox:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        """
    ) as interface:
        
        # Modern header
        gr.HTML("""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">🎯 Agile Story Evaluator</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                Professional INVEST criteria analysis with AI-powered insights
            </p>
        </div>
        """)
        
        # Feature highlights
        gr.HTML("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
            <div class="feature-card">
                <h3 style="color: #667eea; margin-top: 0;">📊 INVEST Analysis</h3>
                <p>Comprehensive evaluation against all 6 INVEST criteria with detailed scoring</p>
            </div>
            <div class="feature-card">
                <h3 style="color: #667eea; margin-top: 0;">🤖 AI Insights</h3>
                <p>Advanced AI analysis powered by OpenAI GPT for professional feedback</p>
            </div>
            <div class="feature-card">
                <h3 style="color: #667eea; margin-top: 0;">✨ Story Improvement</h3>
                <p>Get enhanced versions of your stories with better scope and clarity</p>
            </div>
        </div>
        """)
        
        # Initialize CAPTCHA state - this will be unique per user session
        initial_question, initial_answer = generate_captcha()
        captcha_state = gr.State({"question": initial_question, "answer": initial_answer})
        
        with gr.Row():
            with gr.Column(scale=2):
                # Input section with modern styling
                gr.HTML("""
                <div class="feature-card">
                    <h3 style="color: #667eea; margin-top: 0; margin-bottom: 1rem;">📝 Story Input</h3>
                """)
                
                story_input = gr.Textbox(
                    label="Enter your user story",
                    placeholder="As a [persona], I want [action] so that [value]",
                    lines=4,
                    max_lines=8,
                    info="Use the standard user story format for best results"
                )
                
                # Enhanced CAPTCHA section
                gr.HTML("""
                <div class="captcha-section">
                    <h4 style="margin-top: 0; color: #495057;">🔒 Security Verification</h4>
                """)
                
                with gr.Row():
                    captcha_question = gr.Textbox(
                        label="Math Problem",
                        value=initial_question,
                        interactive=False,
                        scale=2,
                        info="Solve this math problem to verify you're human"
                    )
                    captcha_answer = gr.Textbox(
                        label="Your Answer",
                        placeholder="Enter the answer",
                        scale=1,
                        info="Type the numerical answer"
                    )
                
                gr.HTML("</div>")  # Close captcha section
                
                evaluate_btn = gr.Button(
                    "🚀 Evaluate Story", 
                    variant="primary", 
                    size="lg",
                    elem_classes="evaluate-btn"
                )
                
                gr.HTML("</div>")  # Close input card
                
                # Sample stories with better styling
                gr.HTML("""
                <div class="feature-card">
                    <h3 style="color: #667eea; margin-top: 0;">💡 Sample Stories to Try</h3>
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; border-left: 4px solid #667eea;">
                        <p style="margin: 0.5rem 0;"><strong>Good Example:</strong> "As a customer, I want to view my order history so that I can track my purchases"</p>
                        <p style="margin: 0.5rem 0;"><strong>Needs Work:</strong> "As a user, I want a login feature"</p>
                        <p style="margin: 0.5rem 0;"><strong>Complex:</strong> "As a product manager, I want to see analytics so that I can make data-driven decisions"</p>
                    </div>
                </div>
                """)
            
            with gr.Column(scale=3):
                # Results section with modern styling
                gr.HTML("""
                <div class="feature-card">
                    <h3 style="color: #667eea; margin-top: 0; margin-bottom: 1rem;">📊 INVEST Evaluation Results</h3>
                """)
                
                invest_feedback = gr.Markdown(
                    label="",
                    value="**Ready to evaluate your story!** Enter a user story above and click 'Evaluate Story' to see detailed INVEST criteria analysis.",
                    elem_classes="results-section"
                )
                
                gr.HTML("</div>")  # Close results card
        
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="feature-card">
                    <h3 style="color: #667eea; margin-top: 0; margin-bottom: 1rem;">🤖 AI Analysis</h3>
                """)
                
                ai_analysis = gr.Markdown(
                    label="",
                    value="*AI analysis will appear here after evaluation...*",
                    elem_classes="ai-section"
                )
                
                gr.HTML("</div>")
            
            with gr.Column():
                gr.HTML("""
                <div class="feature-card">
                    <h3 style="color: #667eea; margin-top: 0; margin-bottom: 1rem;">✨ Improved Story</h3>
                """)
                
                improved_story = gr.Markdown(
                    label="",
                    value="*Enhanced story suggestions will appear here after evaluation...*",
                    elem_classes="improved-section"
                )
                
                gr.HTML("</div>")
        
        # Event handlers
        evaluate_btn.click(
            fn=evaluate_story,
            inputs=[story_input, captcha_answer, captcha_state],
            outputs=[invest_feedback, ai_analysis, improved_story, captcha_question, captcha_state]
        )
        
        # Auto-evaluate on text change (with debouncing) - disabled to require CAPTCHA
        # story_input.change(
        #     fn=evaluate_story,
        #     inputs=[story_input, captcha_answer],
        #     outputs=[invest_feedback, ai_analysis, improved_story, captcha_question]
        # )
        
        # Modern footer with guidelines
        gr.HTML("""
        <div style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: center;">
                <div>
                    <h4 style="color: #667eea; margin-bottom: 0.5rem;">⚡ Rate Limits</h4>
                    <p style="margin: 0; color: #6c757d;">10 requests/minute<br>100 requests/hour</p>
                </div>
                <div>
                    <h4 style="color: #667eea; margin-bottom: 0.5rem;">🎯 Purpose</h4>
                    <p style="margin: 0; color: #6c757d;">Professional Agile<br>story evaluation</p>
                </div>
                <div>
                    <h4 style="color: #667eea; margin-bottom: 0.5rem;">🤝 Respectful Use</h4>
                    <p style="margin: 0; color: #6c757d;">Please use responsibly<br>and don't abuse</p>
                </div>
            </div>
        </div>
        """)
    
    return interface

# For Railway deployment
if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=False
    )