"""
LinkedIn Blog Agent - Main Orchestrator
This is the main agent that coordinates blog generation and email sending.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import argparse
import sys

# Import our custom modules
from blog_generator import LinkedInBlogGenerator
from email_sender import EmailSender

class LinkedInBlogAgent:
    """
    Main LinkedIn Blog Agent that orchestrates blog generation and email sending.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the LinkedIn Blog Agent.
        
        Args:
            config_path (Optional[str]): Path to configuration file
        """
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('linkedin_agent.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        try:
            self.blog_generator = LinkedInBlogGenerator()
            self.email_sender = EmailSender()
            
            self.logger.info("LinkedIn Blog Agent initialized successfully")
            
            # Create output directory if it doesn't exist
            self.output_dir = Path("output")
            self.output_dir.mkdir(exist_ok=True)
            
        except Exception as e:
            self.logger.error(f"Failed to initialize agent: {str(e)}")
            raise
    
    def generate_and_send_blog(self, 
                              topic: str,
                              tone: str = "professional",
                              length: str = "medium",
                              target_audience: str = "professionals",
                              recipient_email: Optional[str] = None,
                              save_to_file: bool = True) -> Dict[str, Any]:
        """
        Generate a blog post and send it via email.
        
        Args:
            topic (str): Blog post topic
            tone (str): Writing tone
            length (str): Blog length
            target_audience (str): Target audience
            recipient_email (Optional[str]): Email recipient
            save_to_file (bool): Whether to save to file
            
        Returns:
            Dict[str, Any]: Results of the operation
        """
        results = {
            'success': False,
            'blog_post': None,
            'email_sent': False,
            'file_saved': False,
            'errors': []
        }
        
        try:
            self.logger.info(f"Starting blog generation for topic: {topic}")
            
            # Generate blog post
            blog_post = self.blog_generator.generate_blog_post(
                topic=topic,
                tone=tone,
                length=length,
                target_audience=target_audience,
                include_hashtags=True,
                include_call_to_action=True
            )
            
            results['blog_post'] = blog_post
            self.logger.info("Blog post generated successfully")
            
            # Save to file if requested
            if save_to_file:
                file_path = self._save_blog_to_file(blog_post)
                results['file_saved'] = True
                results['file_path'] = str(file_path)
                self.logger.info(f"Blog post saved to: {file_path}")
            
            # Send email
            email_success = self.email_sender.send_blog_post(
                blog_post=blog_post,
                recipient=recipient_email
            )
            
            results['email_sent'] = email_success
            
            if email_success:
                self.logger.info("Email sent successfully")
            else:
                self.logger.warning("Email sending failed")
                results['errors'].append("Email sending failed")
            
            results['success'] = True
            
        except Exception as e:
            error_msg = f"Error in generate_and_send_blog: {str(e)}"
            self.logger.error(error_msg)
            results['errors'].append(error_msg)
        
        return results
    
    def generate_multiple_blogs(self,
                               topics: List[str],
                               tone: str = "professional",
                               length: str = "medium",
                               target_audience: str = "professionals",
                               recipient_email: Optional[str] = None,
                               send_separately: bool = True,
                               save_to_files: bool = True) -> Dict[str, Any]:
        """
        Generate multiple blog posts and send them via email.
        
        Args:
            topics (List[str]): List of blog topics
            tone (str): Writing tone
            length (str): Blog length
            target_audience (str): Target audience
            recipient_email (Optional[str]): Email recipient
            send_separately (bool): Send each post as separate email
            save_to_files (bool): Save posts to files
            
        Returns:
            Dict[str, Any]: Results of the operations
        """
        results = {
            'success': False,
            'blog_posts': [],
            'email_results': {},
            'files_saved': [],
            'errors': []
        }
        
        try:
            self.logger.info(f"Starting generation of {len(topics)} blog posts")
            
            # Generate all blog posts
            blog_posts = self.blog_generator.generate_multiple_posts(
                topics=topics,
                tone=tone,
                length=length,
                target_audience=target_audience,
                include_hashtags=True,
                include_call_to_action=True
            )
            
            results['blog_posts'] = blog_posts
            self.logger.info(f"Generated {len(blog_posts)} blog posts")
            
            # Save to files if requested
            if save_to_files:
                for i, post in enumerate(blog_posts):
                    try:
                        file_path = self._save_blog_to_file(post, suffix=f"_{i+1}")
                        results['files_saved'].append(str(file_path))
                    except Exception as e:
                        self.logger.error(f"Failed to save post {i+1}: {str(e)}")
            
            # Send emails
            if blog_posts:
                email_results = self.email_sender.send_multiple_posts(
                    blog_posts=blog_posts,
                    recipient=recipient_email,
                    send_separately=send_separately
                )
                results['email_results'] = email_results
                
                successful_emails = sum(1 for success in email_results.values() if success)
                self.logger.info(f"Successfully sent {successful_emails}/{len(email_results)} emails")
            
            results['success'] = True
            
        except Exception as e:
            error_msg = f"Error in generate_multiple_blogs: {str(e)}"
            self.logger.error(error_msg)
            results['errors'].append(error_msg)
        
        return results
    
    def generate_and_send_to_multiple_recipients(self,
                                               topic: str,
                                               recipients: List[str],
                                               tone: str = "professional",
                                               length: str = "medium",
                                               target_audience: str = "professionals",
                                               subject_prefix: str = "Generated LinkedIn Blog Post",
                                               personalized_subjects: Optional[Dict[str, str]] = None,
                                               save_to_file: bool = True,
                                               validate_emails: bool = True) -> Dict[str, Any]:
        """
        Generate a blog post and send it to multiple recipients with validation.
        
        Args:
            topic (str): Blog post topic
            recipients (List[str]): List of email addresses to send to
            tone (str): Writing tone
            length (str): Blog length
            target_audience (str): Target audience
            subject_prefix (str): Subject prefix for emails
            personalized_subjects (Optional[Dict[str, str]]): Custom subjects per recipient
            save_to_file (bool): Whether to save to file
            validate_emails (bool): Whether to validate email addresses
            
        Returns:
            Dict[str, Any]: Detailed results of the operation
        """
        results = {
            'success': False,
            'blog_post': None,
            'email_results': {},
            'file_saved': False,
            'errors': [],
            'validation_results': {}
        }
        
        try:
            self.logger.info(f"Starting blog generation for topic: {topic}")
            self.logger.info(f"Recipients: {len(recipients)} emails")
            
            # Generate blog post
            blog_post = self.blog_generator.generate_blog_post(
                topic=topic,
                tone=tone,
                length=length,
                target_audience=target_audience,
                include_hashtags=True,
                include_call_to_action=True
            )
            
            results['blog_post'] = blog_post
            self.logger.info("Blog post generated successfully")
            
            # Save to file if requested
            if save_to_file:
                file_path = self._save_blog_to_file(blog_post)
                results['file_saved'] = True
                results['file_path'] = str(file_path)
                self.logger.info(f"Blog post saved to: {file_path}")
            
            # Send emails with validation
            if validate_emails:
                email_results = self.email_sender.send_batch_with_validation(
                    blog_post=blog_post,
                    recipients=recipients,
                    subject_prefix=subject_prefix,
                    skip_invalid=True
                )
                results['email_results'] = email_results
                results['validation_results'] = email_results.get('validation', {})
                
                # Log summary
                summary = email_results.get('summary', {})
                self.logger.info(f"Email summary: {summary['emails_sent']}/{summary['valid_emails']} sent successfully")
                if summary['invalid_emails'] > 0:
                    self.logger.warning(f"Found {summary['invalid_emails']} invalid email addresses")
                    
            else:
                # Send without validation (legacy method)
                email_results = self.email_sender.send_to_multiple_recipients(
                    blog_post=blog_post,
                    recipients=recipients,
                    subject_prefix=subject_prefix,
                    personalized_subjects=personalized_subjects
                )
                results['email_results'] = {'sending': email_results}
                
                successful_sends = sum(1 for success in email_results.values() if success)
                self.logger.info(f"Sent {successful_sends}/{len(recipients)} emails successfully")
            
            results['success'] = True
            
        except Exception as e:
            error_msg = f"Error in generate_and_send_to_multiple_recipients: {str(e)}"
            self.logger.error(error_msg)
            results['errors'].append(error_msg)
        
        return results
    
    def get_topic_suggestions(self, industry: str, keywords: List[str] = None) -> List[str]:
        """
        Get topic suggestions for blog posts.
        
        Args:
            industry (str): Industry or field
            keywords (List[str]): Optional keywords
            
        Returns:
            List[str]: List of suggested topics
        """
        try:
            return self.blog_generator.get_topic_suggestions(industry, keywords)
        except Exception as e:
            self.logger.error(f"Error getting topic suggestions: {str(e)}")
            return []
    
    def _save_blog_to_file(self, blog_post: Dict[str, str], suffix: str = "") -> Path:
        """
        Save blog post to a file.
        
        Args:
            blog_post (Dict[str, str]): Blog post data
            suffix (str): Optional suffix for filename
            
        Returns:
            Path: Path to saved file
        """
        # Create filename based on title and timestamp
        title = blog_post.get('title', 'Untitled').replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_post_{title[:30]}{suffix}_{timestamp}.json"
        
        file_path = self.output_dir / filename
        
        # Save as JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(blog_post, f, indent=2, ensure_ascii=False)
        
        # Also save as readable text
        text_filename = filename.replace('.json', '.txt')
        text_path = self.output_dir / text_filename
        
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(f"TITLE: {blog_post.get('title', 'Untitled')}\n")
            f.write("="*50 + "\n\n")
            f.write(blog_post.get('content', 'No content'))
            f.write(f"\n\nHashtags: {blog_post.get('hashtags', '')}")
            f.write(f"\n\nCall to Action: {blog_post.get('call_to_action', '')}")
            f.write(f"\n\n---\nGenerated: {blog_post.get('generated_at', '')}")
        
        return file_path
    
    def run_interactive_mode(self):
        """
        Run the agent in interactive mode with a command-line interface.
        """
        print("🚀 LinkedIn Blog Agent - Interactive Mode")
        print("=" * 50)
        
        while True:
            try:
                print("\nOptions:")
                print("1. Generate single blog post")
                print("2. Generate multiple blog posts")
                print("3. Generate blog with dynamic recipients")
                print("4. Get topic suggestions")
                print("5. Test email connection")
                print("6. Exit")
                
                choice = input("\nSelect an option (1-6): ").strip()
                
                if choice == '1':
                    self._interactive_single_blog()
                elif choice == '2':
                    self._interactive_multiple_blogs()
                elif choice == '3':
                    self._interactive_dynamic_recipients()
                elif choice == '4':
                    self._interactive_topic_suggestions()
                elif choice == '5':
                    self._test_email_connection()
                elif choice == '6':
                    print("Goodbye! 👋")
                    break
                else:
                    print("Invalid option. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting... Goodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _interactive_single_blog(self):
        """Interactive mode for generating a single blog post."""
        print("\n📝 Generate Single Blog Post")
        print("-" * 30)
        
        topic = input("Enter blog topic: ").strip()
        if not topic:
            print("Topic is required!")
            return
        
        tone = input("Enter tone (professional/casual/inspirational) [professional]: ").strip() or "professional"
        length = input("Enter length (short/medium/long) [medium]: ").strip() or "medium"
        audience = input("Enter target audience [professionals]: ").strip() or "professionals"
        
        print(f"\n🤖 Generating blog post for: {topic}")
        
        results = self.generate_and_send_blog(
            topic=topic,
            tone=tone,
            length=length,
            target_audience=audience
        )
        
        if results['success']:
            print("✅ Blog post generated successfully!")
            
            if results.get('file_saved'):
                print(f"📁 Saved to: {results.get('file_path')}")
            
            if results['email_sent']:
                print("📧 Email sent successfully!")
            else:
                print("⚠️ Email sending failed")
            
            # Display the blog post
            blog_post = results['blog_post']
            print(f"\n📖 Generated Blog Post:")
            print(f"Title: {blog_post.get('title')}")
            print(f"Length: {len(blog_post.get('content', '').split())} words")
            
        else:
            print("❌ Failed to generate blog post")
            for error in results.get('errors', []):
                print(f"Error: {error}")
    
    def _interactive_multiple_blogs(self):
        """Interactive mode for generating multiple blog posts."""
        print("\n📝 Generate Multiple Blog Posts")
        print("-" * 35)
        
        topics_input = input("Enter topics (comma-separated): ").strip()
        if not topics_input:
            print("Topics are required!")
            return
        
        topics = [topic.strip() for topic in topics_input.split(',')]
        
        tone = input("Enter tone (professional/casual/inspirational) [professional]: ").strip() or "professional"
        length = input("Enter length (short/medium/long) [medium]: ").strip() or "medium"
        
        print(f"\n🤖 Generating {len(topics)} blog posts...")
        
        results = self.generate_multiple_blogs(
            topics=topics,
            tone=tone,
            length=length
        )
        
        if results['success']:
            print(f"✅ Generated {len(results['blog_posts'])} blog posts!")
            
            for i, post in enumerate(results['blog_posts'], 1):
                print(f"\n{i}. {post.get('title')}")
            
            successful_emails = sum(1 for success in results['email_results'].values() if success)
            print(f"\n📧 Successfully sent {successful_emails}/{len(results['email_results'])} emails")
            
        else:
            print("❌ Failed to generate blog posts")
            for error in results.get('errors', []):
                print(f"Error: {error}")
    
    def _interactive_dynamic_recipients(self):
        """Interactive mode for generating blog with dynamic recipients."""
        print("\n📧 Generate Blog with Dynamic Recipients")
        print("-" * 42)
        
        # Get blog details
        topic = input("Enter blog topic: ").strip()
        if not topic:
            print("Topic is required!")
            return
        
        tone = input("Enter tone (professional/casual/inspirational) [professional]: ").strip() or "professional"
        length = input("Enter length (short/medium/long) [medium]: ").strip() or "medium"
        audience = input("Enter target audience [professionals]: ").strip() or "professionals"
        
        # Get email recipients
        print("\n📧 Email Recipients Setup")
        print("Enter email addresses (one per line, empty line to finish):")
        
        recipients = []
        while True:
            email = input(f"Email {len(recipients)+1}: ").strip()
            if not email:
                break
            recipients.append(email)
        
        if not recipients:
            print("No email recipients provided!")
            return
        
        # Optional: Custom subject prefix
        subject_prefix = input(f"\nCustom subject prefix [Generated LinkedIn Blog Post]: ").strip()
        if not subject_prefix:
            subject_prefix = "Generated LinkedIn Blog Post"
        
        # Show recipients and validate
        print(f"\n📋 Recipients Summary:")
        for i, email in enumerate(recipients, 1):
            print(f"   {i}. {email}")
        
        confirm = input(f"\nSend to {len(recipients)} recipients? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled.")
            return
        
        print(f"\n🤖 Generating blog post: {topic}")
        print("📧 Validating emails and sending...")
        
        # Generate and send
        results = self.generate_and_send_to_multiple_recipients(
            topic=topic,
            recipients=recipients,
            tone=tone,
            length=length,
            target_audience=audience,
            subject_prefix=subject_prefix,
            validate_emails=True,
            save_to_file=True
        )
        
        # Display results
        if results['success']:
            print("✅ Blog post generated successfully!")
            
            blog_post = results['blog_post']
            print(f"\n📖 Generated: {blog_post.get('title')}")
            print(f"📝 Length: {len(blog_post.get('content', '').split())} words")
            
            if results.get('file_saved'):
                print(f"📁 Saved to: {results.get('file_path')}")
            
            # Email results
            email_results = results.get('email_results', {})
            if 'summary' in email_results:
                summary = email_results['summary']
                print(f"\n📧 Email Results:")
                print(f"   Total recipients: {summary['total_recipients']}")
                print(f"   Valid emails: {summary['valid_emails']}")
                print(f"   Invalid emails: {summary['invalid_emails']}")
                print(f"   Successfully sent: {summary['emails_sent']}")
                print(f"   Failed to send: {summary['emails_failed']}")
                
                # Show validation details if there were invalid emails
                if summary['invalid_emails'] > 0:
                    validation = results.get('validation_results', {})
                    invalid_emails = [email for email, valid in validation.items() if not valid]
                    print(f"\n⚠️  Invalid email addresses:")
                    for email in invalid_emails:
                        print(f"   ❌ {email}")
                
                # Show sending details
                if 'sending' in email_results:
                    sending_results = email_results['sending']
                    successful = [email for email, success in sending_results.items() if success]
                    failed = [email for email, success in sending_results.items() if not success]
                    
                    if successful:
                        print(f"\n✅ Successfully sent to:")
                        for email in successful:
                            print(f"   📧 {email}")
                    
                    if failed:
                        print(f"\n❌ Failed to send to:")
                        for email in failed:
                            print(f"   📧 {email}")
            
        else:
            print("❌ Failed to generate blog post or send emails")
            for error in results.get('errors', []):
                print(f"Error: {error}")
    
    def _interactive_topic_suggestions(self):
        """Interactive mode for getting topic suggestions."""
        print("\n💡 Get Topic Suggestions")
        print("-" * 25)
        
        industry = input("Enter industry/field: ").strip()
        if not industry:
            print("Industry is required!")
            return
        
        keywords_input = input("Enter keywords (comma-separated, optional): ").strip()
        keywords = [kw.strip() for kw in keywords_input.split(',')] if keywords_input else None
        
        print(f"\n🤖 Getting topic suggestions for {industry}...")
        
        topics = self.get_topic_suggestions(industry, keywords)
        
        if topics:
            print(f"\n📋 Suggested Topics for {industry}:")
            for i, topic in enumerate(topics, 1):
                print(f"{i}. {topic}")
        else:
            print("❌ Failed to get topic suggestions")
    
    def _test_email_connection(self):
        """Test email connection."""
        print("\n📧 Testing Email Connection")
        print("-" * 28)
        
        success = self.email_sender.test_connection()
        
        if success:
            print("✅ Email connection successful!")
        else:
            print("❌ Email connection failed. Please check your credentials in .env file.")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description="LinkedIn Blog Agent")
    parser.add_argument('--topic', type=str, help='Blog post topic')
    parser.add_argument('--tone', type=str, default='professional', help='Blog tone')
    parser.add_argument('--length', type=str, default='medium', help='Blog length')
    parser.add_argument('--audience', type=str, default='professionals', help='Target audience')
    parser.add_argument('--email', type=str, help='Recipient email')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    try:
        # Initialize agent
        agent = LinkedInBlogAgent()
        
        if args.interactive or not args.topic:
            # Run in interactive mode
            agent.run_interactive_mode()
        else:
            # Run with command-line arguments
            print(f"🤖 Generating blog post for: {args.topic}")
            
            results = agent.generate_and_send_blog(
                topic=args.topic,
                tone=args.tone,
                length=args.length,
                target_audience=args.audience,
                recipient_email=args.email
            )
            
            if results['success']:
                print("✅ Blog post generated and sent successfully!")
                print(f"Title: {results['blog_post'].get('title')}")
            else:
                print("❌ Failed to generate blog post")
                for error in results.get('errors', []):
                    print(f"Error: {error}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure you have set up your .env file with the required credentials.")


if __name__ == "__main__":
    main()