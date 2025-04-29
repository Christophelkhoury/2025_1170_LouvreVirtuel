import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express();
const port = 10000;

// Enable CORS
app.use(cors());
app.use(express.json());

// Get API key from environment variables
const STABLE_DIFFUSION_API_KEY = process.env.STABILITY_API_KEY;
const API_ENDPOINT = 'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image';

// Validate API key format
const isValidApiKey = (key) => {
    return typeof key === 'string' && key.length > 20;
};

// Health check endpoint with API key status
app.get('/api/status', (req, res) => {
    const apiKeyStatus = isValidApiKey(STABLE_DIFFUSION_API_KEY) ? 'valid format' : 'invalid format';
    res.json({
        status: 'healthy',
        apiKeyStatus,
        message: 'Using Stability AI API for image generation'
    });
});

// Enhanced API key verification middleware
const verifyApiKey = (req, res, next) => {
    if (!STABLE_DIFFUSION_API_KEY) {
        return res.status(401).json({
            error: 'API Key Missing',
            details: 'Stability AI API key is not configured'
        });
    }

    if (!isValidApiKey(STABLE_DIFFUSION_API_KEY)) {
        return res.status(401).json({
            error: 'API Key Format Error',
            details: 'Invalid API key format'
        });
    }

    next();
};

// Apply API key verification to all routes
app.use('/api', verifyApiKey);

app.post('/api/generate', async (req, res) => {
  try {
    const { style } = req.body;
    console.log('Received request with style:', style);

    if (!style) {
      console.error('Style parameter missing in request');
      return res.status(400).json({
        error: 'Missing parameter',
        details: 'Style parameter is required'
      });
    }

    if (!STABLE_DIFFUSION_API_KEY) {
      console.error('API Key Missing: STABILITY_API_KEY is not set in environment');
      return res.status(401).json({
        error: 'API Key Missing',
        details: 'Stability AI API key is not configured'
      });
    }

    console.log('API Key present:', STABLE_DIFFUSION_API_KEY ? 'Yes' : 'No');
    console.log(`Generating image for style: ${style}`);
    console.log('Making request to Stability AI API:', API_ENDPOINT);

    try {
      const requestBody = {
        text_prompts: [
          {
            text: `Create a ${style} style painting. The image should be highly detailed and artistic, following the characteristics of ${style} art movement.`,
            weight: 1
          }
        ],
        cfg_scale: 7,
        height: 1024,
        width: 1024,
        samples: 1,
        steps: 30,
        seed: seed ? abs(hash(seed)) % (2**32) : null
      };

      console.log('Request body:', JSON.stringify(requestBody, null, 2));

      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Bearer ${STABLE_DIFFUSION_API_KEY}`
        },
        body: JSON.stringify(requestBody)
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', Object.fromEntries(response.headers));

      const data = await response.json();
      
      console.log('Stability AI Response data:', JSON.stringify(data, null, 2));

      if (!response.ok) {
        const errorDetails = {
          statusCode: response.status,
          apiError: data.message || data.error || response.statusText,
          requestId: response.headers.get('x-request-id'),
          timestamp: new Date().toISOString(),
          endpoint: API_ENDPOINT,
          requestBody: requestBody
        };

        console.error('Stability AI API Error:', errorDetails);

        return res.status(response.status).json({
          error: 'Stability AI API Error',
          details: errorDetails
        });
      }

      if (!data.artifacts || !data.artifacts[0] || !data.artifacts[0].base64) {
        console.error('Invalid API Response - No image data:', data);
        return res.status(502).json({
          error: 'Invalid API response',
          details: 'Response did not contain image data',
          response: data,
          endpoint: API_ENDPOINT
        });
      }

      console.log('Successfully generated image');
      res.json({
        imageUrl: `data:image/png;base64,${data.artifacts[0].base64}`,
        prompt: `${style} style painting`
      });

    } catch (fetchError) {
      console.error('Fetch Error:', {
        message: fetchError.message,
        stack: fetchError.stack,
        endpoint: API_ENDPOINT
      });
      return res.status(500).json({
        error: 'Network Error',
        details: fetchError.message,
        endpoint: API_ENDPOINT
      });
    }

  } catch (error) {
    console.error('Server Error:', {
      message: error.message,
      stack: error.stack
    });
    res.status(500).json({
      error: 'Server error',
      details: error.message
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

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
  console.log('API available at http://localhost:' + port);
  console.log('Stability AI API Key status:', isValidApiKey(STABLE_DIFFUSION_API_KEY) ? 'valid format' : 'invalid format');
}).on('error', (error) => {
  console.error('Server failed to start:', error);
  process.exit(1);
});