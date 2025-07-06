import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Form, Button, Alert } from 'react-bootstrap';
import Plot from 'react-plotly.js';
import axios from 'axios';

const DataVisualization = () => {
  const [footprints, setFootprints] = useState([]);
  const [selectedFootprint, setSelectedFootprint] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadFootprints();
  }, []);

  const loadFootprints = async () => {
    try {
      const response = await axios.get('/footprints');
      setFootprints(response.data.footprints || []);
    } catch (err) {
      console.error('Failed to load footprints:', err);
    }
  };

  const loadFootprintData = async (name) => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`/footprints/${name}`);
      setSelectedFootprint(response.data.footprint);
    } catch (err) {
      setError('Failed to load footprint data.');
      console.error('Footprint data error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFootprintSelect = (e) => {
    const name = e.target.value;
    if (name) {
      loadFootprintData(name);
    } else {
      setSelectedFootprint(null);
    }
  };

  // Mock data for demonstration
  const mockData = {
    socialMediaData: {
      platforms: ['Twitter', 'LinkedIn', 'Facebook', 'Instagram'],
      followers: [1200, 850, 2300, 450],
      posts: [150, 45, 320, 89]
    },
    riskTrends: {
      months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      riskScores: [0.3, 0.4, 0.35, 0.5, 0.45, 0.6]
    },
    breachTypes: {
      types: ['Email', 'Password', 'Phone', 'Address', 'Credit Card'],
      counts: [15, 12, 8, 5, 3]
    }
  };

  return (
    <div>
      <h2>📊 Data Visualization</h2>
      <p className="text-muted mb-4">
        Interactive charts and graphs to visualize OSINT data and relationships
      </p>

      <Row className="mb-4">
        <Col md={6}>
          <Form.Group>
            <Form.Label>Select Digital Footprint</Form.Label>
            <Form.Select onChange={handleFootprintSelect}>
              <option value="">Choose a footprint...</option>
              {footprints.map((name, index) => (
                <option key={index} value={name}>{name}</option>
              ))}
            </Form.Select>
          </Form.Group>
        </Col>
        <Col md={6} className="d-flex align-items-end">
          <Button 
            variant="outline-primary" 
            onClick={loadFootprints}
            disabled={loading}
          >
            Refresh Data
          </Button>
        </Col>
      </Row>

      {error && (
        <Alert variant="danger" className="mb-4">
          {error}
        </Alert>
      )}

      {loading && (
        <Alert variant="info" className="mb-4">
          Loading visualization data...
        </Alert>
      )}

      {/* Social Media Presence Chart */}
      <Card className="mb-4">
        <Card.Body>
          <h5>Social Media Presence</h5>
          <Plot
            data={[
              {
                x: mockData.socialMediaData.platforms,
                y: mockData.socialMediaData.followers,
                type: 'bar',
                name: 'Followers',
                marker: { color: 'rgb(55, 83, 109)' }
              },
              {
                x: mockData.socialMediaData.platforms,
                y: mockData.socialMediaData.posts,
                type: 'bar',
                name: 'Posts',
                marker: { color: 'rgb(26, 118, 255)' }
              }
            ]}
            layout={{
              title: 'Social Media Activity',
              barmode: 'group',
              xaxis: { title: 'Platform' },
              yaxis: { title: 'Count' },
              height: 400
            }}
            config={{ displayModeBar: false }}
          />
        </Card.Body>
      </Card>

      {/* Risk Score Trends */}
      <Card className="mb-4">
        <Card.Body>
          <h5>Risk Score Trends</h5>
          <Plot
            data={[
              {
                x: mockData.riskTrends.months,
                y: mockData.riskTrends.riskScores,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Risk Score',
                line: { color: 'rgb(219, 64, 82)', width: 3 },
                marker: { size: 8 }
              }
            ]}
            layout={{
              title: 'Digital Risk Score Over Time',
              xaxis: { title: 'Month' },
              yaxis: { 
                title: 'Risk Score',
                range: [0, 1]
              },
              height: 400
            }}
            config={{ displayModeBar: false }}
          />
        </Card.Body>
      </Card>

      {/* Data Breach Analysis */}
      <Row>
        <Col lg={6}>
          <Card className="mb-4">
            <Card.Body>
              <h5>Data Breach Types</h5>
              <Plot
                data={[
                  {
                    labels: mockData.breachTypes.types,
                    values: mockData.breachTypes.counts,
                    type: 'pie',
                    marker: {
                      colors: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                    }
                  }
                ]}
                layout={{
                  title: 'Types of Compromised Data',
                  height: 400
                }}
                config={{ displayModeBar: false }}
              />
            </Card.Body>
          </Card>
        </Col>
        <Col lg={6}>
          <Card className="mb-4">
            <Card.Body>
              <h5>Platform Distribution</h5>
              <Plot
                data={[
                  {
                    labels: mockData.socialMediaData.platforms,
                    values: mockData.socialMediaData.followers,
                    type: 'pie',
                    marker: {
                      colors: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                    }
                  }
                ]}
                layout={{
                  title: 'Social Media Platform Distribution',
                  height: 400
                }}
                config={{ displayModeBar: false }}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Network Graph Placeholder */}
      <Card className="mb-4">
        <Card.Body>
          <h5>Digital Network Graph</h5>
          <div className="text-center py-5">
            <div className="display-4 mb-3">🕸️</div>
            <p className="text-muted">
              Interactive network visualization showing connections between 
              social media profiles, email addresses, and other digital entities.
            </p>
            <p className="text-muted">
              <small>This feature will show relationships and connections in the digital footprint.</small>
            </p>
          </div>
        </Card.Body>
      </Card>

      {/* Key Insights */}
      <Card>
        <Card.Body>
          <h5>🔍 Key Insights</h5>
          <Row>
            <Col md={4}>
              <div className="text-center">
                <div className="h3 text-primary">3</div>
                <small className="text-muted">Active Social Platforms</small>
              </div>
            </Col>
            <Col md={4}>
              <div className="text-center">
                <div className="h3 text-warning">60%</div>
                <small className="text-muted">Current Risk Score</small>
              </div>
            </Col>
            <Col md={4}>
              <div className="text-center">
                <div className="h3 text-danger">2</div>
                <small className="text-muted">Data Breaches Found</small>
              </div>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </div>
  );
};

export default DataVisualization; 