import requests
import json
import re
from typing import Dict, List, Any
from datetime import datetime

class DigitalFootprintService:
    """Service for digital footprint analysis"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_footprint(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze digital footprint for email or domain"""
        email = data.get('email')
        domain = data.get('domain')
        
        if not email and not domain:
            raise ValueError("Email or domain is required")
        
        analysis = {
            'name': email or domain,
            'email': email,
            'domain': domain,
            'confidence': 0.8,
            'risk_level': 'low',
            'risk_score': 0.0,
            'privacy_score': 0.0,
            'exposure_level': 'low',
            'email_breaches': [],
            'domain_registrations': [],
            'data_breaches': [],
            'online_presence': [],
            'risk_factors': [],
            'recommendations': []
        }
        
        if email:
            email_analysis = self._analyze_email(email)
            analysis.update(email_analysis)
        
        if domain:
            domain_analysis = self._analyze_domain(domain)
            analysis.update(domain_analysis)
        
        # Calculate overall risk and privacy scores
        analysis['risk_score'] = self._calculate_risk_score(analysis)
        analysis['privacy_score'] = self._calculate_privacy_score(analysis)
        analysis['exposure_level'] = self._determine_exposure_level(analysis)
        analysis['risk_level'] = self._determine_risk_level(analysis['risk_score'])
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _analyze_email(self, email: str) -> Dict[str, Any]:
        """Analyze email for breaches and exposure"""
        analysis = {
            'email_breaches': [],
            'data_breaches': [],
            'online_presence': []
        }
        
        # Mock email breach data
        mock_breaches = [
            {
                'breach_name': 'LinkedIn 2012',
                'date': '2012-06-05',
                'records': '165M',
                'email_count': 1,
                'password_hash': True,
                'salted_hash': True
            },
            {
                'breach_name': 'Adobe 2013',
                'date': '2013-10-04',
                'records': '153M',
                'email_count': 1,
                'password_hash': True,
                'salted_hash': False
            },
            {
                'breach_name': 'Dropbox 2012',
                'date': '2012-07-01',
                'records': '68M',
                'email_count': 1,
                'password_hash': True,
                'salted_hash': True
            }
        ]
        
        # Simulate finding breaches (mock)
        if '@' in email:
            analysis['email_breaches'] = mock_breaches[:2]  # Simulate 2 breaches found
            analysis['data_breaches'] = mock_breaches[:1]  # Simulate 1 data breach
        
        # Mock online presence
        analysis['online_presence'] = [
            {
                'platform': 'github',
                'url': f'https://github.com/{email.split("@")[0]}',
                'username': email.split("@")[0],
                'public_repos': 15,
                'followers': 50
            },
            {
                'platform': 'stackoverflow',
                'url': f'https://stackoverflow.com/users/{email.split("@")[0]}',
                'username': email.split("@")[0],
                'reputation': 2500,
                'answers': 45
            }
        ]
        
        return analysis
    
    def _analyze_domain(self, domain: str) -> Dict[str, Any]:
        """Analyze domain for registrations and information"""
        analysis = {
            'domain_registrations': [],
            'online_presence': []
        }
        
        # Mock domain registration data
        analysis['domain_registrations'] = [
            {
                'domain': domain,
                'registrar': 'GoDaddy.com, LLC',
                'creation_date': '2020-01-15',
                'expiration_date': '2025-01-15',
                'status': 'active',
                'nameservers': ['ns1.example.com', 'ns2.example.com'],
                'whois_data': {
                    'registrant_name': 'John Doe',
                    'registrant_email': f'admin@{domain}',
                    'registrant_phone': '+91.1234567890',
                    'registrant_organization': 'Example Corp'
                }
            }
        ]
        
        # Mock online presence for domain
        analysis['online_presence'] = [
            {
                'platform': 'website',
                'url': f'https://{domain}',
                'title': f'{domain.title()} - Official Website',
                'description': f'Official website for {domain}',
                'technologies': ['WordPress', 'PHP', 'MySQL'],
                'ssl_certificate': True,
                'security_headers': True
            },
            {
                'platform': 'social_media',
                'url': f'https://twitter.com/{domain.replace(".", "")}',
                'username': domain.replace(".", ""),
                'followers': 1000,
                'verified': True
            }
        ]
        
        return analysis
    
    def _calculate_risk_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall risk score"""
        risk_score = 0.0
        
        # Email breaches contribute to risk
        breach_count = len(analysis.get('email_breaches', []))
        risk_score += breach_count * 0.2
        
        # Data breaches contribute more to risk
        data_breach_count = len(analysis.get('data_breaches', []))
        risk_score += data_breach_count * 0.3
        
        # Online presence can increase or decrease risk
        online_presence = analysis.get('online_presence', [])
        for presence in online_presence:
            if presence.get('platform') in ['github', 'stackoverflow']:
                risk_score += 0.1  # Professional presence
            elif presence.get('platform') == 'website':
                if presence.get('ssl_certificate') and presence.get('security_headers'):
                    risk_score -= 0.1  # Secure website
                else:
                    risk_score += 0.2  # Insecure website
        
        # Domain age affects risk
        domain_registrations = analysis.get('domain_registrations', [])
        if domain_registrations:
            creation_date = datetime.strptime(domain_registrations[0]['creation_date'], '%Y-%m-%d')
            days_old = (datetime.now() - creation_date).days
            if days_old < 365:  # Less than 1 year
                risk_score += 0.2
            elif days_old > 3650:  # More than 10 years
                risk_score -= 0.1
        
        return min(1.0, max(0.0, risk_score))
    
    def _calculate_privacy_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate privacy score (higher is better)"""
        privacy_score = 1.0
        
        # Each breach reduces privacy
        breach_count = len(analysis.get('email_breaches', []))
        privacy_score -= breach_count * 0.15
        
        # Data breaches reduce privacy more
        data_breach_count = len(analysis.get('data_breaches', []))
        privacy_score -= data_breach_count * 0.25
        
        # Online presence can affect privacy
        online_presence = analysis.get('online_presence', [])
        for presence in online_presence:
            if presence.get('platform') in ['github', 'stackoverflow']:
                privacy_score -= 0.05  # Public professional profiles
            elif presence.get('platform') == 'website':
                privacy_score -= 0.1  # Public website
        
        return max(0.0, privacy_score)
    
    def _determine_exposure_level(self, analysis: Dict[str, Any]) -> str:
        """Determine exposure level based on analysis"""
        breach_count = len(analysis.get('email_breaches', []))
        online_presence_count = len(analysis.get('online_presence', []))
        
        if breach_count >= 3 or online_presence_count >= 5:
            return 'high'
        elif breach_count >= 1 or online_presence_count >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on score"""
        if risk_score >= 0.7:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Breach-related recommendations
        breach_count = len(analysis.get('email_breaches', []))
        if breach_count > 0:
            recommendations.append(f"Email found in {breach_count} data breach(es) - change passwords immediately")
            recommendations.append("Enable two-factor authentication on all accounts")
            recommendations.append("Use a password manager to generate unique passwords")
        
        # Domain-related recommendations
        domain_registrations = analysis.get('domain_registrations', [])
        if domain_registrations:
            domain = domain_registrations[0]
            if not domain.get('whois_data', {}).get('registrant_organization'):
                recommendations.append("Consider using WHOIS privacy protection for domain registration")
            
            if not domain.get('ssl_certificate'):
                recommendations.append("Enable SSL certificate for website security")
        
        # Online presence recommendations
        online_presence = analysis.get('online_presence', [])
        if online_presence:
            recommendations.append("Review and update privacy settings on social media accounts")
            recommendations.append("Consider removing or securing personal information from public profiles")
        
        # General recommendations
        if analysis['risk_score'] > 0.5:
            recommendations.append("Consider using a VPN for additional privacy")
            recommendations.append("Regularly monitor credit reports for suspicious activity")
        
        if analysis['privacy_score'] < 0.5:
            recommendations.append("Review and minimize online footprint")
            recommendations.append("Consider using privacy-focused email and search services")
        
        return recommendations
    
    def check_email_breach(self, email: str) -> List[Dict[str, Any]]:
        """Check if email has been involved in data breaches"""
        # Mock implementation - in real scenario, you'd use HaveIBeenPwned API or similar
        mock_breaches = [
            {
                'breach_name': 'LinkedIn 2012',
                'date': '2012-06-05',
                'records': '165M',
                'email_count': 1,
                'password_hash': True,
                'salted_hash': True,
                'description': 'In 2012, LinkedIn suffered a data breach that exposed 165 million email addresses and hashed passwords.'
            }
        ]
        
        # Simulate finding breaches
        if '@' in email and 'test' not in email.lower():
            return mock_breaches
        return []
    
    def check_domain_info(self, domain: str) -> Dict[str, Any]:
        """Get domain registration information"""
        # Mock implementation - in real scenario, you'd use WHOIS lookup
        return {
            'domain': domain,
            'registrar': 'GoDaddy.com, LLC',
            'creation_date': '2020-01-15',
            'expiration_date': '2025-01-15',
            'status': 'active',
            'nameservers': ['ns1.example.com', 'ns2.example.com'],
            'whois_data': {
                'registrant_name': 'John Doe',
                'registrant_email': f'admin@{domain}',
                'registrant_phone': '+91.1234567890',
                'registrant_organization': 'Example Corp',
                'registrant_address': '123 Main St, Mumbai, Maharashtra, India'
            }
        }
    
    def find_online_presence(self, query: str) -> List[Dict[str, Any]]:
        """Find online presence for a query (name, email, or domain)"""
        # Mock implementation - in real scenario, you'd search multiple platforms
        presence = []
        
        if '@' in query:  # Email
            username = query.split('@')[0]
            presence.extend([
                {
                    'platform': 'github',
                    'url': f'https://github.com/{username}',
                    'username': username,
                    'type': 'code_repository',
                    'public_repos': 15,
                    'followers': 50
                },
                {
                    'platform': 'stackoverflow',
                    'url': f'https://stackoverflow.com/users/{username}',
                    'username': username,
                    'type': 'qa_platform',
                    'reputation': 2500,
                    'answers': 45
                }
            ])
        elif '.' in query:  # Domain
            presence.extend([
                {
                    'platform': 'website',
                    'url': f'https://{query}',
                    'title': f'{query.title()} - Official Website',
                    'type': 'website',
                    'ssl_certificate': True,
                    'security_headers': True
                }
            ])
        else:  # Name
            presence.extend([
                {
                    'platform': 'linkedin',
                    'url': f'https://linkedin.com/in/{query.lower().replace(" ", "-")}',
                    'username': query.lower().replace(" ", "-"),
                    'type': 'professional_network',
                    'verified': True
                }
            ])
        
        return presence 