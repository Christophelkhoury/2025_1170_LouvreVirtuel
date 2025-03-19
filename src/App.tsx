import React, { useState } from 'react';
import { Gallery } from './components/Gallery';
import { StyleSelector } from './components/StyleSelector';
import { AIGenerator } from './components/AIGenerator';
import { Museum3D } from './components/Museum3D';
import { paintingCollections } from './data/paintings';
import { PaintingStyle, Painting, GeneratedPainting } from './types';
import { Palette, Box, Image } from 'lucide-react';

function App() {
  const [selectedStyle, setSelectedStyle] = useState<PaintingStyle | null>(null);
  const [generatedPaintings, setGeneratedPaintings] = useState<GeneratedPainting[]>([]);
  const [view, setView] = useState<'gallery' | '3d'>('gallery');

  const handleGenerated = (painting: GeneratedPainting) => {
    setGeneratedPaintings(prev => [painting, ...prev]);
  };

  const getAllPaintings = (): (Painting | GeneratedPainting)[] => {
    if (!selectedStyle) return [];
    const currentStylePaintings = [...selectedStyle.paintings];
    const currentStyleGeneratedPaintings = generatedPaintings.filter(
      p => p.style === selectedStyle.id
    );
    return [...currentStyleGeneratedPaintings, ...currentStylePaintings];
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Palette className="w-8 h-8 text-indigo-600" />
              <h1 className="text-3xl font-bold text-gray-900">Musée Virtuel</h1>
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => setView('gallery')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                  view === 'gallery' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700'
                }`}
              >
                <Image className="w-5 h-5" />
                Galerie
              </button>
              <button
                onClick={() => setView('3d')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                  view === '3d' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700'
                }`}
              >
                <Box className="w-5 h-5" />
                Musée 3D
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Sélectionnez un Style d'Art</h2>
          <StyleSelector
            styles={paintingCollections}
            onStyleSelect={setSelectedStyle}
            selectedStyle={selectedStyle}
          />
        </div>

        {selectedStyle && (
          <>
            <AIGenerator 
              style={selectedStyle}
              onGenerated={handleGenerated}
            />
            {view === 'gallery' ? (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-2xl font-semibold mb-6">Galerie {selectedStyle.name}</h2>
                <Gallery paintings={getAllPaintings()} />
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                <Museum3D paintings={getAllPaintings()} />
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
