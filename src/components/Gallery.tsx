import React, { useState } from 'react';
import { Painting, GeneratedPainting } from '../types';
import { Sparkles, Info, X } from 'lucide-react';

interface GalleryProps {
  paintings: (Painting | GeneratedPainting)[];
}

export function Gallery({ paintings }: GalleryProps) {
  const [selectedPainting, setSelectedPainting] = useState<Painting | GeneratedPainting | null>(null);

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {paintings.map((painting) => (
          <div 
            key={painting.id} 
            className="bg-white rounded-lg shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-[1.02] hover:shadow-xl cursor-pointer"
            onClick={() => setSelectedPainting(painting)}
          >
            <div className="relative aspect-[4/3] overflow-hidden">
              <img
                src={painting.imageUrl}
                alt={painting.title}
                className="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
              />
              {'prompt' in painting && (
                <div className="absolute top-2 right-2 bg-indigo-600 text-white px-2 py-1 rounded-full text-sm flex items-center gap-1 shadow-lg">
                  <Sparkles className="w-4 h-4" />
                  Généré par IA
                </div>
              )}
            </div>
            <div className="p-4">
              <h3 className="text-xl font-semibold mb-2 line-clamp-2">{painting.title}</h3>
              <p className="text-gray-600 line-clamp-1">{painting.artist}</p>
              <p className="text-gray-500 text-sm mb-3">{painting.year}</p>
              <div className="bg-gray-50 p-3 rounded-lg">
                <div className="flex items-center gap-2 text-gray-700 mb-1">
                  <Info className="w-4 h-4" />
                  <span className="font-medium">Description</span>
                </div>
                <p className="text-sm text-gray-600 line-clamp-3">{painting.description}</p>
              </div>
              {'prompt' in painting && (
                <div className="mt-2 p-2 bg-indigo-50 rounded-lg">
                  <p className="text-sm text-indigo-600 italic line-clamp-2">
                    Prompt : {painting.prompt}
                  </p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {selectedPainting && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-8" onClick={() => setSelectedPainting(null)}>
          <div className="relative max-w-3xl w-full max-h-[90vh] bg-white rounded-lg shadow-xl overflow-auto" onClick={e => e.stopPropagation()}>
            <div className="sticky top-0 z-10 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 pr-8">{selectedPainting.title}</h2>
              <button 
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                onClick={() => setSelectedPainting(null)}
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>
            <div className="p-6">
              <div className="aspect-[4/3] overflow-hidden rounded-lg mb-6">
                <img
                  src={selectedPainting.imageUrl}
                  alt={selectedPainting.title}
                  className="w-full h-full object-contain"
                />
              </div>
              <p className="text-lg text-gray-700 mb-1">{selectedPainting.artist}</p>
              <p className="text-gray-500 mb-4">{selectedPainting.year}</p>
              <div className="bg-gray-50 p-4 rounded-lg mb-4">
                <div className="flex items-center gap-2 text-gray-700 mb-2">
                  <Info className="w-5 h-5" />
                  <span className="font-medium">Description</span>
                </div>
                <p className="text-gray-600">{selectedPainting.description}</p>
              </div>
              {'prompt' in selectedPainting && (
                <div className="bg-indigo-50 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="w-5 h-5 text-indigo-600" />
                    <span className="font-medium text-indigo-900">Prompt IA</span>
                  </div>
                  <p className="text-indigo-700 italic">
                    {selectedPainting.prompt}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
