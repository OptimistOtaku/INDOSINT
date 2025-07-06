import React from 'react';
import { Row, Col, Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const features = [
    {
      title: "Social Media Search",
      description: "Search for individuals across multiple social media platforms including Twitter, LinkedIn, and Facebook.",
      icon: "🔍",
      link: "/social-search",
      color: "primary"
    },
    {
      title: "Digital Footprint Analysis",
      description: "Analyze a person's complete digital presence including social media, email breaches, and domain registrations.",
      icon: "👣",
      link: "/footprint",
      color: "success"
    },
    {
      title: "Face Recognition Search",
      description: "Upload an image to find matching faces across social media and public databases.",
      icon: "👤",
      link: "/face-recognition",
      color: "info"
    },
    {
      title: "Data Visualization",
      description: "Interactive charts and graphs to visualize OSINT data and relationships.",
      icon: "📊",
      link: "/visualization",
      color: "warning"
    }
  ];

  return (
    <div>
      <div className="text-center mb-4">
        <h1>🔍 INDOSINT - Indian OSINT Platform</h1>
        <p className="lead">
          Advanced Open Source Intelligence system designed specifically for India
        </p>
      </div>

      <Row>
        {features.map((feature, index) => (
          <Col key={index} lg={6} md={6} sm={12} className="mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Body className="text-center">
                <div className="display-4 mb-3">{feature.icon}</div>
                <Card.Title>{feature.title}</Card.Title>
                <Card.Text>{feature.description}</Card.Text>
                <Button 
                  as={Link} 
                  to={feature.link} 
                  variant={feature.color}
                  className="w-100"
                >
                  Get Started
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Row className="mt-4">
        <Col>
          <Card className="bg-light">
            <Card.Body>
              <h5>🚀 Quick Start</h5>
              <p>
                Choose any feature above to begin your OSINT investigation. 
                The platform supports multiple Indian languages and provides 
                comprehensive digital intelligence gathering capabilities.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 