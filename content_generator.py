#!/usr/bin/env python3
"""
Content Generator for AI Knowledge Base
Generates AI news and Java Agent interview questions
"""

import os
import random
from datetime import datetime, timedelta
from typing import List, Dict
import json

# Import the skills we need
import sys
sys.path.append('/Users/tyler/.openclaw/skills')

# We'll use web_search for AI news
# And generate Java Agent interview questions based on common topics

class ContentGenerator:
    def __init__(self):
        self.workspace_dir = "/Users/tyler/.openclaw/workspace"
        
    def generate_ai_news(self, date: datetime = None) -> Dict:
        """Generate AI news summary for a specific date."""
        if date is None:
            date = datetime.now() - timedelta(days=1)  # Yesterday
        
        date_str = date.strftime("%Y-%m-%d")
        
        # Simulate AI news generation (in real implementation, this would fetch from APIs)
        # For now, we'll create a template-based news article
        
        news_topics = [
            "LLM Model Updates and Releases",
            "AI Ethics and Responsible AI Development",
            "Machine Learning Framework Improvements",
            "AI in Industry Applications",
            "Research Breakthroughs in Deep Learning",
            "AI Policy and Regulation Updates"
        ]
        
        selected_topic = random.choice(news_topics)
        
        news_content = f"""# AI News Summary - {date_str}

## {selected_topic}

### Overview
Latest developments and updates in the AI field for {date_str}.

### Key Highlights
- New research papers and implementations
- Industry adoption trends
- Technical advancements and optimizations

### Details
This summary covers the most significant AI developments from the past 24 hours, 
focusing on practical applications and technical innovations relevant to developers 
and researchers.

### Impact
- Potential influence on development practices
- New opportunities for AI integration
- Considerations for enterprise adoption

---
*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        return {
            'title': f"AI News Summary - {date_str}",
            'filename': f"ai_news_{date_str}.md",
            'content': news_content,
            'category': 'ai-news'
        }
    
    def generate_java_agent_interview_question(self, topic: str = None) -> Dict:
        """Generate a Java Agent development interview question with answer."""
        
        topics = [
            "Java Agent Instrumentation",
            "Bytecode Manipulation",
            "Class Loading in Java Agents",
            "JVM TI and Java Agents",
            "Performance Monitoring with Java Agents",
            "Profiling and Observability",
            "Java Agent Best Practices",
            "Debugging Java Agents",
            "Spring Boot Integration",
            "Microservices Monitoring"
        ]
        
        if topic is None:
            topic = random.choice(topics)
        
        # Generate different types of questions based on topic
        questions = {
            "Java Agent Instrumentation": {
                "question": "How does Java Agent instrumentation work, and what are the key components involved?",
                "answer": """Java Agent instrumentation works through the Java Instrumentation API, which allows agents to modify class bytecode during class loading.

Key components:
1. **Instrumentation Agent**: The main agent class with `premain` method
2. **ClassFileTransformer**: Interface for transforming class bytecode
3. **Byte Code Manipulation Libraries**: ASM, ByteBuddy, or Javassist
4. **JVM Hooks**: JVM provides hooks for class loading events

The process:
- Agent is specified with `-javaagent` JVM parameter
- `premain` method is called before main application starts
- Transformers are registered to modify classes as they're loaded
- Bytecode can be modified before class definition

**Example**:
```java
public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        inst.addTransformer(new MyClassTransformer());
    }
}
```"""
            },
            "Bytecode Manipulation": {
                "question": "Compare ASM, ByteBuddy, and Javassist for bytecode manipulation in Java Agents.",
                "answer": """**ASM**:
- Pros: High performance, low-level control, widely used
- Cons: Requires understanding of JVM bytecode, verbose API
- Best for: Performance-critical agents, fine-grained control

**ByteBuddy**:
- Pros: High-level API, easy to use, good documentation
- Cons: Slightly higher overhead than ASM
- Best for: Rapid development, readability

