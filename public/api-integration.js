/**
 * API integration with FinAI backend
 * This simplified version works with the new tool step process
 */

// API endpoint configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Initialize the API integration
document.addEventListener('DOMContentLoaded', function() {
  console.log('Initializing FinAI backend integration');
  
  // The main functionality is now integrated directly into the tool step process
  // This script only needs to make sure the API endpoint is properly configured
  
  // Check if window.toolState exists (set by the new tool step process)
  if (window.toolState) {
    console.log('Tool state initialized, integration ready');
  } else {
    console.warn('Tool state not found. Make sure to load script.js before api-integration.js');
  }
});

// Optional: You can add specialized API functions here if needed