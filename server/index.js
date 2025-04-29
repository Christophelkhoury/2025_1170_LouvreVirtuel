import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express();
const port = 10000;

// Enable CORS
app.use(cors());
app.use(express.json());

// Get API key from environment variables
const STABLE_DIFFUSION_API_KEY = process.env.STABLE_DIFFUSION_API_KEY;
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
        apiKeyStatus
    });
});

// Enhanced API key verification middleware
const verifyApiKey = (req, res, next) => {
    if (!STABLE_DIFFUSION_API_KEY) {
        return res.status(401).json({
            error: 'API Key Missing',
            details: 'Stable Diffusion API key is not configured'
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

    if (!style) {
      return res.status(400).json({
        error: 'Missing parameter',
        details: 'Style parameter is required'
      });
    }

    if (!STABLE_DIFFUSION_API_KEY) {
      return res.status(401).json({
        error: 'API Key Missing',
        details: 'Stable Diffusion API key is not configured'
      });
    }

    console.log(`Generating image for style: ${style}`);
    console.log('Making request to Stability AI...');

    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${STABLE_DIFFUSION_API_KEY}`
      },
      body: JSON.stringify({
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

    if (!data.artifacts || !data.artifacts[0] || !data.artifacts[0].base64) {
      console.error('Invalid API Response:', data);
      return res.status(502).json({
        error: 'Invalid API response',
        details: 'Response did not contain image data',
        response: data
      });
    }

    console.log('Successfully generated image');
    res.json({
      imageUrl: `data:image/png;base64,${data.artifacts[0].base64}`,
      prompt: `${style} style painting`
    });

  } catch (error) {
    console.error('Server Error:', error);
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
  console.log('Stable Diffusion API Key status:', isValidApiKey(STABLE_DIFFUSION_API_KEY) ? 'valid format' : 'invalid format');
}).on('error', (error) => {
  console.error('Server failed to start:', error);
  process.exit(1);
});