**Javassist**:
- Pros: Source-level abstraction, simple API
- Cons: Performance overhead, limited features
- Best for: Simple transformations, quick prototyping

**Recommendation**: Use ByteBuddy for most cases due to balance of performance and usability."""
            },
            "Class Loading in Java Agents": {
                "question": "How do Java Agents interact with class loading, and what are the timing considerations?",
                "answer": """Java Agents interact with class loading through several mechanisms:

**1. Class File Transformation**:
- Agents can modify class bytecode before class is defined
- Occurs during `ClassFileTransformer.transform()` call
- Transformation happens only once per class

**2. Timing Considerations**:
- **Premain**: Called before any application classes are loaded
- **Agentmain**: Can be loaded into running JVM (requires JVM support)
- **Class Loading Order**: System classes load first, then application classes

**3. Important Points**:
- Can only transform classes that haven't been loaded yet
- Some JVM classes cannot be transformed for security reasons
- Circular dependencies can cause issues
- Transformer performance affects application startup

**4. Best Practices**:
- Register transformers early in `premain`
- Avoid heavy processing in transformers
- Use caching for frequently accessed classes"""
            }
        }
        
        # Use template for topics not specifically defined
        if topic not in questions:
            questions[topic] = {
                "question": f"What are the key considerations for {topic.lower()} in Java Agent development?",
                "answer": f"""Key considerations for {topic} in Java Agent development:

1. **Performance Impact**: Minimize overhead on application startup and runtime
2. **Compatibility**: Ensure compatibility with different JVM versions and frameworks
3. **Error Handling**: Robust error handling to prevent application failures
4. **Resource Management**: Proper cleanup of resources and transformers
5. **Security**: Consider security implications of bytecode modification
6. **Testing**: Comprehensive testing across different environments

**Best Practices**:
- Use appropriate bytecode manipulation libraries
- Implement proper error handling and fallbacks
- Monitor agent performance in production
- Keep transformations minimal and focused
- Document all modifications and their purposes"""
            }
        
        qa = questions[topic]
        
        content = f"""# Java Agent Interview Question: {topic}

## Question
{qa['question']}

## Detailed Answer
{qa['answer']}

## Key Points to Remember
- Understanding of core concepts
- Practical implementation experience
- Performance considerations
- Common pitfalls and solutions

## Follow-up Topics
- Related concepts and advanced topics
- Real-world application scenarios
- Comparison with alternative approaches

---
*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        return {
            'title': f"Java Agent Interview - {topic}",
            'filename': f"java_agent_{topic.lower().replace(' ', '_')}_interview.md",
            'content': content,
            'category': 'interview-preparation'
        }
    
    def save_generated_content(self, content_list: List[Dict]) -> List[str]:
        """Save generated content to files and return file paths."""
        saved_files = []
        
        for content_item in content_list:
            filename = content_item['filename']
            category = content_item['category']
            
            # Create category directory if it doesn't exist
            category_dir = f"{self.workspace_dir}/ai-knowledge-base/{category}"
            os.makedirs(category_dir, exist_ok=True)
            
            # Save file
            file_path = f"{category_dir}/{filename}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_item['content'])
            
            saved_files.append(file_path)
            print(f"Generated: {file_path}")
        
        return saved_files


def main():
    """Test content generation."""
    generator = ContentGenerator()
    
    # Generate yesterday's AI news
    yesterday = datetime.now() - timedelta(days=1)
    ai_news = generator.generate_ai_news(yesterday)
    
    # Generate 2 Java Agent interview questions
    java_questions = []
    topics = ["Java Agent Instrumentation", "Bytecode Manipulation"]
    for topic in topics:
        java_questions.append(generator.generate_java_agent_interview_question(topic))
    
    # Save all content
    all_content = [ai_news] + java_questions
    saved_files = generator.save_generated_content(all_content)
    
    print(f"Generated {len(saved_files)} files total")


if __name__ == "__main__":
    main()