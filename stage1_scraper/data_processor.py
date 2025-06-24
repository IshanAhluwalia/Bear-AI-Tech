"""
DATA PROCESSOR MODULE - anaylzing chat gpt responses and counting brand mentions
"""

import re
import json
from datetime import datetime
from prompts import get_target_brands


class BrandMentionProcessor:
    #processes text and counts brand mentions
    def __init__(self):
        self.target_brands = get_target_brands()  # Get brands from prompts module
        self.processed_data = []  # List to store all our results
        print(f"Created processor tracking: {', '.join(self.target_brands)}")
    
    def count_brand_mentions(self, text):
        """
        This function counts how many times each brand appears in text. 
        Returns: dict: {"Nike": 2, "Adidas": 1, ...}
        """
        print(f"\n🔍 Analyzing text: '{text[:50]}...'")
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        brand_counts = {}
        
        for brand in self.target_brands:
            pattern = r'\b' + re.escape(brand.lower()) + r'\b'
            matches = re.findall(pattern, text_lower)
            count = len(matches)
            
            brand_counts[brand] = count
            
            if count > 0:
                print(f"   ✅ Found '{brand}': {count} times")
        
        return brand_counts
    
    def process_response(self, prompt, response):
        print(f"\n📦 Processing response for prompt: '{prompt[:30]}...'")
        
        # Count the brand mentions
        brand_counts = self.count_brand_mentions(response)
        
        # Create a structured data package
        result = {
            "timestamp": datetime.now().isoformat(),  # When this happened
            "prompt": prompt,                         # What we asked
            "response": response,                     # What ChatGPT said
            "brand_mentions": brand_counts,           # Our analysis
            "total_mentions": sum(brand_counts.values())  # Quick summary
        }
        
        # Store it in our collection
        self.processed_data.append(result)
        
        print(f"   Total mentions in this response: {result['total_mentions']}")
        return result
    
    def get_summary(self):
        # Initialize totals
        total_counts = {brand: 0 for brand in self.target_brands}
        
        # Add up all the individual counts
        for data in self.processed_data:
            for brand, count in data["brand_mentions"].items():
                total_counts[brand] += count
        
        summary = {
            "total_responses_processed": len(self.processed_data),
            "overall_brand_totals": total_counts,
            "grand_total_mentions": sum(total_counts.values())
        }
        
        print(f"   📊 Processed {summary['total_responses_processed']} responses")
        print(f"   🎯 Found {summary['grand_total_mentions']} total brand mentions")
        
        return summary
    
    def get_comprehensive_analysis(self):
        """
        📊 COMPREHENSIVE ANALYSIS
        =======================
        Generate detailed aggregate statistics and analysis tables
        """
        if not self.processed_data:
            return {}
        
        # Basic summary
        total_counts = {brand: 0 for brand in self.target_brands}
        for data in self.processed_data:
            for brand, count in data["brand_mentions"].items():
                total_counts[brand] += count
        
        total_mentions = sum(total_counts.values())
        total_responses = len(self.processed_data)
        
        # Aggregate brand analysis
        brand_analysis = {}
        for brand in self.target_brands:
            brand_total = total_counts[brand]
            brand_counts = [resp['brand_mentions'][brand] for resp in self.processed_data]
            
            brand_analysis[brand] = {
                "total_mentions": brand_total,
                "percentage": (brand_total / total_mentions * 100) if total_mentions > 0 else 0,
                "avg_per_response": brand_total / total_responses,
                "max_in_single_response": max(brand_counts),
                "responses_with_mentions": sum(1 for count in brand_counts if count > 0),
                "response_coverage": (sum(1 for count in brand_counts if count > 0) / total_responses * 100)
            }
        
        # Response analysis
        response_analysis = []
        for i, resp in enumerate(self.processed_data, 1):
            response_analysis.append({
                "response_number": i,
                "prompt": resp['prompt'],
                "response_length": len(resp['response']),
                "total_mentions": resp['total_mentions'],
                "brand_breakdown": resp['brand_mentions'],
                "timestamp": resp['timestamp']
            })
        
        # Key insights
        max_mentions_response = max(self.processed_data, key=lambda x: x['total_mentions'])
        max_mentions_idx = self.processed_data.index(max_mentions_response) + 1
        
        dominant_brand = max(total_counts, key=total_counts.get)
        second_brand = sorted(total_counts.items(), key=lambda x: x[1], reverse=True)[1][0]
        
        response_totals = [r['total_mentions'] for r in self.processed_data]
        consistency = min(response_totals) / max(response_totals) * 100 if max(response_totals) > 0 else 0
        
        avg_response_length = sum(len(r['response']) for r in self.processed_data) / len(self.processed_data)
        
        insights = {
            "most_mentions_single_response": {
                "count": max_mentions_response['total_mentions'],
                "response_number": max_mentions_idx,
                "prompt": max_mentions_response['prompt']
            },
            "dominant_brand": {
                "name": dominant_brand,
                "mentions": total_counts[dominant_brand],
                "percentage": (total_counts[dominant_brand] / total_mentions * 100) if total_mentions > 0 else 0
            },
            "second_place_brand": {
                "name": second_brand,
                "mentions": total_counts[second_brand],
                "percentage": (total_counts[second_brand] / total_mentions * 100) if total_mentions > 0 else 0
            },
            "response_consistency": {
                "consistency_percentage": consistency,
                "min_mentions": min(response_totals),
                "max_mentions": max(response_totals),
                "range": max(response_totals) - min(response_totals)
            },
            "averages": {
                "response_length": avg_response_length,
                "mentions_per_response": total_mentions / total_responses
            }
        }
        
        # Market share analysis
        market_share = {
            "nike_jordan_combined": {
                "mentions": total_counts.get('Nike', 0) + total_counts.get('Jordan', 0),
                "percentage": ((total_counts.get('Nike', 0) + total_counts.get('Jordan', 0)) / total_mentions * 100) if total_mentions > 0 else 0
            },
            "traditional_big_three": {
                "brands": ["Nike", "Adidas", "New Balance"],
                "mentions": total_counts.get('Nike', 0) + total_counts.get('Adidas', 0) + total_counts.get('New Balance', 0),
                "percentage": ((total_counts.get('Nike', 0) + total_counts.get('Adidas', 0) + total_counts.get('New Balance', 0)) / total_mentions * 100) if total_mentions > 0 else 0
            }
        }
        
        return {
            "brand_analysis": brand_analysis,
            "response_analysis": response_analysis,
            "key_insights": insights,
            "market_share_analysis": market_share
        }

    def save_to_json(self, filename="brand_mentions.json"):
        """
        💾 SAVE OUR WORK WITH COMPREHENSIVE ANALYSIS
        ============================================
        Saves all processed data plus detailed aggregate analysis to JSON file.
        """
        print(f"\n💾 Saving comprehensive results to {filename}...")
        
        # Get basic summary
        summary = self.get_summary()
        
        # Get comprehensive analysis
        comprehensive_analysis = self.get_comprehensive_analysis()
        
        # Package everything together
        output = {
            "analysis_timestamp": datetime.now().isoformat(),
            "summary": summary,
            "comprehensive_analysis": comprehensive_analysis,
            "detailed_responses": self.processed_data
        }
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Saved {len(self.processed_data)} responses with comprehensive analysis to {filename}")
        print(f"   📊 Includes: Brand analysis, response analysis, key insights, and market share data")
        return filename
    
    def print_detailed_summary(self):
        """
        🖨️ PRETTY PRINT SUMMARY
        =======================
        Shows a nice formatted summary of our analysis.
        """
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("🎯 BRAND MENTION ANALYSIS RESULTS")
        print("="*60)
        print(f"📊 Total ChatGPT responses analyzed: {summary['total_responses_processed']}")
        print(f"🎯 Total brand mentions found: {summary['grand_total_mentions']}")
        print("\n🏷️ Brand breakdown:")
        
        # Sort brands by mention count (most mentioned first)
        sorted_brands = sorted(
            summary['overall_brand_totals'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for brand, count in sorted_brands:
            percentage = (count / summary['grand_total_mentions'] * 100) if summary['grand_total_mentions'] > 0 else 0
            print(f"   🔸 {brand}: {count} mentions ({percentage:.1f}%)")
        
        print("="*60)


# 🧪 TEST THE PROCESSOR
def test_processor():
    """
    🧪 TEST FUNCTION
    ================
    Let's test our processor with some sample text!
    """
    print("🧪 TESTING THE BRAND MENTION PROCESSOR")
    print("="*50)
    
    # Create a processor
    processor = BrandMentionProcessor()
    
    # Test with sample data
    sample_prompt = "What are the best running shoes?"
    sample_response = "I recommend Nike Air Max for comfort and Adidas Ultraboost for performance. Hoka offers great cushioning too!"
    
    # Process the sample
    result = processor.process_response(sample_prompt, sample_response)
    
    # Show detailed summary
    processor.print_detailed_summary()
    
    # Save the results to JSON file
    filename = processor.save_to_json("test_output.json")
    print(f"\n📁 Output saved to: {filename}")
    
    return processor


if __name__ == "__main__":
    # Run the test when this file is executed directly
    test_processor() 