import React, { useState, useRef } from 'react';
import { Form, Button, Card, Row, Col, Alert, Image } from 'react-bootstrap';
import axios from 'axios';

const FaceRecognition = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef();

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        setSelectedFile(file);
        setError('');
        
        // Create preview URL
        const reader = new FileReader();
        reader.onload = (e) => {
          setPreviewUrl(e.target.result);
        };
        reader.readAsDataURL(file);
      } else {
        setError('Please select a valid image file.');
        setSelectedFile(null);
        setPreviewUrl('');
      }
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setLoading(true);
    setError('');
    setResults(null);

    try {
      // Convert file to base64
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64Data = e.target.result;
        
        try {
          const response = await axios.post('/search/face-recognition', base64Data);
          setResults(response.data);
        } catch (err) {
          setError('Face recognition failed. Please try again.');
          console.error('Face recognition error:', err);
        } finally {
          setLoading(false);
        }
      };
      reader.readAsDataURL(selectedFile);
    } catch (err) {
      setError('File processing failed. Please try again.');
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreviewUrl('');
    setResults(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div>
      <h2>👤 Face Recognition Search</h2>
      <p className="text-muted mb-4">
        Upload an image to find matching faces across social media and public databases
      </p>

      <Card className="mb-4">
        <Card.Body>
          <Form onSubmit={handleAnalyze}>
            <Form.Group className="mb-3">
              <Form.Label>Upload Image</Form.Label>
              <Form.Control
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                ref={fileInputRef}
                required
              />
              <Form.Text className="text-muted">
                Supported formats: JPG, PNG, GIF. Maximum file size: 10MB
              </Form.Text>
            </Form.Group>

            {previewUrl && (
              <div className="mb-3">
                <h6>Image Preview:</h6>
                <Image 
                  src={previewUrl} 
                  alt="Preview" 
                  fluid 
                  style={{ maxHeight: '300px' }}
                  className="border rounded"
                />
              </div>
            )}

            <div className="d-flex gap-2">
              <Button 
                type="submit" 
                variant="primary" 
                disabled={loading || !selectedFile}
              >
                {loading ? 'Analyzing...' : 'Analyze Image'}
              </Button>
              <Button 
                type="button" 
                variant="secondary" 
                onClick={handleClear}
                disabled={loading}
              >
                Clear
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>

      {error && (
        <Alert variant="danger" className="mb-4">
          {error}
        </Alert>
      )}

      {results && (
        <div>
          <h4>Analysis Results</h4>
          
          {results.error ? (
            <Alert variant="warning">
              {results.error}
            </Alert>
          ) : (
            <Card>
              <Card.Body>
                <h5>Faces Detected: {results.faces_detected}</h5>
                
                {results.results.map((face, index) => (
                  <div key={index} className="mb-4">
                    <h6>Face #{index + 1}</h6>
                    
                    {face.matches && face.matches.length > 0 ? (
                      <Row>
                        {face.matches.map((match, matchIndex) => (
                          <Col key={matchIndex} lg={6} md={6} sm={12} className="mb-3">
                            <Card className="h-100">
                              <Card.Body>
                                <div className="d-flex justify-content-between align-items-start mb-2">
                                  <h6 className="mb-0">{match.name}</h6>
                                  <span className={`badge bg-${match.confidence > 0.8 ? 'success' : 'warning'}`}>
                                    {Math.round(match.confidence * 100)}% Match
                                  </span>
                                </div>
                                <p className="text-muted mb-2">
                                  Source: {match.source}
                                </p>
                                <Button 
                                  href={match.url} 
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
                    ) : (
                      <Alert variant="info">
                        No matches found for this face in our database.
                      </Alert>
                    )}
                  </div>
                ))}
              </Card.Body>
            </Card>
          )}
        </div>
      )}

      <Card className="mt-4">
        <Card.Body>
          <h5>💡 Tips for Better Results</h5>
          <ul className="mb-0">
            <li>Use clear, high-quality images with good lighting</li>
            <li>Ensure the face is clearly visible and not obstructed</li>
            <li>Try different angles if no matches are found</li>
            <li>Results are based on publicly available data only</li>
          </ul>
        </Card.Body>
      </Card>
    </div>
  );
};

export default FaceRecognition; 