import requests
import json
from typing import List, Dict, Any
import time
import random
import re

class DigitalFootprintService:
    """Service for analyzing digital footprint and online presence"""
    
    def __init__(self):
        self.breach_databases = [
            'haveibeenpwned',
            'dehashed',
            'leakcheck',
            'intelx'
        ]
        
        self.domain_registrars = [
            'whois',
            'godaddy',
            'namecheap',
            'google_domains'
        ]
        
        self.data_sources = [
            'social_media',
            'professional_networks',
            'news_articles',
            'public_records',
            'company_databases'
        ]
    
    def search(self, query: str, filters: Dict = None, search_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        Search for digital footprint information
        
        Args:
            query: Search query (email, domain, name, etc.)
            filters: Additional filters
            search_types: Types of search to perform
            
        Returns:
            List of search results
        """
        if search_types is None:
            search_types = ['email_breaches', 'domain_registrations', 'data_breaches']
        
        results = []
        
        for search_type in search_types:
            try:
                if search_type == 'email_breaches':
                    breach_results = self._search_email_breaches(query, filters)
                    results.extend(breach_results)
                elif search_type == 'domain_registrations':
                    domain_results = self._search_domain_registrations(query, filters)
                    results.extend(domain_results)
                elif search_type == 'data_breaches':
                    breach_results = self._search_data_breaches(query, filters)
                    results.extend(breach_results)
                elif search_type == 'online_presence':
                    presence_results = self._search_online_presence(query, filters)
                    results.extend(presence_results)
            except Exception as e:
                print(f"Error in {search_type} search: {str(e)}")
                continue
        
        return results
    
    def _search_email_breaches(self, email: str, filters: Dict) -> List[Dict[str, Any]]:
        """Search for email in data breaches"""
        # Mock implementation
        time.sleep(random.uniform(0.2, 0.8))
        
        # Check if email looks valid
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return []
        
        # Generate mock breach data
        breaches = []
        
        # Simulate different breach scenarios
        breach_scenarios = [
            {
                'source': 'Adobe',
                'date': '2013-10-04',
                'records': 153000000,
                'severity': 'high',
                'data_types': ['email', 'password', 'username']
            },
            {
                'source': 'LinkedIn',
                'date': '2012-05-05',
                'records': 117000000,
                'severity': 'high',
                'data_types': ['email', 'password', 'username']
            },
            {
                'source': 'Dropbox',
                'date': '2012-07-01',
                'records': 68700000,
                'severity': 'medium',
                'data_types': ['email', 'password']
            },
            {
                'source': 'MySpace',
                'date': '2008-01-01',
                'records': 360000000,
                'severity': 'high',
                'data_types': ['email', 'password', 'username']
            }
        ]
        
        for scenario in random.sample(breach_scenarios, random.randint(1, 3)):
            breaches.append({
                'type': 'email_breach',
                'source': scenario['source'],
                'content': {
                    'email': email,
                    'breach_date': scenario['date'],
                    'records_affected': scenario['records'],
                    'severity': scenario['severity'],
                    'data_types_exposed': scenario['data_types'],
                    'description': f"Email found in {scenario['source']} data breach",
                    'verification_status': random.choice(['verified', 'unverified']),
                    'last_checked': '2024-01-15T10:30:00Z'
                },
                'confidence_score': round(random.uniform(0.8, 0.98), 2),
                'tags': ['breach', 'email', scenario['severity']]
            })
        
        return breaches
    
    def _search_domain_registrations(self, domain: str, filters: Dict) -> List[Dict[str, Any]]:
        """Search for domain registrations"""
        # Mock implementation
        time.sleep(random.uniform(0.3, 1.0))
        
        # Clean domain input
        domain = domain.lower().replace('http://', '').replace('https://', '').split('/')[0]
        
        # Generate mock domain data
        domains = []
        
        # Simulate different domain scenarios
        domain_scenarios = [
            {
                'domain': f'{domain}.com',
                'registrar': 'GoDaddy',
                'creation_date': '2020-03-15',
                'expiry_date': '2025-03-15',
                'status': 'active'
            },
            {
                'domain': f'{domain}.in',
                'registrar': 'NameCheap',
                'creation_date': '2019-08-20',
                'expiry_date': '2024-08-20',
                'status': 'active'
            },
            {
                'domain': f'{domain}.org',
                'registrar': 'Google Domains',
                'creation_date': '2021-01-10',
                'expiry_date': '2026-01-10',
                'status': 'active'
            }
        ]
        
        for scenario in random.sample(domain_scenarios, random.randint(1, 2)):
            domains.append({
                'type': 'domain_registration',
                'source': 'whois',
                'content': {
                    'domain': scenario['domain'],
                    'registrar': scenario['registrar'],
                    'creation_date': scenario['creation_date'],
                    'expiry_date': scenario['expiry_date'],
                    'status': scenario['status'],
                    'name_servers': [
                        'ns1.cloudflare.com',
                        'ns2.cloudflare.com'
                    ],
                    'dns_records': {
                        'A': '192.168.1.1',
                        'MX': 'mail.example.com',
                        'TXT': 'v=spf1 include:_spf.google.com ~all'
                    },
                    'whois_data': {
                        'registrant_name': f'{domain.title()} Admin',
                        'registrant_email': f'admin@{scenario["domain"]}',
                        'registrant_phone': '+91-9876543210',
                        'registrant_organization': f'{domain.title()} Organization'
                    }
                },
                'confidence_score': round(random.uniform(0.9, 0.99), 2),
                'tags': ['domain', 'registration', 'whois']
            })
        
        return domains
    
    def _search_data_breaches(self, query: str, filters: Dict) -> List[Dict[str, Any]]:
        """Search for general data breaches"""
        # Mock implementation
        time.sleep(random.uniform(0.4, 1.2))
        
        breaches = []
        
        # Simulate different types of data breaches
        breach_types = [
            {
                'type': 'password_breach',
                'source': 'RockYou2021',
                'description': 'Password breach containing millions of credentials',
                'severity': 'critical',
                'data_types': ['password', 'email', 'username']
            },
            {
                'type': 'personal_info_breach',
                'source': 'Facebook',
                'description': 'Personal information leak affecting millions of users',
                'severity': 'high',
                'data_types': ['name', 'email', 'phone', 'address']
            },
            {
                'type': 'financial_breach',
                'source': 'Equifax',
                'description': 'Financial data breach affecting credit information',
                'severity': 'critical',
                'data_types': ['ssn', 'credit_card', 'address', 'name']
            }
        ]
        
        for breach_type in random.sample(breach_types, random.randint(1, 2)):
            breaches.append({
                'type': 'data_breach',
                'source': breach_type['source'],
                'content': {
                    'breach_type': breach_type['type'],
                    'description': breach_type['description'],
                    'severity': breach_type['severity'],
                    'data_types_exposed': breach_type['data_types'],
                    'records_affected': random.randint(1000000, 100000000),
                    'breach_date': f'202{random.randint(0,3)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                    'discovery_date': f'202{random.randint(1,4)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                    'verification_status': random.choice(['verified', 'investigating', 'unverified']),
                    'impact_assessment': {
                        'financial_impact': random.choice(['low', 'medium', 'high']),
                        'privacy_impact': random.choice(['low', 'medium', 'high']),
                        'reputation_impact': random.choice(['low', 'medium', 'high'])
                    }
                },
                'confidence_score': round(random.uniform(0.7, 0.95), 2),
                'tags': ['breach', breach_type['severity'], 'data_exposure']
            })
        
        return breaches
    
    def _search_online_presence(self, query: str, filters: Dict) -> List[Dict[str, Any]]:
        """Search for online presence across various platforms"""
        # Mock implementation
        time.sleep(random.uniform(0.5, 1.5))
        
        presence_data = []
        
        # Simulate online presence on various platforms
        platforms = [
            {
                'platform': 'GitHub',
                'username': f'{query}-dev',
                'profile_url': f'https://github.com/{query}-dev',
                'type': 'developer',
                'repositories': random.randint(5, 50),
                'followers': random.randint(10, 500)
            },
            {
                'platform': 'Stack Overflow',
                'username': f'{query}_user',
                'profile_url': f'https://stackoverflow.com/users/{random.randint(100000, 999999)}/{query}_user',
                'type': 'developer',
                'reputation': random.randint(100, 10000),
                'answers': random.randint(10, 200)
            },
            {
                'platform': 'Medium',
                'username': f'{query}.writer',
                'profile_url': f'https://medium.com/@{query}.writer',
                'type': 'content_creator',
                'articles': random.randint(5, 100),
                'followers': random.randint(50, 2000)
            },
            {
                'platform': 'Reddit',
                'username': f'u/{query}_redditor',
                'profile_url': f'https://reddit.com/user/{query}_redditor',
                'type': 'social',
                'karma': random.randint(100, 10000),
                'posts': random.randint(20, 500)
            },
            {
                'platform': 'Quora',
                'username': f'{query}-expert',
                'profile_url': f'https://quora.com/profile/{query}-expert',
                'type': 'expert',
                'answers': random.randint(10, 100),
                'followers': random.randint(20, 1000)
            }
        ]
        
        for platform in random.sample(platforms, random.randint(2, 4)):
            presence_data.append({
                'type': 'online_presence',
                'source': platform['platform'],
                'content': {
                    'platform': platform['platform'],
                    'username': platform['username'],
                    'profile_url': platform['profile_url'],
                    'type': platform['type'],
                    'activity_level': random.choice(['active', 'moderate', 'inactive']),
                    'last_active': f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                    'metrics': {
                        'repositories': platform.get('repositories'),
                        'followers': platform.get('followers'),
                        'reputation': platform.get('reputation'),
                        'answers': platform.get('answers'),
                        'articles': platform.get('articles'),
                        'karma': platform.get('karma'),
                        'posts': platform.get('posts')
                    },
                    'topics': [f'topic_{i}' for i in range(1, random.randint(3, 8))],
                    'verification_status': random.choice(['verified', 'unverified'])
                },
                'confidence_score': round(random.uniform(0.6, 0.9), 2),
                'tags': ['online_presence', platform['type'], platform['platform'].lower()]
            })
        
        return presence_data
    
    def calculate_risk_score(self, email: str) -> Dict[str, Any]:
        """Calculate risk score for an email address"""
        # Mock risk calculation
        time.sleep(random.uniform(0.2, 0.6))
        
        # Simulate risk factors
        risk_factors = [
            {
                'factor': 'data_breaches',
                'description': 'Email found in multiple data breaches',
                'score': random.randint(20, 40)
            },
            {
                'factor': 'password_strength',
                'description': 'Weak passwords detected in breaches',
                'score': random.randint(10, 30)
            },
            {
                'factor': 'online_exposure',
                'description': 'High online presence and exposure',
                'score': random.randint(5, 25)
            },
            {
                'factor': 'domain_age',
                'description': 'Recently registered domain',
                'score': random.randint(5, 20)
            }
        ]
        
        total_score = sum(factor['score'] for factor in risk_factors)
        risk_level = 'low' if total_score < 30 else 'medium' if total_score < 60 else 'high'
        
        return {
            'email': email,
            'risk_score': total_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'recommendations': [
                'Enable two-factor authentication',
                'Use unique passwords for each account',
                'Monitor credit reports regularly',
                'Consider identity theft protection'
            ],
            'last_updated': '2024-01-15T10:30:00Z'
        }
    
    def get_privacy_score(self, query: str) -> Dict[str, Any]:
        """Calculate privacy exposure score"""
        # Mock privacy calculation
        time.sleep(random.uniform(0.3, 0.8))
        
        exposure_sources = [
            'social_media_profiles',
            'public_records',
            'data_breaches',
            'online_directories',
            'news_articles'
        ]
        
        privacy_score = random.randint(20, 80)
        exposure_level = 'low' if privacy_score < 30 else 'medium' if privacy_score < 60 else 'high'
        
        return {
            'query': query,
            'privacy_score': privacy_score,
            'exposure_level': exposure_level,
            'exposure_sources': random.sample(exposure_sources, random.randint(2, 4)),
            'data_points_exposed': random.randint(5, 50),
            'recommendations': [
                'Review privacy settings on social media',
                'Remove personal information from public directories',
                'Use privacy-focused search engines',
                'Consider data removal services'
            ],
            'last_updated': '2024-01-15T10:30:00Z'
        } 