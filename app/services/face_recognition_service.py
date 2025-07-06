import cv2
import numpy as np
import face_recognition
from typing import List, Dict, Any, Tuple
import os
from PIL import Image
import io
import base64

class FaceRecognitionService:
    """Service for face recognition and analysis"""
    
    def __init__(self):
        self.known_faces = []
        self.known_names = []
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def search_faces(self, image_file, confidence_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Search for faces in an image and match against known faces"""
        try:
            # Read image
            image_bytes = image_file.read()
            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Could not read image")
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            results = []
            
            for i, (face_location, face_encoding) in enumerate(zip(face_locations, face_encodings)):
                # Analyze face
                face_analysis = self._analyze_face(rgb_image, face_location)
                
                # Match against known faces
                matches = self._match_face(face_encoding, confidence_threshold)
                
                # Create result
                result = {
                    'face_id': i,
                    'location': {
                        'top': face_location[0],
                        'right': face_location[1],
                        'bottom': face_location[2],
                        'left': face_location[3]
                    },
                    'analysis': face_analysis,
                    'matches': matches,
                    'confidence': max([match['confidence'] for match in matches]) if matches else 0.0
                }
                
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error in face recognition: {str(e)}")
            return []
    
    def _analyze_face(self, image: np.ndarray, face_location: Tuple[int, int, int, int]) -> Dict[str, Any]:
        """Analyze face characteristics"""
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        
        # Convert to grayscale for analysis
        gray_face = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY)
        
        analysis = {
            'age_estimate': self._estimate_age(gray_face),
            'gender_estimate': self._estimate_gender(gray_face),
            'emotion_estimate': self._estimate_emotion(gray_face),
            'face_quality': self._assess_face_quality(gray_face),
            'landmarks': self._detect_landmarks(face_image),
            'attributes': self._extract_attributes(face_image)
        }
        
        return analysis
    
    def _estimate_age(self, face_image: np.ndarray) -> Dict[str, Any]:
        """Estimate age from face image (mock implementation)"""
        # In a real implementation, you'd use a pre-trained age estimation model
        # For now, return a mock estimate
        return {
            'estimated_age': 30,
            'confidence': 0.7,
            'age_range': '25-35'
        }
    
    def _estimate_gender(self, face_image: np.ndarray) -> Dict[str, Any]:
        """Estimate gender from face image (mock implementation)"""
        # In a real implementation, you'd use a pre-trained gender classification model
        return {
            'gender': 'male',
            'confidence': 0.8
        }
    
    def _estimate_emotion(self, face_image: np.ndarray) -> Dict[str, Any]:
        """Estimate emotion from face image (mock implementation)"""
        # In a real implementation, you'd use a pre-trained emotion recognition model
        emotions = ['happy', 'sad', 'angry', 'surprised', 'neutral']
        return {
            'primary_emotion': 'neutral',
            'confidence': 0.6,
            'emotion_scores': {
                'happy': 0.1,
                'sad': 0.1,
                'angry': 0.1,
                'surprised': 0.1,
                'neutral': 0.6
            }
        }
    
    def _assess_face_quality(self, face_image: np.ndarray) -> Dict[str, Any]:
        """Assess the quality of the face image"""
        # Calculate basic quality metrics
        height, width = face_image.shape
        
        # Brightness
        brightness = np.mean(face_image)
        
        # Contrast
        contrast = np.std(face_image)
        
        # Sharpness (using Laplacian variance)
        laplacian_var = cv2.Laplacian(face_image, cv2.CV_64F).var()
        
        # Quality score
        quality_score = min(1.0, (brightness / 255.0 + contrast / 100.0 + laplacian_var / 1000.0) / 3.0)
        
        return {
            'quality_score': quality_score,
            'brightness': brightness,
            'contrast': contrast,
            'sharpness': laplacian_var,
            'resolution': f"{width}x{height}",
            'is_good_quality': quality_score > 0.5
        }
    
    def _detect_landmarks(self, face_image: np.ndarray) -> Dict[str, Any]:
        """Detect facial landmarks (mock implementation)"""
        # In a real implementation, you'd use dlib or similar for landmark detection
        height, width = face_image.shape[:2]
        
        return {
            'landmarks_detected': True,
            'landmark_count': 68,  # Standard 68-point landmark model
            'key_points': {
                'left_eye': (width // 4, height // 3),
                'right_eye': (3 * width // 4, height // 3),
                'nose': (width // 2, height // 2),
                'left_mouth': (width // 3, 2 * height // 3),
                'right_mouth': (2 * width // 3, 2 * height // 3)
            }
        }
    
    def _extract_attributes(self, face_image: np.ndarray) -> Dict[str, Any]:
        """Extract facial attributes (mock implementation)"""
        # In a real implementation, you'd use a pre-trained attribute classification model
        return {
            'glasses': False,
            'beard': True,
            'mustache': False,
            'bald': False,
            'hair_color': 'black',
            'eye_color': 'brown',
            'skin_tone': 'medium'
        }
    
    def _match_face(self, face_encoding: np.ndarray, confidence_threshold: float) -> List[Dict[str, Any]]:
        """Match face against known faces"""
        matches = []
        
        # In a real implementation, you'd have a database of known faces
        # For now, return mock matches
        mock_known_faces = [
            {
                'name': 'John Doe',
                'encoding': np.random.rand(128),  # Mock encoding
                'source': 'social_media',
                'confidence': 0.85
            },
            {
                'name': 'Jane Smith',
                'encoding': np.random.rand(128),  # Mock encoding
                'source': 'government_database',
                'confidence': 0.72
            }
        ]
        
        for known_face in mock_known_faces:
            # Calculate similarity (mock)
            similarity = np.random.uniform(0.0, 1.0)
            
            if similarity >= confidence_threshold:
                matches.append({
                    'name': known_face['name'],
                    'source': known_face['source'],
                    'confidence': similarity,
                    'similarity_score': similarity
                })
        
        return matches
    
    def add_known_face(self, name: str, image_file, source: str = 'manual') -> bool:
        """Add a known face to the database"""
        try:
            # Read and encode the face
            image_bytes = image_file.read()
            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            if image is None:
                return False
            
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(rgb_image)
            
            if not face_encodings:
                return False
            
            # Add to known faces
            self.known_faces.append(face_encodings[0])
            self.known_names.append({
                'name': name,
                'source': source,
                'added_at': '2024-01-01T00:00:00Z'
            })
            
            return True
            
        except Exception as e:
            print(f"Error adding known face: {str(e)}")
            return False
    
    def compare_faces(self, face_encoding1: np.ndarray, face_encoding2: np.ndarray) -> float:
        """Compare two face encodings and return similarity score"""
        try:
            # Calculate Euclidean distance
            distance = face_recognition.face_distance([face_encoding1], face_encoding2)[0]
            
            # Convert distance to similarity score (0-1)
            similarity = 1.0 - distance
            
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            print(f"Error comparing faces: {str(e)}")
            return 0.0
    
    def detect_faces_in_image(self, image_file) -> List[Dict[str, Any]]:
        """Detect all faces in an image without matching"""
        try:
            # Read image
            image_bytes = image_file.read()
            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Could not read image")
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_image)
            
            results = []
            for i, face_location in enumerate(face_locations):
                result = {
                    'face_id': i,
                    'location': {
                        'top': face_location[0],
                        'right': face_location[1],
                        'bottom': face_location[2],
                        'left': face_location[3]
                    },
                    'confidence': 0.9  # High confidence for detection
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error detecting faces: {str(e)}")
            return []
    
    def extract_face_embedding(self, image_file) -> np.ndarray:
        """Extract face embedding from image"""
        try:
            # Read image
            image_bytes = image_file.read()
            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Could not read image")
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect and encode face
            face_encodings = face_recognition.face_encodings(rgb_image)
            
            if not face_encodings:
                raise ValueError("No face detected in image")
            
            return face_encodings[0]
            
        except Exception as e:
            print(f"Error extracting face embedding: {str(e)}")
            return None
    
    def get_face_statistics(self) -> Dict[str, Any]:
        """Get statistics about the face recognition system"""
        return {
            'total_known_faces': len(self.known_faces),
            'sources': list(set([face['source'] for face in self.known_names])),
            'system_status': 'operational',
            'model_version': '1.0.0',
            'supported_formats': ['jpg', 'jpeg', 'png', 'bmp'],
            'max_image_size': '10MB',
            'confidence_threshold': 0.5
        } 