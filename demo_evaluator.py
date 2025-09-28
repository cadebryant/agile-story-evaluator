#!/usr/bin/env python3
"""
Standalone INVEST evaluator for demo purposes - no API key required
"""

import re
from typing import Dict, List, Tuple

class DemoINVESTEvaluator:
    """
    Evaluates user stories against INVEST criteria without requiring API keys
    """
    
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

def demo_invest_evaluation():
    """Demonstrate the INVEST evaluation without API calls"""
    evaluator = DemoINVESTEvaluator()
    
    # Test stories with varying quality
    test_stories = [
        {
            "title": "Good User Story",
            "story": "As a customer, I want to view my order history so that I can track my purchases"
        },
        {
            "title": "Poor User Story",
            "story": "Add login feature"
        },
        {
            "title": "Complex Story",
            "story": "As a product manager, I want to see comprehensive analytics dashboard with real-time data visualization, user behavior tracking, conversion metrics, A/B testing results, and automated reporting so that I can make data-driven decisions and optimize our product strategy"
        },
        {
            "title": "Story with Acceptance Criteria",
            "story": "As a user, I want to reset my password so that I can regain access to my account. Given I am on the login page, when I click 'Forgot Password', then I should receive an email with reset instructions."
        }
    ]
    
    print("Agile Story Evaluator - Demo")
    print("=" * 60)
    print("This demo shows INVEST criteria evaluation without AI analysis.")
    print("For full AI-powered feedback, add your OpenAI API key to .env file")
    print("=" * 60)
    
    for i, test_case in enumerate(test_stories, 1):
        print(f"\n{i}. {test_case['title']}")
        print("-" * 40)
        print(f"Story: '{test_case['story']}'")
        print()
        
        # Get INVEST evaluation
        criteria = evaluator.evaluate_invest_criteria(test_case['story'])
        
        # Display results
        total_score = 0
        for criterion, data in criteria.items():
            score = data['score']
            total_score += score
            max_score = 3
            
            # Create visual score
            score_bars = "X" * score + "-" * (max_score - score)
            
            print(f"{criterion:12} {score_bars} ({score}/{max_score})")
            print(f"             {data['feedback']}")
            
            if data['suggestions']:
                for suggestion in data['suggestions']:
                    print(f"             -> {suggestion}")
            print()
        
        # Calculate overall score
        overall_score = (total_score / (len(criteria) * 3)) * 100
        score_indicator = "EXCELLENT" if overall_score >= 80 else "GOOD" if overall_score >= 60 else "NEEDS WORK"
        
        print(f"Overall Score: {score_indicator} ({overall_score:.1f}%)")
        print("=" * 60)
    
    print("\nDemo completed! To run the full application with AI analysis:")
    print("1. Get an OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Create a .env file with: OPENAI_API_KEY=your_key_here")
    print("3. Run: python agile_story_evaluator.py")

if __name__ == "__main__":
    demo_invest_evaluation()
