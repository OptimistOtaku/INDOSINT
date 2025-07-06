import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';

const NavigationBar = () => {
  const location = useLocation();

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">
          🔍 INDOSINT
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link 
              as={Link} 
              to="/" 
              active={location.pathname === "/"}
            >
              Dashboard
            </Nav.Link>
            <Nav.Link 
              as={Link} 
              to="/social-search" 
              active={location.pathname === "/social-search"}
            >
              Social Media Search
            </Nav.Link>
            <Nav.Link 
              as={Link} 
              to="/footprint" 
              active={location.pathname === "/footprint"}
            >
              Digital Footprint
            </Nav.Link>
            <Nav.Link 
              as={Link} 
              to="/face-recognition" 
              active={location.pathname === "/face-recognition"}
            >
              Face Recognition
            </Nav.Link>
            <Nav.Link 
              as={Link} 
              to="/visualization" 
              active={location.pathname === "/visualization"}
            >
              Data Visualization
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar; 