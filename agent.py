import os
import logging
import time
from dotenv import load_dotenv
import requests
from memory import ShortTermMemory

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BlogAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError("Missing OpenRouter API key. Add it in .env file as OPENROUTER_API_KEY=<key>")
        
        if len(self.api_key) < 20:
            raise ValueError("Invalid OpenRouter API key format")
        
        self.use_openrouter = True
        logging.info("BlogAgent initialized with valid API key")
        self.memory = ShortTermMemory()
    
    def research_topic(self, topic: str):
        """Research the topic using available tools with enhanced error handling"""
        # Fix common spelling mistakes
        if "Fianance" in topic:
            topic = topic.replace("Fianance", "Finance")
            
        logging.info(f"Researching topic: {topic}")
        
        try:
            from tools import ResearchTools
            
            # Try Wikipedia first with error handling
            try:
                wiki_result = ResearchTools.wikipedia_search(topic)
                if wiki_result and not wiki_result.startswith("Wikipedia search failed"):
                    self.memory.add_research("Wikipedia", wiki_result)
                else:
                    self.memory.add_research("Wikipedia", f"Wikipedia search failed for: {topic}")
            except Exception as e:
                logging.error(f"Wikipedia search error: {str(e)}")
                self.memory.add_research("Wikipedia", f"Wikipedia search failed for: {topic}")
            
            time.sleep(1)  # Rate limiting
            
            # Try web search with error handling
            try:
                web_result = ResearchTools.web_search(f"{topic} latest news 2024 2025")
                if web_result and not web_result.startswith("All search engines failed"):
                    self.memory.add_research("Latest News", web_result)
                else:
                    self.memory.add_research("Latest News", f"Web search failed for: {topic}")
            except Exception as e:
                logging.error(f"Web search error: {str(e)}")
                self.memory.add_research("Latest News", f"Web search failed for: {topic}")
            
            time.sleep(1)
            
            # Try another web search with error handling
            try:
                schemes_result = ResearchTools.web_search(f"{topic} government schemes policies 2024 , 2025")
                if schemes_result and not schemes_result.startswith("All search engines failed"):
                    self.memory.add_research("Government Schemes", schemes_result)
                else:
                    self.memory.add_research("Government Schemes", f"Web search failed for: {topic}")
            except Exception as e:
                logging.error(f"Government schemes search error: {str(e)}")
                self.memory.add_research("Government Schemes", f"Web search failed for: {topic}")
            
            time.sleep(1)
            
            # Try trends search with error handling
            try:
                trends_result = ResearchTools.web_search(f"{topic} current trends developments 2025")
                if trends_result and not trends_result.startswith("All search engines failed"):
                    self.memory.add_research("Current Trends", trends_result)
                else:
                    self.memory.add_research("Current Trends", f"Web search failed for: {topic}")
            except Exception as e:
                logging.error(f"Trends search error: {str(e)}")
                self.memory.add_research("Current Trends", f"Web search failed for: {topic}")
            
            logging.info("Research completed successfully")
        except Exception as e:
            logging.error(f"Research failed: {str(e)}")
            self.memory.add_research("Error", f"Could not complete research for {topic}")
    
    def generate_blog(self, topic: str, intro_sentences: int = 3, content_paragraphs: int = 4, summary_sentences: int = 2):
        """Generate a complete blog post"""
        # Fix common spelling mistakes
        if "Fianance" in topic:
            topic = topic.replace("Fianance", "Finance")
            
        self.research_topic(topic)
        research_context = self.memory.get_all_research()
        
        # Check if we have any valid research data
        all_failed = True
        for item in self.memory.research_data:
            content = item.get('content', '')
            if "failed" not in content.lower() and "error" not in content.lower():
                all_failed = False
                break
        
        if all_failed:
            logging.warning("All research sources failed, using fallback content")
            research_context = f"Basic information about {topic}. This is a fallback due to research failures."
        
        # Calculate target word count based on size
        target_word_count = self._get_target_word_count(intro_sentences, content_paragraphs, summary_sentences)
        
        blog_prompt = f"""
You are an expert blog writer. Create a professional, insightful blog about "{topic}" using ONLY the research data provided.

Research Data:
{research_context}

CRITICAL WORD COUNT REQUIREMENT: You MUST write AT LEAST {target_word_count} words.
This is NON-NEGOTIABLE. Count your words and ensure you meet this minimum.
If you write less than {target_word_count} words, the blog will be rejected.
Write detailed, comprehensive paragraphs to reach the word count.

MANDATORY STRUCTURE:

Write ONE impactful, engaging title (10-15 words max) on the first line.
The title should be catchy, professional, and clearly indicate the blog's focus.

Then write ONE compelling subtitle (20-30 words max) on the next line.
The subtitle should expand on the title and provide context about what readers will learn.

Then write the introduction:
Write EXACTLY {intro_sentences} SHORT, punchy sentences:
- Sentence 1: Open with a powerful statement or statistic
- Sentence 2: Explain the immediate impact or "why now"
- Sentence 3: Preview what the blog will explore
- Keep each sentence under 20 words
- Use active voice and clear language

Then write EXACTLY {content_paragraphs} distinct, analytical paragraphs for the main content:

Each paragraph MUST be AT LEAST 200-300 words long to meet the {target_word_count} word minimum.

Each paragraph should:
- Start with a clear topic sentence
- Include specific examples or data from research
- Explain the real-world impact in detail with multiple sentences
- Provide deep analysis and context
- Add a transition to the next paragraph
- Be comprehensive and thorough - do NOT write short paragraphs

Paragraph 1 - Policies & Reforms (200-300 words):
- Start with a subheading: "Policies & Reforms:"
- State the policy/reform with context
- Add smooth transition from intro
- Explain its REAL-WORLD IMPACT in multiple sentences
- Include specific schemes with correct names and dates
- Add detailed case study or example
- Write at least 200 words for this paragraph

Paragraph 2 - Technology & Digital Transformation (200-300 words):
- Start with a subheading: "Technology & Digital Transformation:"
- Use transition phrase ("Building on this," "Furthermore," "In parallel,")
- Describe the technology/platform with detailed real examples
- Explain HOW it changes the landscape in depth
- Mention specific tools, platforms, or initiatives with details
- Add human insight with multiple sentences
- Write at least 200 words for this paragraph

Paragraph 3 - Current Challenges & Real Data (200-300 words):
- Start with a subheading: "Current Challenges & Real Data:"
- Smooth transition ("However," "Despite progress," "Yet challenges remain")
- Present verified statistics from credible sources with context
- Explain implications with detailed insight
- Discuss multiple challenges in depth
- End with forward-looking transition
- Write at least 200 words for this paragraph

Paragraph 4 - Future Outlook & Predictions (200-300 words):
- Start with a subheading: "Future Outlook & Predictions:"
- Transition with "Looking ahead," or "The next 3-5 years will..."
- Discuss emerging trends in detail
- Provide specific predictions with detailed reasoning
- Add human insight with multiple sentences
- End with implications for readers/stakeholders
- Write at least 200 words for this paragraph

Then write a summary section with EXACTLY {summary_sentences} DISTINCT sentences:
- Synthesize KEY INSIGHTS (do NOT repeat intro or body facts)
- Include forward-looking statement ("Over the next 3-5 years...")
- End with actionable insight or thought-provoking statement
- Make it memorable and impactful

Finally, list all sources at the end:
- Format: "Source Name" (one per line)
- Include ONLY the main site name (e.g., "Wikipedia", "Forbes", "TechCrunch")
- DO NOT include full URLs

IMPORTANT: Do NOT include section labels like "HEADING", "SUBTITLE", "INTRODUCTION", "CONTENT SECTION", "SUMMARY", or "SOURCES" in your output. Just write the content directly.

CRITICAL QUALITY STANDARDS:
1. DEPTH: Every paragraph must answer "Why does this matter?"
2. ACCURACY: Use ONLY data from research - cite sources inline
3. BALANCE: Include global + regional perspectives
4. INSIGHT: Add analytical commentary, not just facts
5. COMPLETENESS: Cover all key subdomains relevant to topic
6. PREDICTIVE: Include future trends and implications
7. SOURCES: Extract and list only the main site names from research data
8. SEO: Use subheadings every 200-300 words and keep paragraphs short (2-4 lines)
9. TITLE: Make it professional, engaging, and relevant to the topic
10. SUBTITLE: Provide context and value proposition for readers

Write the blog now:
"""
        
        logging.info("Generating blog post...")
        
        if self.use_openrouter:
            return self._generate_with_openrouter(blog_prompt, topic)
        else:
            return self._generate_mock_blog(topic, research_context, intro_sentences, content_paragraphs, summary_sentences)
    
    def _get_target_word_count(self, intro_sentences, content_paragraphs, summary_sentences):
        """Calculate target word count based on blog size"""
        # Fixed word counts for each size
        if content_paragraphs == 3:  # Small
            return 800  # Minimum 800 words
        elif content_paragraphs == 4:  # Medium
            return 1200  # 1200 words
        else:  # Large (6 paragraphs)
            return 1800  # 1800 words
    
    def _generate_with_openrouter(self, prompt, topic):
        """Generate blog using OpenRouter API with enhanced error handling"""
        import re
        models = [
            "google/gemini-2.0-flash-exp:free",
            "mistralai/mistral-7b-instruct:free",
            "qwen/qwen3-coder:free",
            "meta-llama/llama-3.2-3b-instruct:free",
            "z-ai/glm-4.5-air:free",
            "google/gemma-2-9b-it:free",
            "huggingfaceh4/zephyr-7b-beta:free"
        ]
        
        for model in models:
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "http://localhost:5000",
                        "X-Title": "Blog Generation System",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are a factual, structured blog generator. Write accurate, well-researched content."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.5
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    content = response.json()["choices"][0]["message"]["content"]
                    
                    # Clean up formatting
                    content = content.replace('**', '').replace('*', '')
                    content = re.sub(r'===\s*(.*?)\s*===', r'\n\n\1\n\n', content)
                    content = re.sub(r'\n+Note:.*$', '', content, flags=re.IGNORECASE | re.DOTALL)
                    content = re.sub(r'\n+\d+:.*picture.*$', '', content, flags=re.MULTILINE)
                    content = re.sub(r'(A |The )?(photo|screenshot|picture|image) of.*?\n', '', content, flags=re.IGNORECASE)
                    content = re.sub(r'Screenshot:.*?\n', '', content, flags=re.IGNORECASE)
                    content = re.sub(r'\[Caption:.*?\]', '', content, flags=re.IGNORECASE)
                    content = re.sub(r'\n{3,}', '\n\n', content)
                    content = content.strip()
                    
                    # Validate content quality
                    if self._validate_content(content, prompt):
                        # Remove all image tags
                        content = re.sub(r'\[IMAGE:[^\]]+\]', '', content)
                        content = self._format_blog_html(content)
                        content = self._add_sources(content)
                        logging.info(f"Blog generated successfully using {model}")
                        return content
                    else:
                        logging.warning(f"Content validation failed for {model}, trying next model")
                        continue
                else:
                    logging.warning(f"Model {model} failed: {response.status_code}")
            except Exception as e:
                logging.error(f"Model {model} error: {str(e)}")
        
        logging.error("All models failed")
        return "Error: All OpenRouter models failed. Please check your API key and try again."
    
    def _format_blog_html(self, content):
        """Format the blog content with proper HTML structure and styling"""
        import re
        
        # Remove section labels
        content = re.sub(r'^(HEADING|SUBTITLE|INTRODUCTION|CONTENT SECTION|SUMMARY|SOURCES)\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n{3,}', '\n\n', content).strip()
        
        lines = content.split('\n')
        formatted = '<div class="blog-container">'
        
        # Add CSS styling
        css = '<style>'
        css += '.blog-container { max-width: 900px; margin: 0 auto; font-family: "Segoe UI", Arial, sans-serif; line-height: 1.8; color: #333; }'
        css += '.blog-title { text-align: center; font-size: 32px; font-weight: bold; color: #1a1a1a; margin: 30px 0 20px 0; padding: 0 20px; text-decoration: none; }'
        css += '.blog-subtitle { font-size: 20px; font-weight: bold; color: #2c3e50; margin: 25px 0 15px 0; border-left: 4px solid #3498db; padding-left: 15px; text-decoration: none; }'
        css += '.section-heading { font-size: 20px; font-weight: bold; color: #2c3e50; margin: 25px 0 15px 0; border-left: 4px solid #3498db; padding-left: 15px; text-decoration: none; }'
        css += '.blog-container p { font-size: 16px; margin: 15px 0; text-align: justify; line-height: 1.8; text-decoration: none; }'
        css += '.blog-container * { text-decoration: none !important; }'
        css += '.sources-section { margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0; }'
        css += '</style>\n'
        formatted += css
        
        line_count = 0
        current_para = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_para:
                    formatted += f'<p>{" ".join(current_para)}</p>\n'
                    current_para = []
                continue
            
            # First line is title
            if line_count == 0:
                formatted += f'<h1 class="blog-title">{line}</h1>\n'
                line_count += 1
            # Second line is subtitle
            elif line_count == 1:
                formatted += f'<div class="blog-subtitle">{line}</div>\n'
                line_count += 1
            # Check for section headings (subheadings within content)
            elif (line.startswith(('###', '##', '#')) or 
                  (len(line.split()) <= 10 and ':' in line and any(keyword in line.lower() for keyword in 
                   ['policies', 'technology', 'challenges', 'future', 'outlook', 'reforms', 'transformation', 'data', 'summary']))):
                if current_para:
                    formatted += f'<p>{" ".join(current_para)}</p>\n'
                    current_para = []
                clean_line = line.replace('###', '').replace('##', '').replace('#', '').strip()
                formatted += f'<h2 class="section-heading">{clean_line}</h2>\n'
            # Skip image lines
            elif '<div style="text-align:center' in line or '<img' in line:
                if current_para:
                    formatted += f'<p>{" ".join(current_para)}</p>\n'
                    current_para = []
                continue
            # Regular content
            else:
                current_para.append(line)
        
        # Add any remaining paragraph
        if current_para:
            formatted += f'<p>{" ".join(current_para)}</p>\n'
        
        formatted += '</div>'
        return formatted
    
    def _add_sources(self, content: str) -> str:
        """Format and enhance sources section"""
        import re
        
        # Extract sources section
        sources_match = re.search(r'(===\s*SOURCES\s*===|Sources:|References:)(.*?)$', content, re.IGNORECASE | re.DOTALL)
        
        if sources_match:
            sources_text = sources_match.group(2).strip()
            # Extract only the main site names from URLs
            sources = re.findall(r'(?:Source: )?([^-\n]+)', sources_text)
            clean_sources = []
            
            for source in sources:
                # Extract just the domain name
                if '://' in source:
                    domain = source.split('://')[1].split('/')[0]
                    clean_sources.append(domain)
                else:
                    clean_sources.append(source.strip())
            
            # Format sources nicely
            formatted_sources = "\n\n---\n\nSources & References:\n\n"
            for source in clean_sources:
                formatted_sources += f"• {source}\n"
            
            content = content[:sources_match.start()] + formatted_sources
        else:
            # Add placeholder if no sources found
            content += "\n\n---\n\nSources & References:\n\nBased on research data from Wikipedia and web sources."
        
        return content
    

    
    def _validate_content(self, content: str, prompt: str) -> bool:
        """Validate generated content for quality and relevance"""
        content_lower = content.lower()
        prompt_lower = prompt.lower()
        
        import re
        
        # Check for off-topic content
        if 'education' in prompt_lower and 'motorcycle' in content_lower:
            return False
        
        # Check minimum length
        if len(content) < 800:
            return False
        
        # Check for placeholder text
        if 'lorem ipsum' in content_lower or '[insert' in content_lower:
            return False
        
        # Check for fabricated percentages (common hallucination pattern)
        if re.search(r'\d{2}% of.*in 202[45]', content) and 'source' not in content_lower:
            logging.warning("Detected unsourced statistics")
            return False
        
        return True
    
    def _generate_mock_blog(self, topic, research, intro_sentences, content_paragraphs, summary_sentences):
        """Generate a structured blog without AI when API is unavailable"""
        intro = '. '.join([f'This blog explores the fascinating world of {topic}' for _ in range(intro_sentences)])
        content = '\n\n'.join([f'**Paragraph {i+1}:** {topic} represents a significant area of interest.' for i in range(content_paragraphs)])
        summary = '. '.join([f'In conclusion, {topic} is important' for _ in range(summary_sentences)])
        
        return f"""# {topic.title()}: A Comprehensive Overview

## Introduction
{intro}.

## Content

{content}

## Research Sources
{research}

## Summary
{summary}.

---
*Note: For AI-generated content, please provide a valid OpenRouter API key.*
"""
    
    def clear_memory(self):
        """Clear the agent's memory"""
        self.memory.clear()