import re
import random
from typing import List, Dict, Any
import time

class NLPService:
    """Service for Natural Language Processing tasks"""
    
    def __init__(self):
        self.supported_languages = ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa']
        self.entity_types = ['PERSON', 'ORGANIZATION', 'LOCATION', 'DATE', 'MONEY', 'PERCENT']
        self.sentiment_labels = ['positive', 'negative', 'neutral']
    
    def analyze_sentiment(self, text: str, language: str = 'en') -> Dict[str, Any]:
        """
        Analyze sentiment of the given text
        
        Args:
            text: Text to analyze
            language: Language of the text
            
        Returns:
            Sentiment analysis results
        """
        # Mock sentiment analysis
        time.sleep(random.uniform(0.1, 0.5))
        
        # Simple keyword-based sentiment (in real system, would use ML models)
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'sad', 'angry', 'disappointing']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = round(random.uniform(0.6, 0.9), 2)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = round(random.uniform(0.6, 0.9), 2)
        else:
            sentiment = 'neutral'
            confidence = round(random.uniform(0.5, 0.8), 2)
        
        return {
            'text': text,
            'language': language,
            'sentiment': sentiment,
            'confidence': confidence,
            'scores': {
                'positive': round(random.uniform(0.1, 0.8), 2),
                'negative': round(random.uniform(0.1, 0.6), 2),
                'neutral': round(random.uniform(0.2, 0.7), 2)
            },
            'emotions': {
                'joy': round(random.uniform(0.1, 0.6), 2),
                'sadness': round(random.uniform(0.05, 0.4), 2),
                'anger': round(random.uniform(0.02, 0.3), 2),
                'fear': round(random.uniform(0.01, 0.2), 2),
                'surprise': round(random.uniform(0.01, 0.3), 2),
                'disgust': round(random.uniform(0.01, 0.2), 2)
            },
            'analysis_metadata': {
                'processing_time': round(random.uniform(0.1, 0.5), 2),
                'model_version': 'v1.2.0',
                'analysis_timestamp': '2024-01-15T10:30:00Z'
            }
        }
    
    def extract_entities(self, text: str, language: str = 'en') -> Dict[str, Any]:
        """
        Extract named entities from text
        
        Args:
            text: Text to analyze
            language: Language of the text
            
        Returns:
            Extracted entities
        """
        # Mock entity extraction
        time.sleep(random.uniform(0.2, 0.8))
        
        entities = []
        
        # Simple regex-based entity extraction (in real system, would use NER models)
        # Person names (capitalized words)
        person_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        persons = re.findall(person_pattern, text)
        for person in persons[:3]:  # Limit to 3 persons
            entities.append({
                'text': person,
                'type': 'PERSON',
                'confidence': round(random.uniform(0.7, 0.95), 2),
                'start': text.find(person),
                'end': text.find(person) + len(person)
            })
        
        # Organizations (words ending with Corp, Inc, Ltd, etc.)
        org_pattern = r'\b[A-Z][a-zA-Z\s]+(?:Corp|Inc|Ltd|LLC|Company|Organization)\b'
        organizations = re.findall(org_pattern, text)
        for org in organizations[:2]:  # Limit to 2 organizations
            entities.append({
                'text': org,
                'type': 'ORGANIZATION',
                'confidence': round(random.uniform(0.6, 0.9), 2),
                'start': text.find(org),
                'end': text.find(org) + len(org)
            })
        
        # Locations (cities, countries)
        locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'India', 'USA', 'UK']
        for location in locations:
            if location in text:
                entities.append({
                    'text': location,
                    'type': 'LOCATION',
                    'confidence': round(random.uniform(0.8, 0.98), 2),
                    'start': text.find(location),
                    'end': text.find(location) + len(location)
                })
        
        # Dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b'
        dates = re.findall(date_pattern, text)
        for date in dates[:2]:  # Limit to 2 dates
            entities.append({
                'text': date,
                'type': 'DATE',
                'confidence': round(random.uniform(0.9, 0.99), 2),
                'start': text.find(date),
                'end': text.find(date) + len(date)
            })
        
        # Money amounts
        money_pattern = r'\$\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars|rupees|USD|INR)'
        money_amounts = re.findall(money_pattern, text)
        for money in money_amounts[:2]:  # Limit to 2 amounts
            entities.append({
                'text': money,
                'type': 'MONEY',
                'confidence': round(random.uniform(0.8, 0.95), 2),
                'start': text.find(money),
                'end': text.find(money) + len(money)
            })
        
        return {
            'text': text,
            'language': language,
            'entities': entities,
            'entity_count': len(entities),
            'entity_types': list(set(entity['type'] for entity in entities)),
            'analysis_metadata': {
                'processing_time': round(random.uniform(0.2, 0.8), 2),
                'model_version': 'v1.3.0',
                'analysis_timestamp': '2024-01-15T10:30:00Z'
            }
        }
    
    def extract_keywords(self, text: str, language: str = 'en', max_keywords: int = 10) -> Dict[str, Any]:
        """
        Extract keywords from text
        
        Args:
            text: Text to analyze
            language: Language of the text
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            Extracted keywords with scores
        """
        # Mock keyword extraction
        time.sleep(random.uniform(0.1, 0.4))
        
        # Simple keyword extraction (in real system, would use TF-IDF or ML models)
        # Remove common stop words
        stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']
        
        # Tokenize and clean text
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and get top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = []
        
        for word, freq in sorted_words[:max_keywords]:
            # Calculate TF-IDF like score (simplified)
            score = round(freq / len(words) * random.uniform(0.5, 1.0), 3)
            keywords.append({
                'keyword': word,
                'frequency': freq,
                'score': score,
                'importance': 'high' if score > 0.1 else 'medium' if score > 0.05 else 'low'
            })
        
        return {
            'text': text,
            'language': language,
            'keywords': keywords,
            'keyword_count': len(keywords),
            'text_length': len(text),
            'unique_words': len(set(words)),
            'analysis_metadata': {
                'processing_time': round(random.uniform(0.1, 0.4), 2),
                'model_version': 'v1.1.0',
                'analysis_timestamp': '2024-01-15T10:30:00Z'
            }
        }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language detection results
        """
        # Mock language detection
        time.sleep(random.uniform(0.1, 0.3))
        
        # Simple language detection based on character patterns
        languages = {
            'en': {
                'name': 'English',
                'confidence': round(random.uniform(0.8, 0.98), 2),
                'character_patterns': 'Latin script'
            },
            'hi': {
                'name': 'Hindi',
                'confidence': round(random.uniform(0.7, 0.95), 2),
                'character_patterns': 'Devanagari script'
            },
            'ta': {
                'name': 'Tamil',
                'confidence': round(random.uniform(0.7, 0.95), 2),
                'character_patterns': 'Tamil script'
            },
            'te': {
                'name': 'Telugu',
                'confidence': round(random.uniform(0.7, 0.95), 2),
                'character_patterns': 'Telugu script'
            },
            'bn': {
                'name': 'Bengali',
                'confidence': round(random.uniform(0.7, 0.95), 2),
                'character_patterns': 'Bengali script'
            }
        }
        
        # Mock detection (in real system, would use language detection models)
        detected_lang = random.choice(list(languages.keys()))
        lang_info = languages[detected_lang]
        
        return {
            'text': text,
            'detected_language': {
                'code': detected_lang,
                'name': lang_info['name'],
                'confidence': lang_info['confidence']
            },
            'alternative_languages': [
                {
                    'code': lang,
                    'name': info['name'],
                    'confidence': round(random.uniform(0.1, 0.5), 2)
                }
                for lang, info in languages.items()
                if lang != detected_lang
            ][:3],
            'analysis_metadata': {
                'processing_time': round(random.uniform(0.1, 0.3), 2),
                'model_version': 'v1.0.0',
                'analysis_timestamp': '2024-01-15T10:30:00Z'
            }
        }
    
    def summarize_text(self, text: str, max_length: int = 200, language: str = 'en') -> Dict[str, Any]:
        """
        Generate a summary of the given text
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            language: Language of the text
            
        Returns:
            Text summary
        """
        # Mock text summarization
        time.sleep(random.uniform(0.3, 1.0))
        
        # Simple extractive summarization (in real system, would use ML models)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Score sentences based on word frequency
        word_freq = {}
        for sentence in sentences:
            words = re.findall(r'\b[a-zA-Z]+\b', sentence.lower())
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score each sentence
        sentence_scores = []
        for sentence in sentences:
            words = re.findall(r'\b[a-zA-Z]+\b', sentence.lower())
            score = sum(word_freq.get(word, 0) for word in words) / len(words) if words else 0
            sentence_scores.append((sentence, score))
        
        # Get top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        summary_sentences = []
        current_length = 0
        
        for sentence, score in sentence_scores:
            if current_length + len(sentence) <= max_length:
                summary_sentences.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        summary = '. '.join(summary_sentences) + '.'
        
        return {
            'original_text': text,
            'summary': summary,
            'language': language,
            'summary_length': len(summary),
            'original_length': len(text),
            'compression_ratio': round(len(summary) / len(text), 2),
            'sentence_count': len(summary_sentences),
            'analysis_metadata': {
                'processing_time': round(random.uniform(0.3, 1.0), 2),
                'model_version': 'v1.4.0',
                'analysis_timestamp': '2024-01-15T10:30:00Z'
            }
        }
    
    def classify_text(self, text: str, categories: List[str] = None, language: str = 'en') -> Dict[str, Any]:
        """
        Classify text into predefined categories
        
        Args:
            text: Text to classify
            categories: List of possible categories
            language: Language of the text
            
        Returns:
            Classification results
        """
        # Mock text classification
        time.sleep(random.uniform(0.2, 0.6))
        
        if categories is None:
            categories = ['technology', 'politics', 'sports', 'entertainment', 'business', 'health', 'education']
        
        # Simple keyword-based classification (in real system, would use ML models)
        category_keywords = {
            'technology': ['tech', 'software', 'computer', 'digital', 'ai', 'machine learning'],
            'politics': ['government', 'election', 'policy', 'minister', 'parliament'],
            'sports': ['game', 'match', 'player', 'team', 'championship', 'tournament'],
            'entertainment': ['movie', 'film', 'actor', 'actress', 'music', 'concert'],
            'business': ['company', 'business', 'market', 'investment', 'finance'],
            'health': ['health', 'medical', 'doctor', 'hospital', 'disease', 'treatment'],
            'education': ['school', 'university', 'student', 'education', 'learning', 'course']
        }
        
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in category_keywords.items():
            if category in categories:
                score = sum(1 for keyword in keywords if keyword in text_lower)
                category_scores[category] = score
        
        # Get top category
        if category_scores:
            top_category = max(category_scores, key=category_scores.get)
            confidence = round(random.uniform(0.6, 0.95), 2) if category_scores[top_category] > 0 else round(random.uniform(0.3, 0.6), 2)
        else:
            top_category = random.choice(categories)
            confidence = round(random.uniform(0.3, 0.6), 2)
        
        return {
            'text': text,
            'language': language,
            'classification': {
                'primary_category': top_category,
                'confidence': confidence,
                'all_scores': {
                    category: round(score / max(category_scores.values()) if category_scores.values() else 0, 2)
                    for category, score in category_scores.items()
                }
            },
            'analysis_metadata': {
                'processing_time': round(random.uniform(0.2, 0.6), 2),
                'model_version': 'v1.5.0',
                'analysis_timestamp': '2024-01-15T10:30:00Z'
            }
        } 