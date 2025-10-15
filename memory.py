class ShortTermMemory:
    def __init__(self):
        self.research_data = []
        self.max_research_items = 3  # Limit to 3 research sources
    
    def add_research(self, source: str, content: str):
        """Add research data to memory with size limit"""
        # If we already have this source, update it
        for i, item in enumerate(self.research_data):
            if item['source'] == source:
                self.research_data[i] = {'source': source, 'content': content}
                return
        
        # Add new research item
        self.research_data.append({
            'source': source,
            'content': content
        })
        
        # Limit the number of research items
        if len(self.research_data) > self.max_research_items:
            self.research_data = self.research_data[-self.max_research_items:]
    
    def get_all_research(self) -> str:
        """Get all research data as formatted string"""
        if not self.research_data:
            return "No research data available."
        
        formatted_data = []
        for item in self.research_data:
            # Limit content length to avoid overly long prompts
            content = item['content']
            if len(content) > 1000:
                content = content[:1000] + "..."
            
            formatted_data.append(f"Source: {item['source']}\n{content}")
        
        return "\n\n" + "\n\n".join(formatted_data)
    
    def clear(self):
        """Clear all memory"""
        self.research_data = []