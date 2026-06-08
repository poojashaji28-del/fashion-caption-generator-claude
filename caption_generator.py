#!/usr/bin/env python3
"""
Fashion Instagram Caption Generator
Generates up to 10 unique captions using Claude AI
"""

import os
import json
from typing import List, Dict, Optional
import anthropic
import click


class CaptionGenerator:
    """Generate Instagram captions for fashion content"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the caption generator with API key"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "API key not found. Please set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def generate(
        self,
        topic: str,
        tone: str = 'sophisticated',
        style: str = 'trendy',
        audience: str = 'general',
        num_captions: int = 5,
        include_hashtags: bool = True,
        include_emojis: bool = True
    ) -> List[str]:
        """
        Generate Instagram captions
        
        Args:
            topic: The main topic/theme for captions (required)
            tone: Caption tone - 'sophisticated', 'playful', 'inspiring', 'casual', 'edgy'
            style: Caption style - 'trendy', 'minimalist', 'luxe', 'vintage', 'bold'
            audience: Target audience - 'general', 'luxury', 'Gen-Z', 'professionals', 'creators'
            num_captions: Number of captions to generate (1-10)
            include_hashtags: Whether to include hashtags
            include_emojis: Whether to include emojis
        
        Returns:
            List of generated captions
        """
        
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty")
        
        if not 1 <= num_captions <= 10:
            raise ValueError("Number of captions must be between 1 and 10")
        
        # Build the prompt
        prompt = f"""You are a professional Instagram caption writer specializing in fashion content.

Generate exactly {num_captions} unique and engaging Instagram captions based on these preferences:
- Topic/Theme: {topic}
- Tone: {tone}
- Style: {style}
- Target Audience: {audience}
- Include Hashtags: {'Yes, add 5-8 relevant hashtags' if include_hashtags else 'No hashtags'}
- Include Emojis: {'Yes, use 2-3 relevant emojis' if include_emojis else 'No emojis'}

Requirements:
- Each caption should be distinct and offer a different angle/perspective
- Captions should be engaging, authentic, and on-brand for fashion
- Keep each caption between 50-150 characters (excluding hashtags)
- Format: Return ONLY the captions, one per line, numbered 1-{num_captions}
- Do not include any preamble or explanation

