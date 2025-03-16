import React, { useState } from 'react';
import { PaintingStyle, GeneratedPainting } from '../types';
import { Wand2, Loader2, AlertCircle } from 'lucide-react';

interface AIGeneratorProps {
  style: PaintingStyle;
  onGenerated: (painting: GeneratedPainting) => void;
}

export function AIGenerator({ style, onGenerated }: AIGeneratorProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<{ message: string; details?: string } | null>(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);

    try {
      // ✅ Fix: Use production URL if available, fallback to development URL
      const apiUrl = import.meta.env.VITE_PRODUCTION_API_URL || import.meta.env.VITE_API_URL;
      if (!apiUrl) {
        throw new Error("API URL is not configured");
      }

      console.log(`Using API URL: ${apiUrl}`); // Debugging info

      const response = await fetch(`${apiUrl}/api/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",  // ✅ Fix: Ensures the API responds with JSON
        },
        body: JSON.stringify({
          prompt: `An artwork in the style of ${style.name}`, // ✅ Fix: Send a proper prompt
          width: 512,  
          height: 512, 
          steps: 30  
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log("API Response:", data); // ✅ Debugging the response

      if (!data.imageUrl) {
  console.error("🚨 No image URL received! Full response:", data);
  throw new Error("AI did not return an image. Please try again.");
}


      const generatedPainting: GeneratedPainting = {
        id: `ai-${Date.now()}`,
        title: `Peinture IA en ${style.name}`,
        imageUrl: data.imageUrl,
        artist: `IA dans le style ${style.name}`,
        year: "2024",
        description: `Une œuvre générée automatiquement dans le style ${style.name}.`,
        prompt: data.prompt,
      };

      onGenerated(generatedPainting);
    } catch (err) {
      console.error("Generation Error:", err);

      let errorMessage = "Failed to generate image";
      let errorDetails = "An unexpected error occurred";

      if (err instanceof Error) {
        if (err.message === "Failed to fetch") {
          errorMessage = "Could not connect to the server";
          errorDetails = "The server might be offline or not accessible. Please try again later.";
        } else if (err.message === "API URL is not configured") {
          errorMessage = "Configuration Error";
          errorDetails = "The API URL is not properly configured in the environment variables";
        } else {
          errorDetails = err.message;
        }
      }

      setError({
        message: errorMessage,
        details: errorDetails,
      });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
      <div className="flex items-center gap-2 mb-6">
        <Wand2 className="w-6 h-6 text-indigo-600" />
        <h2 className="text-2xl font-semibold">Générateur d'Art IA</h2>
      </div>

      <div className="space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex items-center gap-2 text-red-700">
              <AlertCircle className="w-5 h-5" />
              <p className="font-medium">{error.message}</p>
            </div>
            {error.details && (
              <p className="mt-1 text-sm text-red-600 ml-7">{error.details}</p>
            )}
          </div>
        )}

        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg font-medium"
        >
          {isGenerating ? (
            <>
              <Loader2 className="w-6 h-6 animate-spin" />
              Génération en cours...
            </>
          ) : (
            <>
              <Wand2 className="w-6 h-6" />
              Générer une peinture {style.name}
            </>
          )}
        </button>
      </div>
    </div>
  );
}
