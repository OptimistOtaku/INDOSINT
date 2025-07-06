import requests
import json
from typing import List, Dict, Any
import time
import random
import re

class TranslationService:
    """Service for text translation between languages"""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'ur': 'Urdu',
            'or': 'Odia',
            'as': 'Assamese',
            'ne': 'Nepali',
            'si': 'Sinhala',
            'my': 'Myanmar',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay'
        }
        
        # Mock translation dictionaries for common phrases
        self.translation_dict = {
            'en-hi': {
                'hello': 'नमस्ते',
                'how are you': 'आप कैसे हैं',
                'thank you': 'धन्यवाद',
                'good morning': 'सुप्रभात',
                'good night': 'शुभ रात्रि',
                'welcome': 'स्वागत है',
                'please': 'कृपया',
                'sorry': 'माफ़ कीजिए',
                'yes': 'हाँ',
                'no': 'नहीं'
            },
            'en-ta': {
                'hello': 'வணக்கம்',
                'how are you': 'நீங்கள் எப்படி இருக்கிறீர்கள்',
                'thank you': 'நன்றி',
                'good morning': 'காலை வணக்கம்',
                'good night': 'இரவு வணக்கம்',
                'welcome': 'வரவேற்கிறோம்',
                'please': 'தயவுசெய்து',
                'sorry': 'மன்னிக்கவும்',
                'yes': 'ஆம்',
                'no': 'இல்லை'
            },
            'en-te': {
                'hello': 'నమస్కారం',
                'how are you': 'మీరు ఎలా ఉన్నారు',
                'thank you': 'ధన్యవాదాలు',
                'good morning': 'శుభోదయం',
                'good night': 'శుభ రాత్రి',
                'welcome': 'స్వాగతం',
                'please': 'దయచేసి',
                'sorry': 'క్షమించండి',
                'yes': 'అవును',
                'no': 'లేదు'
            }
        }
    
    def translate(self, text: str, source_language: str = 'auto', target_language: str = 'en') -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_language: Source language code (or 'auto' for auto-detection)
            target_language: Target language code
            
        Returns:
            Translated text
        """
        # Mock translation
        time.sleep(random.uniform(0.2, 0.8))
        
        # Validate languages
        if target_language not in self.supported_languages:
            raise ValueError(f"Unsupported target language: {target_language}")
        
        # Auto-detect source language if needed
        if source_language == 'auto':
            source_language = self._detect_language(text)
        
        if source_language not in self.supported_languages:
            raise ValueError(f"Unsupported source language: {source_language}")
        
        # Check if it's the same language
        if source_language == target_language:
            return text
        
        # Try to find translation in dictionary
        dict_key = f"{source_language}-{target_language}"
        if dict_key in self.translation_dict:
            for eng_phrase, translated_phrase in self.translation_dict[dict_key].items():
                if text.lower() == eng_phrase:
                    return translated_phrase
        
        # Mock translation for other text
        return self._mock_translate(text, source_language, target_language)
    
    def _detect_language(self, text: str) -> str:
        """Detect the language of the text"""
        # Simple language detection based on character patterns
        if re.search(r'[\u0900-\u097F]', text):  # Devanagari
            return 'hi'
        elif re.search(r'[\u0B80-\u0BFF]', text):  # Tamil
            return 'ta'
        elif re.search(r'[\u0C00-\u0C7F]', text):  # Telugu
            return 'te'
        elif re.search(r'[\u0980-\u09FF]', text):  # Bengali
            return 'bn'
        else:
            return 'en'  # Default to English
    
    def _mock_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Mock translation for demonstration purposes"""
        # Generate mock translations based on language pairs
        if source_lang == 'en' and target_lang == 'hi':
            # English to Hindi mock translations
            translations = {
                'hello world': 'नमस्ते दुनिया',
                'good morning': 'सुप्रभात',
                'how are you': 'आप कैसे हैं',
                'thank you': 'धन्यवाद',
                'welcome': 'स्वागत है',
                'please help me': 'कृपया मेरी मदद करें',
                'i love you': 'मैं आपसे प्यार करता हूं',
                'goodbye': 'अलविदा',
                'see you later': 'फिर मिलेंगे',
                'have a nice day': 'आपका दिन शुभ हो'
            }
        elif source_lang == 'en' and target_lang == 'ta':
            # English to Tamil mock translations
            translations = {
                'hello world': 'வணக்கம் உலகம்',
                'good morning': 'காலை வணக்கம்',
                'how are you': 'நீங்கள் எப்படி இருக்கிறீர்கள்',
                'thank you': 'நன்றி',
                'welcome': 'வரவேற்கிறோம்',
                'please help me': 'தயவுசெய்து எனக்கு உதவுங்கள்',
                'i love you': 'நான் உன்னை காதலிக்கிறேன்',
                'goodbye': 'பிரியாவிடை',
                'see you later': 'பின்னர் சந்திப்போம்',
                'have a nice day': 'நல்ல நாள் கிடைக்கட்டும்'
            }
        elif source_lang == 'en' and target_lang == 'te':
            # English to Telugu mock translations
            translations = {
                'hello world': 'నమస్కారం ప్రపంచం',
                'good morning': 'శుభోదయం',
                'how are you': 'మీరు ఎలా ఉన్నారు',
                'thank you': 'ధన్యవాదాలు',
                'welcome': 'స్వాగతం',
                'please help me': 'దయచేసి నాకు సహాయం చేయండి',
                'i love you': 'నేను మిమ్మల్ని ప్రేమిస్తున్నాను',
                'goodbye': 'వీడ్కోలు',
                'see you later': 'తర్వాత కలుద్దాం',
                'have a nice day': 'మంచి రోజు కలగాలని కోరుకుంటున్నాను'
            }
        else:
            # Generic mock translation
            translations = {}
        
        # Try to find exact match
        text_lower = text.lower()
        if text_lower in translations:
            return translations[text_lower]
        
        # Generate mock translation based on language
        if target_lang == 'hi':
            return f"[Hindi Translation] {text}"
        elif target_lang == 'ta':
            return f"[Tamil Translation] {text}"
        elif target_lang == 'te':
            return f"[Telugu Translation] {text}"
        elif target_lang == 'bn':
            return f"[Bengali Translation] {text}"
        else:
            return f"[{self.supported_languages.get(target_lang, target_lang)} Translation] {text}"
    
    def translate_batch(self, texts: List[str], source_language: str = 'auto', target_language: str = 'en') -> List[str]:
        """
        Translate multiple texts at once
        
        Args:
            texts: List of texts to translate
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            List of translated texts
        """
        # Mock batch translation
        time.sleep(random.uniform(0.5, 1.5))
        
        translated_texts = []
        for text in texts:
            try:
                translated = self.translate(text, source_language, target_language)
                translated_texts.append(translated)
            except Exception as e:
                # Return original text if translation fails
                translated_texts.append(text)
        
        return translated_texts
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        
        Returns:
            Dictionary of language codes and names
        """
        return self.supported_languages.copy()
    
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
        
        detected_lang = self._detect_language(text)
        
        return {
            'text': text,
            'detected_language': {
                'code': detected_lang,
                'name': self.supported_languages.get(detected_lang, 'Unknown'),
                'confidence': round(random.uniform(0.7, 0.95), 2)
            },
            'alternative_languages': [
                {
                    'code': lang,
                    'name': name,
                    'confidence': round(random.uniform(0.1, 0.5), 2)
                }
                for lang, name in self.supported_languages.items()
                if lang != detected_lang
            ][:3],
            'analysis_metadata': {
                'processing_time': round(random.uniform(0.1, 0.3), 2),
                'model_version': 'v1.0.0',
                'analysis_timestamp': '2024-01-15T10:30:00Z'
            }
        }
    
    def get_translation_quality(self, original_text: str, translated_text: str, source_language: str, target_language: str) -> Dict[str, Any]:
        """
        Assess the quality of a translation
        
        Args:
            original_text: Original text
            translated_text: Translated text
            source_language: Source language
            target_language: Target language
            
        Returns:
            Translation quality assessment
        """
        # Mock quality assessment
        time.sleep(random.uniform(0.2, 0.6))
        
        # Simple quality metrics (in real system, would use more sophisticated methods)
        fluency_score = round(random.uniform(0.6, 0.95), 2)
        accuracy_score = round(random.uniform(0.7, 0.98), 2)
        adequacy_score = round(random.uniform(0.65, 0.92), 2)
        
        overall_score = round((fluency_score + accuracy_score + adequacy_score) / 3, 2)
        
        quality_level = 'excellent' if overall_score > 0.9 else 'good' if overall_score > 0.7 else 'fair' if overall_score > 0.5 else 'poor'
        
        return {
            'original_text': original_text,
            'translated_text': translated_text,
            'source_language': source_language,
            'target_language': target_language,
            'quality_scores': {
                'fluency': fluency_score,
                'accuracy': accuracy_score,
                'adequacy': adequacy_score,
                'overall': overall_score
            },
            'quality_level': quality_level,
            'issues': [
                'Minor grammatical errors' if fluency_score < 0.8 else None,
                'Some meaning loss' if accuracy_score < 0.85 else None,
                'Incomplete translation' if adequacy_score < 0.8 else None
            ],
            'suggestions': [
                'Consider professional review' if overall_score < 0.8 else 'Translation quality is good',
                'Check for cultural nuances' if accuracy_score < 0.9 else None,
                'Verify technical terms' if adequacy_score < 0.85 else None
            ],
            'analysis_metadata': {
                'processing_time': round(random.uniform(0.2, 0.6), 2),
                'model_version': 'v1.1.0',
                'analysis_timestamp': '2024-01-15T10:30:00Z'
            }
        }
    
    def translate_with_context(self, text: str, context: str, source_language: str = 'auto', target_language: str = 'en') -> str:
        """
        Translate text with additional context
        
        Args:
            text: Text to translate
            context: Additional context for better translation
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            Context-aware translated text
        """
        # Mock context-aware translation
        time.sleep(random.uniform(0.3, 1.0))
        
        # In a real system, this would use context to improve translation quality
        base_translation = self.translate(text, source_language, target_language)
        
        # Add context indicator
        return f"[Context: {context[:50]}...] {base_translation}"
    
    def get_translation_memory(self, source_language: str, target_language: str) -> Dict[str, Any]:
        """
        Get translation memory for a language pair
        
        Args:
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            Translation memory data
        """
        # Mock translation memory
        time.sleep(random.uniform(0.1, 0.3))
        
        dict_key = f"{source_language}-{target_language}"
        memory_entries = self.translation_dict.get(dict_key, {})
        
        return {
            'source_language': source_language,
            'target_language': target_language,
            'memory_entries': len(memory_entries),
            'entries': [
                {
                    'source': source,
                    'target': target,
                    'usage_count': random.randint(1, 100),
                    'last_used': '2024-01-15T10:30:00Z'
                }
                for source, target in memory_entries.items()
            ],
            'metadata': {
                'created_date': '2024-01-01T00:00:00Z',
                'last_updated': '2024-01-15T10:30:00Z',
                'version': '1.0.0'
            }
        } 