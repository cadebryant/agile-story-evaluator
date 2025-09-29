#!/usr/bin/env python3
"""
Railway deployment version of Agile Story Evaluator
"""

import os
import time
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
    """Create the Gradio web interface with rate limiting"""
    evaluator = INVESTEvaluator()
    
    def evaluate_story(story_text):
        if not story_text.strip():
            return "Please enter a user story to evaluate.", "", ""
        
        # Check rate limiting
        if not evaluator.check_rate_limit():
            return "⚠️ Rate limit exceeded. Please wait before making more requests.", "", ""
        
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
        
        return feedback, ai_analysis, improved_story
    
    # Create Gradio interface
    with gr.Blocks(title="Agile Story Evaluator", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎯 Agile Story Evaluator")
        gr.Markdown("Evaluate your user stories against INVEST criteria and get AI-powered feedback for improvement.")
        
        # Add usage guidelines
        gr.Markdown("""
        ### 📋 Usage Guidelines
        - **Rate Limit**: 10 requests per minute, 100 per hour
        - **Purpose**: Professional Agile story evaluation only
        - **Respectful Use**: Please use responsibly and don't abuse the service
        """)
        
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

# For Railway deployment
if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=False
    )