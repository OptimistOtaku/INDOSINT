import React, { useState } from 'react';
import { Form, Button, Card, Row, Col, Badge, Alert } from 'react-bootstrap';
import axios from 'axios';

const SocialMediaSearch = () => {
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('en');
  const [platforms, setPlatforms] = useState(['twitter', 'linkedin', 'facebook']);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const platformOptions = [
    { value: 'twitter', label: 'Twitter' },
    { value: 'linkedin', label: 'LinkedIn' },
    { value: 'facebook', label: 'Facebook' }
  ];

  const languageOptions = [
    { value: 'en', label: 'English' },
    { value: 'hi', label: 'Hindi' },
    { value: 'bn', label: 'Bengali' },
    { value: 'ta', label: 'Tamil' },
    { value: 'te', label: 'Telugu' },
    { value: 'mr', label: 'Marathi' },
    { value: 'gu', label: 'Gujarati' }
  ];

  const handlePlatformChange = (platform) => {
    setPlatforms(prev => 
      prev.includes(platform) 
        ? prev.filter(p => p !== platform)
        : [...prev, platform]
    );
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const response = await axios.post('/search/social-media', {
        query: query.trim(),
        platforms: platforms,
        language: language
      });

      setResults(response.data.results);
    } catch (err) {
      setError('Search failed. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>🔍 Social Media Search</h2>
      <p className="text-muted mb-4">
        Search for individuals across multiple social media platforms
      </p>

      <Card className="mb-4">
        <Card.Body>
          <Form onSubmit={handleSearch}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Search Query</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter name or username to search..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Language</Form.Label>
                  <Form.Select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                  >
                    {languageOptions.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Platforms</Form.Label>
              <div>
                {platformOptions.map(platform => (
                  <Form.Check
                    key={platform.value}
                    inline
                    type="checkbox"
                    id={`platform-${platform.value}`}
                    label={platform.label}
                    checked={platforms.includes(platform.value)}
                    onChange={() => handlePlatformChange(platform.value)}
                  />
                ))}
              </div>
            </Form.Group>

            <Button 
              type="submit" 
              variant="primary" 
              disabled={loading || platforms.length === 0}
            >
              {loading ? 'Searching...' : 'Search'}
            </Button>
          </Form>
        </Card.Body>
      </Card>

      {error && (
        <Alert variant="danger" className="mb-4">
          {error}
        </Alert>
      )}

      {results.length > 0 && (
        <div>
          <h4>Search Results ({results.length})</h4>
          <Row>
            {results.map((result, index) => (
              <Col key={index} lg={6} md={6} sm={12} className="mb-3">
                <Card>
                  <Card.Body>
                    <div className="d-flex justify-content-between align-items-start mb-2">
                      <h6 className="mb-0">{result.platform}</h6>
                      <Badge bg={result.confidence > 0.8 ? 'success' : 'warning'}>
                        {Math.round(result.confidence * 100)}% Match
                      </Badge>
                    </div>
                    
                    <Card.Title>{result.username}</Card.Title>
                    <Card.Text>
                      {result.bio && <small className="text-muted">{result.bio}</small>}
                    </Card.Text>
                    
                    <div className="row text-center mb-3">
                      <div className="col">
                        <strong>{result.followers?.toLocaleString() || 'N/A'}</strong>
                        <br />
                        <small className="text-muted">Followers</small>
                      </div>
                      <div className="col">
                        <strong>{result.posts?.toLocaleString() || 'N/A'}</strong>
                        <br />
                        <small className="text-muted">Posts</small>
                      </div>
                    </div>
                    
                    <Button 
                      href={result.profile_url} 
                      target="_blank" 
                      variant="outline-primary" 
                      size="sm"
                    >
                      View Profile
                    </Button>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      )}
    </div>
  );
};

export default SocialMediaSearch; 