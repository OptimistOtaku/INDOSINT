import React, { useState } from 'react';
import { Form, Button, Card, Row, Col, Badge, Alert, ProgressBar } from 'react-bootstrap';
import axios from 'axios';

const DigitalFootprint = () => {
  const [personData, setPersonData] = useState({
    name: '',
    email: '',
    phone: '',
    location: ''
  });
  const [footprint, setFootprint] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPersonData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!personData.name.trim()) return;

    setLoading(true);
    setError('');
    setFootprint(null);

    try {
      const response = await axios.post('/analyze/footprint', personData);
      setFootprint(response.data);
    } catch (err) {
      setError('Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score) => {
    if (score < 0.3) return 'success';
    if (score < 0.7) return 'warning';
    return 'danger';
  };

  const getRiskLevel = (score) => {
    if (score < 0.3) return 'Low';
    if (score < 0.7) return 'Medium';
    return 'High';
  };

  return (
    <div>
      <h2>👣 Digital Footprint Analysis</h2>
      <p className="text-muted mb-4">
        Analyze a person's complete digital presence and assess risk factors
      </p>

      <Card className="mb-4">
        <Card.Body>
          <Form onSubmit={handleAnalyze}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Full Name *</Form.Label>
                  <Form.Control
                    type="text"
                    name="name"
                    placeholder="Enter full name..."
                    value={personData.name}
                    onChange={handleInputChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Email Address</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    placeholder="Enter email address..."
                    value={personData.email}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Phone Number</Form.Label>
                  <Form.Control
                    type="tel"
                    name="phone"
                    placeholder="Enter phone number..."
                    value={personData.phone}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Location</Form.Label>
                  <Form.Control
                    type="text"
                    name="location"
                    placeholder="Enter location..."
                    value={personData.location}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Button 
              type="submit" 
              variant="primary" 
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Analyze Digital Footprint'}
            </Button>
          </Form>
        </Card.Body>
      </Card>

      {error && (
        <Alert variant="danger" className="mb-4">
          {error}
        </Alert>
      )}

      {footprint && (
        <div>
          <h4>Analysis Results</h4>
          
          {/* Risk Score */}
          <Card className="mb-4">
            <Card.Body>
              <h5>Risk Assessment</h5>
              <div className="d-flex align-items-center mb-3">
                <div className="flex-grow-1 me-3">
                  <ProgressBar 
                    now={footprint.footprint.risk_score * 100} 
                    variant={getRiskColor(footprint.footprint.risk_score)}
                    className="mb-2"
                  />
                  <small className="text-muted">
                    Risk Score: {Math.round(footprint.footprint.risk_score * 100)}%
                  </small>
                </div>
                <Badge bg={getRiskColor(footprint.footprint.risk_score)}>
                  {getRiskLevel(footprint.footprint.risk_score)} Risk
                </Badge>
              </div>
            </Card.Body>
          </Card>

          {/* Social Media Presence */}
          <Card className="mb-4">
            <Card.Body>
              <h5>Social Media Presence</h5>
              <Row>
                {footprint.footprint.social_presence.map((profile, index) => (
                  <Col key={index} lg={4} md={6} sm={12} className="mb-3">
                    <Card className="h-100">
                      <Card.Body>
                        <div className="d-flex justify-content-between align-items-start mb-2">
                          <h6 className="mb-0">{profile.platform}</h6>
                          <Badge bg={profile.confidence > 0.8 ? 'success' : 'warning'}>
                            {Math.round(profile.confidence * 100)}%
                          </Badge>
                        </div>
                        <Card.Title>{profile.username}</Card.Title>
                        <Card.Text>
                          <small className="text-muted">{profile.bio}</small>
                        </Card.Text>
                        <div className="row text-center">
                          <div className="col">
                            <strong>{profile.followers?.toLocaleString() || 'N/A'}</strong>
                            <br />
                            <small className="text-muted">Followers</small>
                          </div>
                          <div className="col">
                            <strong>{profile.posts?.toLocaleString() || 'N/A'}</strong>
                            <br />
                            <small className="text-muted">Posts</small>
                          </div>
                        </div>
                      </Card.Body>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card.Body>
          </Card>

          {/* Email Breaches */}
          {footprint.footprint.email_breaches.length > 0 && (
            <Card className="mb-4">
              <Card.Body>
                <h5>Email Breach History</h5>
                <Row>
                  {footprint.footprint.email_breaches.map((breach, index) => (
                    <Col key={index} md={6} sm={12} className="mb-3">
                      <Card className="border-danger">
                        <Card.Body>
                          <h6>{breach.breach_name}</h6>
                          <p className="text-muted mb-2">
                            Date: {breach.date} | Severity: {breach.severity}
                          </p>
                          <div>
                            <strong>Compromised Data:</strong>
                            <div>
                              {breach.data_types.map((type, i) => (
                                <Badge key={i} bg="danger" className="me-1">
                                  {type}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </Card.Body>
            </Card>
          )}

          {/* Domain Registrations */}
          {footprint.footprint.domain_registrations.length > 0 && (
            <Card className="mb-4">
              <Card.Body>
                <h5>Domain Registrations</h5>
                <Row>
                  {footprint.footprint.domain_registrations.map((domain, index) => (
                    <Col key={index} md={6} sm={12} className="mb-3">
                      <Card>
                        <Card.Body>
                          <h6>{domain.domain}</h6>
                          <p className="text-muted mb-2">
                            Registrar: {domain.registrar}
                          </p>
                          <div className="row">
                            <div className="col">
                              <small className="text-muted">Registered</small>
                              <br />
                              <strong>{domain.registration_date}</strong>
                            </div>
                            <div className="col">
                              <small className="text-muted">Expires</small>
                              <br />
                              <strong>{domain.expiry_date}</strong>
                            </div>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </Card.Body>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

export default DigitalFootprint; 