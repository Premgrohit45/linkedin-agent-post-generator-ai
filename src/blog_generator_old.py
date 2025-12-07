"""
LinkedIn Blog Generator with Multi-AI Provider Support
This module handles the generation of LinkedIn blog posts using multiple AI providers.
"""

from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from .multi_ai_provider import MultiAIBlogGenerator

# Load environment variables
load_dotenv()

class LinkedInBlogGenerator:
    """
    A class to generate LinkedIn blog posts using multiple AI providers with smart fallback.
    Supports OpenAI GPT, Anthropic Claude, Groq, and Google AI.
    """
    
    def __init__(self):
        """Initialize the blog generator with multi-AI provider support."""
        
        # Initialize the multi-AI generator
        self.multi_ai = MultiAIBlogGenerator()
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        available_providers = self.multi_ai.get_available_providers()
        
        if available_providers:
            self.logger.info(f"LinkedIn Blog Generator initialized with providers: {available_providers}")
        else:
            self.logger.warning("LinkedIn Blog Generator initialized with NO AI providers - will use fallback content only")
        
        self.logger.info("LinkedIn Blog Generator initialized successfully")
    
    def get_available_providers(self) -> List[str]:
        """
        Get list of available AI providers.
        """
        return self.multi_ai.get_available_providers()
    
    def generate_fallback_content(self, topic: str, tone: str, length: str, target_audience: str) -> Dict[str, str]:
        """
        Generate basic content structure when API quota is exceeded.
        """
        length_words = {"short": 150, "medium": 300, "long": 500}
        target_words = length_words.get(length, 300)
        
        return {
            'title': f"Professional Insights on {topic}",
            'content': f"""Thank you for your interest in {topic}.

Due to current API limitations, we're unable to generate personalized content at this moment. However, here are some key points to consider when exploring {topic}:

1. Understanding the current landscape and market trends
2. Identifying opportunities for growth and innovation  
3. Developing strategic approaches for implementation
4. Building sustainable practices for long-term success

For {target_audience}, it's particularly important to focus on practical applications and measurable outcomes when approaching {topic}.

We recommend conducting thorough research and consulting with industry experts to develop comprehensive strategies that align with your specific goals and requirements.""",
            'hashtags': f"#{topic.replace(' ', '')} #Professional #Business #Strategy #Growth #Innovation #Leadership",
            'call_to_action': "What are your thoughts on this topic? Share your experiences and insights in the comments below.",
            'generated_at': datetime.now().isoformat(),
            'topic': topic,
            'tone': tone,
            'length': length,
            'fallback': True
        }
    
    def generate_blog_post(self, 
                          topic: str, 
                          tone: str = "professional",
                          length: str = "medium",
                          target_audience: str = "professionals",
                          include_hashtags: bool = True,
                          include_call_to_action: bool = True) -> Dict[str, str]:
        """
        Generate a LinkedIn blog post on a given topic.
        
        Args:
            topic (str): The main topic/theme for the blog post
            tone (str): Tone of the blog (professional, casual, inspirational, etc.)
            length (str): Length of the blog (short, medium, long)
            target_audience (str): Target audience description
            include_hashtags (bool): Whether to include hashtags
            include_call_to_action (bool): Whether to include a call to action
            
        Returns:
            Dict[str, str]: Generated blog post with title, content, hashtags, etc.
        """
        try:
            # First check if API quota is available
            if not self.check_api_quota():
                self.logger.warning("API quota exceeded, using fallback content")
                return self.generate_fallback_content(topic, tone, length, target_audience)
            
            # Create the prompt for blog generation
            prompt = self._create_blog_prompt(
                topic=topic,
                tone=tone,
                length=length,
                target_audience=target_audience,
                include_hashtags=include_hashtags,
                include_call_to_action=include_call_to_action
            )
            
            self.logger.info(f"Generating blog post for topic: {topic}")
            
            # Generate the blog post using Google AI with error handling
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        candidate_count=1,
                        max_output_tokens=2048,
                        temperature=0.7,
                    )
                )
                
                if not response.text:
                    raise Exception("No content generated from Google AI")
                
                # Parse the response
                blog_data = self._parse_blog_response(response.text)
                
                # Add metadata
                blog_data['generated_at'] = datetime.now().isoformat()
                blog_data['topic'] = topic
                blog_data['tone'] = tone
                blog_data['length'] = length
                
                self.logger.info("Blog post generated successfully")
                return blog_data
                
            except Exception as api_error:
                error_message = str(api_error).lower()
                
                if "quota" in error_message or "exceeded" in error_message or "limit" in error_message:
                    self.logger.warning("API quota exceeded during generation, using fallback content")
                    fallback_content = self.generate_fallback_content(topic, tone, length, target_audience)
                    fallback_content['quota_warning'] = (
                        "⚠️ API Quota Exceeded - Using fallback content.\n\n"
                        "Your Google AI (Gemini) quota has been reached.\n"
                        "Solutions: Wait 24 hours, upgrade plan, or check https://makersuite.google.com"
                    )
                    return fallback_content
                    
                elif "rate" in error_message:
                    self.logger.warning("Rate limit exceeded, using fallback content")
                    fallback_content = self.generate_fallback_content(topic, tone, length, target_audience)
                    fallback_content['rate_warning'] = (
                        "⚠️ Rate Limit Exceeded - Using fallback content.\n"
                        "Please wait 60 seconds before generating another blog post."
                    )
                    return fallback_content
                else:
                    raise Exception(f"Google AI API Error: {api_error}")
            
        except Exception as e:
            self.logger.error(f"Error generating blog post: {str(e)}")
            raise
    
    def _create_blog_prompt(self, topic: str, tone: str, length: str, 
                           target_audience: str, include_hashtags: bool, 
                           include_call_to_action: bool) -> str:
        """
        Create a detailed prompt for blog generation.
        """
        length_guidelines = {
            "short": "150-300 words",
            "medium": "400-600 words", 
            "long": "700-1000 words"
        }
        
        prompt = f"""
        Create a professional LinkedIn blog post with the following specifications:

        Topic: {topic}
        Tone: {tone}
        Length: {length_guidelines.get(length, "400-600 words")}
        Target Audience: {target_audience}

        IMPORTANT FORMATTING GUIDELINES:
        - Use clean, professional text WITHOUT asterisks (*) for emphasis
        - DO NOT use emojis in the main content
        - Use proper paragraphs with clear line breaks
        - Write in a conversational yet professional style
        - Focus on valuable insights and actionable advice
        - Avoid excessive formatting symbols or decorative elements
        - Keep the {tone} tone throughout

        CONTENT REQUIREMENTS:
        1. Create an engaging, professional title (no emojis)
        2. Write a compelling opening paragraph
        3. Include 2-3 main points with practical insights
        4. Use clear, readable formatting with proper paragraphs
        5. Make it valuable and shareable for {target_audience}
        
        {"6. Include 5-8 relevant hashtags (hashtags only, no decorative elements)" if include_hashtags else ""}
        {"7. End with a professional call-to-action that encourages meaningful engagement" if include_call_to_action else ""}

        FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:
        TITLE: [Clean professional title here]
        
        CONTENT: [Main blog post content in clear paragraphs, no asterisks or emojis]
        
        {"HASHTAGS: [Only hashtags, separated by spaces]" if include_hashtags else ""}
        
        {"CALL_TO_ACTION: [Professional call to action]" if include_call_to_action else ""}

        Remember: Focus on professional, clean content that provides real value without unnecessary formatting.
        """
        
        return prompt
    
    def _parse_blog_response(self, response_text: str) -> Dict[str, str]:
        """
        Parse the AI response into structured blog data.
        """
        blog_data = {
            'title': '',
            'content': '',
            'hashtags': '',
            'call_to_action': '',
            'full_post': response_text
        }
        
        lines = response_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('TITLE:'):
                current_section = 'title'
                blog_data['title'] = line.replace('TITLE:', '').strip()
            elif line.startswith('CONTENT:'):
                current_section = 'content'
                blog_data['content'] = line.replace('CONTENT:', '').strip()
            elif line.startswith('HASHTAGS:'):
                current_section = 'hashtags'
                blog_data['hashtags'] = line.replace('HASHTAGS:', '').strip()
            elif line.startswith('CALL_TO_ACTION:'):
                current_section = 'call_to_action'
                blog_data['call_to_action'] = line.replace('CALL_TO_ACTION:', '').strip()
            elif current_section and line:
                # Continue adding to the current section
                if blog_data[current_section]:
                    blog_data[current_section] += '\n' + line
                else:
                    blog_data[current_section] = line
        
        # Clean the content to ensure professional formatting
        blog_data = self._clean_content(blog_data)
        
        return blog_data
    
    def _clean_content(self, blog_data: Dict[str, str]) -> Dict[str, str]:
        """
        Clean the generated content to ensure professional formatting.
        """
        import re
        
        # Clean title - remove excessive formatting
        if blog_data['title']:
            blog_data['title'] = re.sub(r'\*+', '', blog_data['title'])  # Remove asterisks
            blog_data['title'] = re.sub(r'[🎯📝💡🚀✨🔥💪🌟📈⭐️🎪🎭🎨🎬🎤🎼🎵🎶🎸🎺🎻🥳🤝👍💯]', '', blog_data['title'])  # Remove common emojis
            blog_data['title'] = blog_data['title'].strip()
        
        # Clean content - remove excessive formatting and emojis
        if blog_data['content']:
            content = blog_data['content']
            # Remove asterisks used for emphasis
            content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)  # Remove **bold**
            content = re.sub(r'\*([^*]+)\*', r'\1', content)      # Remove *italic*
            content = re.sub(r'\*+', '', content)                # Remove remaining asterisks
            
            # Remove emojis from content (keep it professional)
            content = re.sub(r'[🎯📝💡🚀✨🔥💪🌟📈⭐️🎪🎭🎨🎬🎤🎼🎵🎶🎸🎺🎻🥳🤝👍💯🌍🌎🌏🔮🎊🎉🎈🎀🎁🏆🥇🥈🥉🏅🎖️🏵️🎗️]', '', content)
            
            # Clean up multiple line breaks
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Remove bullet points and formatting symbols
            content = re.sub(r'^[•▪▫◦‣⁃]\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'^[-*]\s+', '', content, flags=re.MULTILINE)
            
            blog_data['content'] = content.strip()
        
        # Clean hashtags - keep only actual hashtags
        if blog_data['hashtags']:
            hashtags = blog_data['hashtags']
            # Remove emojis from hashtags
            hashtags = re.sub(r'[🎯📝💡🚀✨🔥💪🌟📈⭐️🎪🎭🎨🎬🎤🎼🎵🎶🎸🎺🎻🥳🤝👍💯]', '', hashtags)
            # Ensure hashtags start with #
            hashtags = re.sub(r'(?<!\#)\b([A-Za-z][A-Za-z0-9_]*)', r'#\1', hashtags)
            blog_data['hashtags'] = hashtags.strip()
        
        # Clean call to action
        if blog_data['call_to_action']:
            cta = blog_data['call_to_action']
            # Remove emojis from CTA
            cta = re.sub(r'[🎯📝💡🚀✨🔥💪🌟📈⭐️🎪🎭🎨🎬🎤🎼🎵🎶🎸🎺🎻🥳🤝👍💯]', '', cta)
            cta = re.sub(r'\*+', '', cta)  # Remove asterisks
            blog_data['call_to_action'] = cta.strip()
        
        return blog_data
    
    def generate_multiple_posts(self, topics: List[str], **kwargs) -> List[Dict[str, str]]:
        """
        Generate multiple blog posts for different topics.
        
        Args:
            topics (List[str]): List of topics to generate posts for
            **kwargs: Additional parameters for blog generation
            
        Returns:
            List[Dict[str, str]]: List of generated blog posts
        """
        blog_posts = []
        
        for topic in topics:
            try:
                post = self.generate_blog_post(topic=topic, **kwargs)
                blog_posts.append(post)
                self.logger.info(f"Generated post for topic: {topic}")
            except Exception as e:
                self.logger.error(f"Failed to generate post for topic '{topic}': {str(e)}")
                continue
        
        return blog_posts
    
    def get_topic_suggestions(self, industry: str, keywords: List[str] = None) -> List[str]:
        """
        Generate topic suggestions for blog posts based on industry and keywords.
        
        Args:
            industry (str): The industry or field
            keywords (List[str]): Optional keywords to include
            
        Returns:
            List[str]: List of suggested topics
        """
        try:
            keywords_str = ", ".join(keywords) if keywords else "general topics"
            
            prompt = f"""
            Suggest 10 trending and engaging LinkedIn blog post topics for the {industry} industry.
            
            Consider these keywords: {keywords_str}
            
            Make sure the topics are:
            1. Relevant to current industry trends
            2. Engaging and likely to get good engagement on LinkedIn
            3. Valuable to professionals in this field
            4. Actionable and practical
            
            Format your response as a numbered list:
            1. Topic 1
            2. Topic 2
            ...etc
            """
            
            response = self.model.generate_content(prompt)
            
            # Extract topics from response
            topics = []
            lines = response.text.split('\n')
            for line in lines:
                line = line.strip()
                if line and any(line.startswith(f"{i}.") for i in range(1, 11)):
                    topic = line.split('.', 1)[1].strip() if '.' in line else line
                    topics.append(topic)
            
            return topics
            
        except Exception as e:
            self.logger.error(f"Error generating topic suggestions: {str(e)}")
            return []


if __name__ == "__main__":
    # Example usage
    try:
        # Initialize the generator
        generator = LinkedInBlogGenerator()
        
        # Generate a blog post
        blog_post = generator.generate_blog_post(
            topic="The Future of AI in Business",
            tone="professional",
            length="medium",
            target_audience="business professionals and entrepreneurs"
        )
        
        print("Generated Blog Post:")
        print(f"Title: {blog_post['title']}")
        print(f"\nContent:\n{blog_post['content']}")
        print(f"\nHashtags: {blog_post['hashtags']}")
        print(f"\nCall to Action: {blog_post['call_to_action']}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your GOOGLE_API_KEY in the .env file")