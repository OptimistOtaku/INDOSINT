import requests
import json
from typing import Dict, List, Any
import re

class TranslationService:
    """Service for text translation and language processing"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Supported languages
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'te': 'Telugu',
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
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'pt': 'Portuguese',
            'it': 'Italian',
            'ru': 'Russian'
        }
        
        # Language families for better translation routing
        self.language_families = {
            'indo_aryan': ['hi', 'bn', 'gu', 'mr', 'pa', 'ur', 'or', 'as', 'ne'],
            'dravidian': ['ta', 'te', 'kn', 'ml'],
            'european': ['en', 'fr', 'de', 'es', 'pt', 'it', 'ru'],
            'east_asian': ['zh', 'ja', 'ko'],
            'southeast_asian': ['th', 'vi', 'my'],
            'middle_eastern': ['ar', 'ur'],
            'south_asian': ['si']
        }
    
    def translate_query(self, query: str, target_languages: List[str], source_language: str = 'auto') -> Dict[str, Any]:
        """Translate a query to multiple target languages"""
        try:
            results = {
                'original_query': query,
                'source_language': source_language,
                'translations': {},
                'detected_language': source_language if source_language != 'auto' else None
            }
            
            # Detect source language if auto
            if source_language == 'auto':
                detected_lang = self.detect_language(query)
                results['detected_language'] = detected_lang['language']
                source_language = detected_lang['language']
            
            # Translate to each target language
            for target_lang in target_languages:
                if target_lang in self.supported_languages:
                    translation = self._translate_text(query, source_language, target_lang)
                    results['translations'][target_lang] = {
                        'translated_text': translation,
                        'language_name': self.supported_languages[target_lang],
                        'confidence': 0.8  # Mock confidence
                    }
            
            return results
            
        except Exception as e:
            return {
                'original_query': query,
                'source_language': source_language,
                'translations': {},
                'error': str(e)
            }
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> Dict[str, Any]:
        """Translate text to a single target language"""
        try:
            # Detect source language if auto
            if source_language == 'auto':
                detected_lang = self.detect_language(text)
                source_language = detected_lang['language']
            
            # Validate languages
            if target_language not in self.supported_languages:
                return {
                    'error': f'Unsupported target language: {target_language}',
                    'supported_languages': list(self.supported_languages.keys())
                }
            
            # Perform translation
            translated_text = self._translate_text(text, source_language, target_language)
            
            return {
                'original_text': text,
                'translated_text': translated_text,
                'source_language': source_language,
                'target_language': target_language,
                'source_language_name': self.supported_languages.get(source_language, 'Unknown'),
                'target_language_name': self.supported_languages[target_language],
                'confidence': 0.8  # Mock confidence
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'original_text': text,
                'target_language': target_language
            }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of text"""
        try:
            # Simple language detection based on character sets
            # In a real implementation, you'd use a proper language detection library
            
            # Check for Indian scripts
            devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
            bengali_chars = len(re.findall(r'[\u0980-\u09FF]', text))
            tamil_chars = len(re.findall(r'[\u0B80-\u0BFF]', text))
            telugu_chars = len(re.findall(r'[\u0C00-\u0C7F]', text))
            kannada_chars = len(re.findall(r'[\u0C80-\u0CFF]', text))
            malayalam_chars = len(re.findall(r'[\u0D00-\u0D7F]', text))
            gujarati_chars = len(re.findall(r'[\u0A80-\u0AFF]', text))
            gurmukhi_chars = len(re.findall(r'[\u0A00-\u0A7F]', text))
            urdu_chars = len(re.findall(r'[\u0600-\u06FF]', text))
            
            total_chars = len(text)
            
            if total_chars == 0:
                return {'language': 'en', 'confidence': 0.0}
            
            # Calculate ratios
            ratios = [
                ('hi', devanagari_chars / total_chars),
                ('bn', bengali_chars / total_chars),
                ('ta', tamil_chars / total_chars),
                ('te', telugu_chars / total_chars),
                ('kn', kannada_chars / total_chars),
                ('ml', malayalam_chars / total_chars),
                ('gu', gujarati_chars / total_chars),
                ('pa', gurmukhi_chars / total_chars),
                ('ur', urdu_chars / total_chars)
            ]
            
            max_ratio = max(ratios, key=lambda x: x[1])
            
            if max_ratio[1] > 0.1:  # More than 10% of characters
                return {
                    'language': max_ratio[0],
                    'confidence': min(0.9, max_ratio[1] + 0.5),
                    'language_name': self.supported_languages.get(max_ratio[0], 'Unknown')
                }
            else:
                return {
                    'language': 'en',
                    'confidence': 0.8,
                    'language_name': 'English'
                }
                
        except Exception as e:
            return {
                'language': 'en',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_supported_languages(self) -> Dict[str, Any]:
        """Get list of supported languages"""
        return {
            'languages': self.supported_languages,
            'language_families': self.language_families,
            'total_languages': len(self.supported_languages),
            'indian_languages': [lang for lang in self.supported_languages.keys() if lang in ['hi', 'bn', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur', 'or', 'as', 'ne']]
        }
    
    def translate_search_terms(self, search_terms: List[str], target_language: str) -> Dict[str, Any]:
        """Translate search terms for better search results"""
        try:
            translated_terms = {}
            
            for term in search_terms:
                translation = self.translate_text(term, target_language)
                if 'error' not in translation:
                    translated_terms[term] = translation['translated_text']
                else:
                    translated_terms[term] = term  # Keep original if translation fails
            
            return {
                'original_terms': search_terms,
                'translated_terms': translated_terms,
                'target_language': target_language,
                'target_language_name': self.supported_languages.get(target_language, 'Unknown')
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'original_terms': search_terms,
                'target_language': target_language
            }
    
    def get_language_statistics(self, text: str) -> Dict[str, Any]:
        """Get language statistics for text"""
        try:
            # Detect language
            detected = self.detect_language(text)
            
            # Count characters by script
            script_counts = {
                'devanagari': len(re.findall(r'[\u0900-\u097F]', text)),
                'bengali': len(re.findall(r'[\u0980-\u09FF]', text)),
                'tamil': len(re.findall(r'[\u0B80-\u0BFF]', text)),
                'telugu': len(re.findall(r'[\u0C00-\u0C7F]', text)),
                'kannada': len(re.findall(r'[\u0C80-\u0C7F]', text)),
                'malayalam': len(re.findall(r'[\u0D00-\u0D7F]', text)),
                'gujarati': len(re.findall(r'[\u0A80-\u0AFF]', text)),
                'gurmukhi': len(re.findall(r'[\u0A00-\u0A7F]', text)),
                'urdu': len(re.findall(r'[\u0600-\u06FF]', text)),
                'latin': len(re.findall(r'[a-zA-Z]', text)),
                'numbers': len(re.findall(r'[0-9]', text)),
                'punctuation': len(re.findall(r'[^\w\s]', text))
            }
            
            total_chars = len(text)
            
            return {
                'detected_language': detected,
                'total_characters': total_chars,
                'script_distribution': {
                    script: {
                        'count': count,
                        'percentage': (count / total_chars * 100) if total_chars > 0 else 0
                    }
                    for script, count in script_counts.items()
                },
                'language_family': self._get_language_family(detected.get('language', 'en'))
            }
            
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def _translate_text(self, text: str, source_language: str, target_language: str) -> str:
        """Internal translation method (mock implementation)"""
        # In a real implementation, you'd use Google Translate API, Azure Translator, or similar
        
        # Mock translations for demonstration
        mock_translations = {
            ('en', 'hi'): {
                'hello': 'नमस्ते',
                'world': 'दुनिया',
                'search': 'खोज',
                'information': 'जानकारी',
                'security': 'सुरक्षा',
                'analysis': 'विश्लेषण'
            },
            ('en', 'bn'): {
                'hello': 'হ্যালো',
                'world': 'বিশ্ব',
                'search': 'অনুসন্ধান',
                'information': 'তথ্য',
                'security': 'নিরাপত্তা',
                'analysis': 'বিশ্লেষণ'
            },
            ('en', 'ta'): {
                'hello': 'வணக்கம்',
                'world': 'உலகம்',
                'search': 'தேடல்',
                'information': 'தகவல்',
                'security': 'பாதுகாப்பு',
                'analysis': 'பகுப்பாய்வு'
            },
            ('en', 'te'): {
                'hello': 'హలో',
                'world': 'ప్రపంచం',
                'search': 'శోధన',
                'information': 'సమాచారం',
                'security': 'భద్రత',
                'analysis': 'విశ్లేషణ'
            },
            ('en', 'mr'): {
                'hello': 'नमस्कार',
                'world': 'जग',
                'search': 'शोध',
                'information': 'माहिती',
                'security': 'सुरक्षा',
                'analysis': 'विश्लेषण'
            }
        }
        
        # Check if we have mock translations
        translation_key = (source_language, target_language)
        if translation_key in mock_translations:
            # Simple word-by-word translation
            words = text.lower().split()
            translated_words = []
            
            for word in words:
                if word in mock_translations[translation_key]:
                    translated_words.append(mock_translations[translation_key][word])
                else:
                    translated_words.append(word)  # Keep original if no translation
            
            return ' '.join(translated_words)
        else:
            # For unsupported language pairs, return original text
            return text
    
    def _get_language_family(self, language_code: str) -> str:
        """Get the language family for a language code"""
        for family, languages in self.language_families.items():
            if language_code in languages:
                return family
        return 'other'
    
    def validate_language_code(self, language_code: str) -> bool:
        """Validate if a language code is supported"""
        return language_code in self.supported_languages
    
    def get_language_name(self, language_code: str) -> str:
        """Get the full name of a language from its code"""
        return self.supported_languages.get(language_code, 'Unknown')
    
    def get_related_languages(self, language_code: str) -> List[str]:
        """Get related languages in the same family"""
        for family, languages in self.language_families.items():
            if language_code in languages:
                return [lang for lang in languages if lang != language_code]
        return [] 