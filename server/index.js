import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import fetch from 'node-fetch';

dotenv.config();

const app = express();

// Enhanced CORS configuration with specific origin and credentials
app.use(cors({
  origin: ['http://localhost:5173', 'https://stackblitz.com'],
  credentials: true,
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());

const STABILITY_API_KEY = process.env.STABILITY_AI_API_KEY;
const API_ENDPOINT = "https://api.stability.ai/v2beta/stable-image/generate/sd3";

// Validate API key format
const isValidApiKey = (key) => {
  return typeof key === 'string' && key.startsWith('sk-') && key.length > 20;
};

// Health check endpoint with API key status
app.get('/', (req, res) => {
  const apiKeyStatus = isValidApiKey(STABILITY_API_KEY) ? 'valid format' : 'invalid format';
  res.json({
    status: 'healthy',
    message: 'AI Art Generator API is running',
    apiKeyStatus
  });
});

// Enhanced API key verification middleware
app.use('/api', (req, res, next) => {
  if (!STABILITY_API_KEY) {
    return res.status(500).json({
      error: 'API Configuration Error',
      details: 'Stability AI API key is not configured'
    });
  }
  
  if (!isValidApiKey(STABILITY_API_KEY)) {
    return res.status(500).json({
      error: 'API Key Format Error',
      details: 'The provided Stability AI API key appears to be invalid'
    });
  }
  
  next();
});

app.post('/api/generate', async (req, res) => {
  try {
    const { style } = req.body;

    if (!style) {
      return res.status(400).json({
        error: 'Missing parameter',
        details: 'Style parameter is required'
      });
    }

    console.log(`Generating image for style: ${style}`);
    console.log('Making request to Stability AI...');

    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${STABILITY_API_KEY}`
      },
      body: JSON.stringify({
        prompt: `Create a ${style} style painting. The image should be highly detailed and artistic, following the characteristics of ${style} art movement.`,
        output_format: 'jpeg'
      })
    });

    const data = await response.json();
    
    // Log the full response for debugging
    console.log('Stability AI Response:', {
      status: response.status,
      headers: Object.fromEntries(response.headers),
      body: data
    });

    if (!response.ok) {
      // Enhanced error reporting
      const errorDetails = {
        statusCode: response.status,
        apiError: data.message || data.error || response.statusText,
        requestId: response.headers.get('x-request-id'),
        timestamp: new Date().toISOString()
      };

      console.error('Stability AI API Error:', errorDetails);

      return res.status(response.status).json({
        error: 'Stability AI API Error',
        details: errorDetails
      });
    }

    if (!data.image_url) {
      console.error('Invalid API Response:', data);
      return res.status(502).json({
        error: 'Invalid API response',
        details: 'Response did not contain image URL',
        response: data
      });
    }

    console.log('Successfully generated image');
    res.json({
      imageUrl: data.image_url,
      prompt: `${style} style painting`
    });

  } catch (error) {
    console.error('Server Error:', error);
    res.status(500).json({
      error: 'Server error',
      details: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

// Error handling for process termination
process.on('SIGINT', () => {
  console.log('Gracefully shutting down server...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('Gracefully shutting down server...');
  process.exit(0);
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log('API available at http://localhost:' + PORT);
  console.log('Stability AI API Key status:', isValidApiKey(STABILITY_API_KEY) ? 'valid format' : 'invalid format');
}).on('error', (error) => {
  console.error('Server failed to start:', error);
  process.exit(1);
});