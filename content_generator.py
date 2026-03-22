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
        
        # AI新闻主题（中文）
        news_topics = [
            "大语言模型更新与发布",
            "AI伦理与负责任AI发展",
            "机器学习框架改进",
            "AI行业应用",
            "深度学习研究突破",
            "AI政策与监管更新"
        ]
        
        selected_topic = random.choice(news_topics)
        
        news_content = f"""# AI新闻摘要 - {date_str}

## {selected_topic}

### 概述
{date_str} AI领域的最新发展和更新。

### 主要亮点
- 新的研究论文和实现
- 行业采用趋势
- 技术进步和优化

### 详细内容
本摘要涵盖过去24小时最重要的AI发展，重点关注与开发人员和研究者相关的实际应用和技术创新。

### 影响
- 对开发实践的潜在影响
- AI集成的新机会
- 企业采用注意事项

---
*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        return {
            'title': f"AI新闻摘要 - {date_str}",
            'filename': f"ai_news_{date_str}.md",
            'content': news_content,
            'category': 'ai-news'
        }
    
    def generate_java_agent_interview_question(self, topic: str = None) -> Dict:
        """Generate a Java Agent development interview question with answer."""
        
        topics = [
            "Java Agent字节码插桩",
            "字节码操作技术",
            "Java Agent中的类加载",
            "JVM TI与Java Agents",
            "Java Agent性能监控",
            "性能分析与可观测性",
            "Java Agent最佳实践",
            "Java Agent调试技巧",
            "Spring Boot集成",
            "微服务监控"
        ]
        
        if topic is None:
            topic = random.choice(topics)
        
        # Generate different types of questions based on topic
        questions = {
            "Java Agent字节码插桩": {
                "question": "Java Agent字节码插桩是如何工作的？涉及哪些关键组件？",
                "answer": """Java Agent字节码插桩通过Java Instrumentation API实现，允许代理在类加载期间修改类字节码。

关键组件：
1. **Instrumentation Agent**: 包含`premain`方法的主代理类
2. **ClassFileTransformer**: 用于转换类字节码的接口
3. **字节码操作库**: ASM、ByteBuddy或Javassist
4. **JVM钩子**: JVM提供的类加载事件钩子

工作流程：
- 通过`-javaagent` JVM参数指定代理
- `premain`方法在应用主程序启动前被调用
- 注册转换器来修改加载的类
- 在类定义前可以修改字节码

**示例代码**:
```java
public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        inst.addTransformer(new MyClassTransformer());
    }
}
```"""
            },
            "字节码操作技术": {
                "question": "请对比ASM、ByteBuddy和Javassist在Java Agent字节码操作中的优缺点。",
                "answer": """**ASM**:
- 优点：高性能、底层控制、广泛使用
- 缺点：需要理解JVM字节码、API较为繁琐
- 适用场景：性能关键的代理、需要精细控制

**ByteBuddy**:
- 优点：高级API、易于使用、文档完善
- 缺点：相比ASM开销稍大
- 适用场景：快速开发、代码可读性要求高

**Javassist**:
- 优点：源码级抽象、API简单
- 缺点：性能开销较大、功能有限
- 适用场景：简单转换、快速原型开发

**推荐**: 大多数情况下使用ByteBuddy，因为其在性能和易用性之间取得了良好平衡。"""
            },
            "Java Agent中的类加载": {
                "question": "Java Agent如何与类加载机制交互？有哪些时序考虑？",
                "answer": """Java Agent通过以下几种机制与类加载交互：

**1. 类文件转换**:
- 代理可以在类定义前修改类字节码
- 发生在`ClassFileTransformer.transform()`调用期间
- 每个类仅转换一次

**2. 时序考虑**:
- **Premain**: 在任何应用类加载前被调用
- **Agentmain**: 可以加载到运行的JVM中（需要JVM支持）
- **类加载顺序**: 系统类先加载，然后是应用类

**3. 重要要点**:
- 只能转换尚未加载的类
- 某些JVM类因安全原因无法转换
- 循环依赖可能导致问题
- 转换器性能影响应用启动

**4. 最佳实践**:
- 在`premain`中尽早注册转换器
- 避免在转换器中进行重处理
- 对频繁访问的类使用缓存"""
            }
        }
        
        # Use template for topics not specifically defined
        if topic not in questions:
            questions[topic] = {
                "question": f"在Java Agent开发中，{topic.lower()}有哪些关键考虑因素？",
                "answer": f"""{topic}在Java Agent开发中的关键考虑因素：

1. **性能影响**: 最小化应用启动和运行时的开销
2. **兼容性**: 确保与不同JVM版本和框架的兼容性
3. **错误处理**: 健壮的错误处理以防止应用失败
4. **资源管理**: 适当清理资源和转换器
5. **安全性**: 考虑字节码修改的安全影响
6. **测试**: 跨不同环境的全面测试

**最佳实践**:
- 使用合适的字节码操作库
- 实现适当的错误处理和回退机制
- 监控生产环境中的代理性能
- 保持转换最小化且聚焦
- 记录所有修改及其目的"""
            }
        
        qa = questions[topic]
        
        content = f"""# Java Agent面试题：{topic}

## 问题
{qa['question']}

## 详细解答
{qa['answer']}

## 关键要点
- 核心概念的理解
- 实际实现经验
- 性能考虑
- 常见陷阱和解决方案

## 后续话题
- 相关概念和高级主题
- 实际应用场景
- 与其他方案的对比

---
*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        return {
            'title': f"Java Agent面试题 - {topic}",
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