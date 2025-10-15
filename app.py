from flask import Flask, render_template, request, jsonify
from agent import BlogAgent
from output import OutputManager
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

try:
    agent = BlogAgent()
    logger.info("BlogAgent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize BlogAgent: {str(e)}")
    agent = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_blog():
    try:
        if not agent:
            return jsonify({'error': 'Blog generation service is not available. Please check server logs.'}), 503
            
        data = request.json
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        blog_size = data.get('blog_size', 'medium')
        size_map = {
            'small': {'intro': 2, 'content': 3, 'summary': 1},
            'medium': {'intro': 3, 'content': 4, 'summary': 2},
            'large': {'intro': 4, 'content': 6, 'summary': 3}
        }
        sizes = size_map.get(blog_size, size_map['medium'])
        intro_sentences = sizes['intro']
        content_paragraphs = sizes['content']
        summary_sentences = sizes['summary']
        
        # Generate blog
        logger.info(f"Generating blog for topic: {topic}, size: {blog_size}")
        blog_content = agent.generate_blog(
            topic=topic,
            intro_sentences=intro_sentences,
            content_paragraphs=content_paragraphs,
            summary_sentences=summary_sentences
        )
        
        return jsonify({
            'success': True,
            'blog_content': blog_content,
            'topic': topic,
            'blog_size': blog_size
        })
        
    except Exception as e:
        logger.error(f"Error generating blog: {str(e)}", exc_info=True)
        return jsonify({'error': f'An error occurred while generating the blog: {str(e)}'}), 500

@app.route('/save', methods=['POST'])
def save_blog():
    try:
        data = request.json
        blog_content = data.get('blog_content', '')
        topic = data.get('topic', '')
        format_type = data.get('format', 'markdown')
        
        if format_type == 'text':
            filepath = OutputManager.save_to_text(blog_content, topic)
        else:
            filepath = OutputManager.save_to_markdown(blog_content, topic)
        
        return jsonify({
            'success': True,
            'filepath': filepath
        })
        
    except Exception as e:
        logger.error(f"Error saving blog: {str(e)}", exc_info=True)
        return jsonify({'error': f'An error occurred while saving the blog: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)