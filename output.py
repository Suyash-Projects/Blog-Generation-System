import os
from datetime import datetime

class OutputManager:
    @staticmethod
    def display_blog(blog_content: str, topic: str):
        """Display blog content to console"""
        print("\n" + "="*80)
        print(f"📝 GENERATED BLOG: {topic.upper()}")
        print("="*80)
        print(blog_content)
        print("="*80)
    
    @staticmethod
    def save_to_markdown(blog_content: str, topic: str, filename: str = None):
        """Save blog content to markdown file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"blog_{safe_topic.replace(' ', '_')}_{timestamp}.md"
        
        # Create blogs directory if it doesn't exist
        os.makedirs("blogs", exist_ok=True)
        filepath = os.path.join("blogs", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Blog: {topic}\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(blog_content)
        
        print(f"💾 Blog saved to: {filepath}")
        return filepath
    
    @staticmethod
    def save_to_text(blog_content: str, topic: str, filename: str = None):
        """Save blog content to text file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"blog_{safe_topic.replace(' ', '_')}_{timestamp}.txt"
        
        # Create blogs directory if it doesn't exist
        os.makedirs("blogs", exist_ok=True)
        filepath = os.path.join("blogs", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Blog: {topic}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n\n")
            f.write(blog_content)
        
        print(f"💾 Blog saved to: {filepath}")
        return filepath