import re
import nltk
from typing import Dict, List, Any
from collections import Counter
import json

class NLPService:
    """Service for Natural Language Processing tasks"""
    
    def __init__(self):
        # Download required NLTK data (in a real app, this would be done during setup)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        
        # Initialize stop words
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        
        # Add Indian language stop words (basic)
        self.indian_stop_words = {
            'hindi': ['है', 'में', 'की', 'के', 'और', 'से', 'पर', 'नहीं', 'यह', 'वह', 'क्या', 'कौन', 'कहाँ', 'कब', 'कैसे'],
            'bengali': ['হয়', 'মধ্যে', 'এর', 'এবং', 'থেকে', 'পরে', 'না', 'এই', 'সে', 'কি', 'কে', 'কোথায়', 'কখন', 'কিভাবে'],
            'tamil': ['ஆகும்', 'இல்', 'இன்', 'மற்றும்', 'இருந்து', 'பிறகு', 'இல்லை', 'இது', 'அது', 'என்ன', 'யார்', 'எங்கே', 'எப்போது', 'எப்படி'],
            'telugu': ['అవుతుంది', 'లో', 'యొక్క', 'మరియు', 'నుండి', 'తర్వాత', 'లేదు', 'ఇది', 'అది', 'ఏమి', 'ఎవరు', 'ఎక్కడ', 'ఎప్పుడు', 'ఎలా'],
            'marathi': ['आहे', 'मध्ये', 'ची', 'आणि', 'पासून', 'नंतर', 'नाही', 'हे', 'ते', 'काय', 'कोण', 'कुठे', 'कधी', 'कसे']
        }
    
    def analyze_sentiment(self, text: str, language: str = 'en') -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Tokenize
            tokens = nltk.word_tokenize(cleaned_text)
            
            # Remove stop words
            if language == 'en':
                filtered_tokens = [word for word in tokens if word.lower() not in self.stop_words]
            else:
                indian_stops = self.indian_stop_words.get(language, [])
                filtered_tokens = [word for word in tokens if word.lower() not in indian_stops]
            
            # Calculate sentiment scores (mock implementation)
            # In a real implementation, you'd use a pre-trained sentiment analysis model
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'like']
            negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'disappointed']
            
            positive_count = sum(1 for word in filtered_tokens if word.lower() in positive_words)
            negative_count = sum(1 for word in filtered_tokens if word.lower() in negative_words)
            total_words = len(filtered_tokens)
            
            if total_words == 0:
                sentiment_score = 0.0
            else:
                sentiment_score = (positive_count - negative_count) / total_words
            
            # Determine sentiment
            if sentiment_score > 0.1:
                sentiment = 'positive'
                confidence = min(0.9, abs(sentiment_score) + 0.5)
            elif sentiment_score < -0.1:
                sentiment = 'negative'
                confidence = min(0.9, abs(sentiment_score) + 0.5)
            else:
                sentiment = 'neutral'
                confidence = 0.7
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'score': sentiment_score,
                'positive_words': positive_count,
                'negative_words': negative_count,
                'total_words': total_words,
                'language': language
            }
            
        except Exception as e:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'score': 0.0,
                'error': str(e),
                'language': language
            }
    
    def extract_entities(self, text: str, language: str = 'en') -> Dict[str, Any]:
        """Extract named entities from text"""
        try:
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Tokenize and tag
            tokens = nltk.word_tokenize(cleaned_text)
            tagged = nltk.pos_tag(tokens)
            
            # Extract entities (mock implementation)
            # In a real implementation, you'd use NER models or spaCy
            entities = {
                'persons': [],
                'organizations': [],
                'locations': [],
                'dates': [],
                'emails': [],
                'phones': [],
                'urls': []
            }
            
            # Extract emails
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            entities['emails'] = emails
            
            # Extract phone numbers
            phone_pattern = r'(\+?[\d\s\-\(\)]{10,})'
            phones = re.findall(phone_pattern, text)
            entities['phones'] = phones
            
            # Extract URLs
            url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
            urls = re.findall(url_pattern, text)
            entities['urls'] = urls
            
            # Extract dates
            date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'
            dates = re.findall(date_pattern, text)
            entities['dates'] = dates
            
            # Mock entity extraction for persons, organizations, locations
            # In a real implementation, you'd use NER models
            words = text.split()
            for word in words:
                if word.istitle() and len(word) > 2:
                    if word.endswith(('Corp', 'Inc', 'Ltd', 'LLC', 'Company')):
                        entities['organizations'].append(word)
                    elif word in ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune']:
                        entities['locations'].append(word)
                    else:
                        entities['persons'].append(word)
            
            return {
                'entities': entities,
                'total_entities': sum(len(entity_list) for entity_list in entities.values()),
                'language': language
            }
            
        except Exception as e:
            return {
                'entities': {},
                'total_entities': 0,
                'error': str(e),
                'language': language
            }
    
    def extract_keywords(self, text: str, language: str = 'en', max_keywords: int = 10) -> List[Dict[str, Any]]:
        """Extract keywords from text"""
        try:
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Tokenize
            tokens = nltk.word_tokenize(cleaned_text)
            
            # Remove stop words
            if language == 'en':
                filtered_tokens = [word.lower() for word in tokens if word.lower() not in self.stop_words and word.isalpha()]
            else:
                indian_stops = self.indian_stop_words.get(language, [])
                filtered_tokens = [word.lower() for word in tokens if word.lower() not in indian_stops and word.isalpha()]
            
            # Count frequencies
            word_freq = Counter(filtered_tokens)
            
            # Get top keywords
            keywords = []
            for word, freq in word_freq.most_common(max_keywords):
                keywords.append({
                    'keyword': word,
                    'frequency': freq,
                    'score': freq / len(filtered_tokens) if filtered_tokens else 0
                })
            
            return keywords
            
        except Exception as e:
            return []
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of text"""
        try:
            # Simple language detection based on character sets
            # In a real implementation, you'd use a proper language detection library
            
            # Check for Indian scripts
            devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
            bengali_chars = len(re.findall(r'[\u0980-\u09FF]', text))
            tamil_chars = len(re.findall(r'[\u0B80-\u0BFF]', text))
            telugu_chars = len(re.findall(r'[\u0C00-\u0C7F]', text))
            marathi_chars = len(re.findall(r'[\u0C80-\u0CFF]', text))
            
            total_chars = len(text)
            
            if total_chars == 0:
                return {'language': 'unknown', 'confidence': 0.0}
            
            # Calculate percentages
            devanagari_ratio = devanagari_chars / total_chars
            bengali_ratio = bengali_chars / total_chars
            tamil_ratio = tamil_chars / total_chars
            telugu_ratio = telugu_chars / total_chars
            marathi_ratio = marathi_chars / total_chars
            
            # Determine language
            ratios = [
                ('hindi', devanagari_ratio),
                ('bengali', bengali_ratio),
                ('tamil', tamil_ratio),
                ('telugu', telugu_ratio),
                ('marathi', marathi_ratio)
            ]
            
            max_ratio = max(ratios, key=lambda x: x[1])
            
            if max_ratio[1] > 0.1:  # More than 10% of characters
                return {
                    'language': max_ratio[0],
                    'confidence': min(0.9, max_ratio[1] + 0.5),
                    'alternatives': [lang for lang, ratio in ratios if ratio > 0.05]
                }
            else:
                return {
                    'language': 'en',
                    'confidence': 0.8,
                    'alternatives': []
                }
                
        except Exception as e:
            return {
                'language': 'unknown',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> Dict[str, Any]:
        """Generate text summary"""
        try:
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Split into sentences
            sentences = nltk.sent_tokenize(cleaned_text)
            
            if len(sentences) <= max_sentences:
                return {
                    'summary': text,
                    'original_length': len(text),
                    'summary_length': len(text),
                    'compression_ratio': 1.0,
                    'sentences_used': len(sentences)
                }
            
            # Simple extractive summarization (mock)
            # In a real implementation, you'd use more sophisticated algorithms
            keywords = self.extract_keywords(text, max_keywords=20)
            keyword_set = set(kw['keyword'] for kw in keywords)
            
            # Score sentences based on keyword presence
            sentence_scores = []
            for sentence in sentences:
                sentence_words = set(nltk.word_tokenize(sentence.lower()))
                score = len(sentence_words.intersection(keyword_set))
                sentence_scores.append((sentence, score))
            
            # Sort by score and take top sentences
            sentence_scores.sort(key=lambda x: x[1], reverse=True)
            top_sentences = [sentence for sentence, score in sentence_scores[:max_sentences]]
            
            # Sort by original order
            summary = ' '.join(sorted(top_sentences, key=lambda x: sentences.index(x)))
            
            return {
                'summary': summary,
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': len(summary) / len(text),
                'sentences_used': len(top_sentences)
            }
            
        except Exception as e:
            return {
                'summary': text,
                'original_length': len(text),
                'summary_length': len(text),
                'compression_ratio': 1.0,
                'error': str(e)
            }
    
    def analyze_text_complexity(self, text: str) -> Dict[str, Any]:
        """Analyze text complexity"""
        try:
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Tokenize
            tokens = nltk.word_tokenize(cleaned_text)
            sentences = nltk.sent_tokenize(cleaned_text)
            
            # Calculate metrics
            word_count = len(tokens)
            sentence_count = len(sentences)
            unique_words = len(set(tokens))
            
            # Average sentence length
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            # Lexical diversity (type-token ratio)
            lexical_diversity = unique_words / word_count if word_count > 0 else 0
            
            # Average word length
            avg_word_length = sum(len(word) for word in tokens) / word_count if word_count > 0 else 0
            
            # Determine complexity level
            if avg_sentence_length > 20 or lexical_diversity > 0.8:
                complexity = 'high'
            elif avg_sentence_length > 15 or lexical_diversity > 0.6:
                complexity = 'medium'
            else:
                complexity = 'low'
            
            return {
                'word_count': word_count,
                'sentence_count': sentence_count,
                'unique_words': unique_words,
                'avg_sentence_length': avg_sentence_length,
                'lexical_diversity': lexical_diversity,
                'avg_word_length': avg_word_length,
                'complexity_level': complexity,
                'readability_score': self._calculate_readability(text)
            }
            
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        return text
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate Flesch Reading Ease score"""
        try:
            sentences = nltk.sent_tokenize(text)
            words = nltk.word_tokenize(text)
            syllables = sum(self._count_syllables(word) for word in words)
            
            if len(sentences) == 0 or len(words) == 0:
                return 0.0
            
            # Flesch Reading Ease formula
            score = 206.835 - (1.015 * (len(words) / len(sentences))) - (84.6 * (syllables / len(words)))
            
            return max(0.0, min(100.0, score))
            
        except Exception:
            return 50.0  # Default middle score
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        if word.endswith('e'):
            count -= 1
        
        return max(1, count) 