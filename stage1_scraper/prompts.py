"""
🎯 PROMPTS MODULE
================

This file contains all the questions we'll ask ChatGPT.

💡 WHY SEPARATE THIS?
- Easy to modify questions without touching other code
- Clear separation of data and logic
- Makes testing different prompts simple

🧠 CONCEPT: We want questions that will naturally mention our target brands
"""

# The brands we want to track mentions for
TARGET_BRANDS = [
    "Nike",
    "Adidas", 
    "Hoka",
    "New Balance",
    "Jordan"
]

# Questions designed to get ChatGPT to mention athletic shoe brands
SPORTSWEAR_PROMPTS = [
    "What are the best running shoes in 2025?",
    "Top performance sneakers for athletes",
    "Which basketball shoes provide the best ankle support?",
    "Recommend comfortable athletic shoes for marathon training",
    "What are the most popular sneaker brands among professional athletes?",
    "Best shoes for cross-training and gym workouts",
    "Which athletic footwear brands offer the best value for money?",
    "Most innovative running shoe technologies available today",
    "What shoes do NBA players prefer for performance?",
    "Best athletic shoes for people with wide feet"
]

def get_prompts():
    """
    🔄 GETTER FUNCTION
    Returns the list of prompts for the scraper to use.
    
    💡 WHY A FUNCTION? 
    - Could add logic later (random selection, filtering, etc.)
    - Consistent interface for other modules
    """
    return SPORTSWEAR_PROMPTS

def get_target_brands():
    """
    🔄 GETTER FUNCTION  
    Returns the brands we're tracking.
    """
    return TARGET_BRANDS


# 🧪 TEST THE MODULE
if __name__ == "__main__":
    print("📋 Testing prompts module...")
    print(f"📊 Number of prompts: {len(get_prompts())}")
    print(f"🏷️  Target brands: {', '.join(get_target_brands())}")
    print("\n🎯 Sample prompts:")
    for i, prompt in enumerate(get_prompts()[:3], 1):
        print(f"   {i}. {prompt}") 