Generate the captions now:"""

        try:
            message = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse the response
            response_text = message.content[0].text
            captions = [
                line.strip().lstrip('0123456789. ')
                for line in response_text.split('\n')
                if line.strip()
            ]
            
            # Remove any empty lines
            captions = [c for c in captions if c]
            
            # Limit to requested number
            captions = captions[:num_captions]
            
            if not captions:
                raise ValueError("No captions were generated. Please try again.")
            
            return captions
        
        except anthropic.APIError as e:
            raise RuntimeError(f"API Error: {str(e)}")


# CLI Interface
@click.group()
def cli():
    """Fashion Instagram Caption Generator"""
    pass


@cli.command()
@click.option(
    '--topic',
    prompt='What is your caption topic?',
    help='The main topic or theme for the captions'
)
@click.option(
    '--tone',
    type=click.Choice(['sophisticated', 'playful', 'inspiring', 'casual', 'edgy']),
    default='sophisticated',
    help='The tone of the captions'
)
@click.option(
    '--style',
    type=click.Choice(['trendy', 'minimalist', 'luxe', 'vintage', 'bold']),
    default='trendy',
    help='The style of the captions'
)
@click.option(
    '--audience',
    type=click.Choice(['general', 'luxury', 'Gen-Z', 'professionals', 'creators']),
    default='general',
    help='The target audience'
)
@click.option(
    '--count',
    type=click.IntRange(1, 10),
    default=5,
    help='Number of captions to generate (1-10)'
)
@click.option(
    '--hashtags/--no-hashtags',
    default=True,
    help='Include hashtags in captions'
)
@click.option(
    '--emojis/--no-emojis',
    default=True,
    help='Include emojis in captions'
)
def generate(topic, tone, style, audience, count, hashtags, emojis):
    """Generate Instagram captions with custom preferences"""
    
    try:
        generator = CaptionGenerator()
        
        click.echo("\n✨ Generating captions...\n")
        
        captions = generator.generate(
            topic=topic,
            tone=tone,
            style=style,
            audience=audience,
            num_captions=count,
            include_hashtags=hashtags,
            include_emojis=emojis
        )
        
        click.echo(f"📸 Generated {len(captions)} captions for: {topic}\n")
        click.echo("=" * 60)
        
        for i, caption in enumerate(captions, 1):
            click.echo(f"\n{i}. {caption}")
        
        click.echo("\n" + "=" * 60)
        click.echo(f"\n✅ Total: {len(captions)} captions created")
        
        # Option to save to file
        save_file = click.confirm("\nSave captions to file?", default=False)
        if save_file:
            filename = f"captions_{topic.lower().replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Instagram Captions for: {topic}\n")
                f.write(f"Generated with tone: {tone}, style: {style}\n")
                f.write("=" * 60 + "\n\n")
                for i, caption in enumerate(captions, 1):
                    f.write(f"{i}. {caption}\n\n")
            
            click.echo(f"✅ Captions saved to: {filename}")
    
    except ValueError as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
    except RuntimeError as e:
        click.echo(f"❌ {str(e)}", err=True)


@cli.command()
def interactive():
    """Start interactive mode for generating captions"""
    
    click.clear()
    click.echo("🎀 Fashion Instagram Caption Generator - Interactive Mode")
    click.echo("=" * 60)
    
    try:
        # Get preferences
        topic = click.prompt("📝 What is your caption topic?")
        
        click.echo("\n🎯 Select tone:")
        tones = ['sophisticated', 'playful', 'inspiring', 'casual', 'edgy']
        for i, tone in enumerate(tones, 1):
            click.echo(f"  {i}. {tone}")
        tone_choice = click.prompt("Choose", type=click.IntRange(1, len(tones))) - 1
        tone = tones[tone_choice]
        
        click.echo("\n🎨 Select style:")
        styles = ['trendy', 'minimalist', 'luxe', 'vintage', 'bold']
        for i, style in enumerate(styles, 1):
            click.echo(f"  {i}. {style}")
        style_choice = click.prompt("Choose", type=click.IntRange(1, len(styles))) - 1
        style = styles[style_choice]
        
        click.echo("\n👥 Select audience:")
        audiences = ['general', 'luxury', 'Gen-Z', 'professionals', 'creators']
        for i, audience in enumerate(audiences, 1):
            click.echo(f"  {i}. {audience}")
        audience_choice = click.prompt("Choose", type=click.IntRange(1, len(audiences))) - 1
        audience = audiences[audience_choice]
        
        num_captions = click.prompt(
            "\n📊 How many captions?",
            type=click.IntRange(1, 10),
            default=5
        )
        
        hashtags = click.confirm("\n#️⃣ Include hashtags?", default=True)
        emojis = click.confirm("😊 Include emojis?", default=True)
        
        # Generate
        generator = CaptionGenerator()
        click.echo("\n✨ Generating captions...\n")
        
        captions = generator.generate(
            topic=topic,
            tone=tone,
            style=style,
            audience=audience,
            num_captions=num_captions,
            include_hashtags=hashtags,
            include_emojis=emojis
        )
        
        click.echo("=" * 60)
        for i, caption in enumerate(captions, 1):
            click.echo(f"\n{i}. {caption}")
        click.echo("\n" + "=" * 60)
        
    except KeyboardInterrupt:
        click.echo("\n\n👋 Goodbye!")
    except ValueError as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
    except RuntimeError as e:
        click.echo(f"\n❌ {str(e)}", err=True)


if __name__ == '__main__':
    cli()
