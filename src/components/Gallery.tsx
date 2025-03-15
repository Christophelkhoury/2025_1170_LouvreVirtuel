import React from 'react';
import { Painting, GeneratedPainting } from '../types';
import { Sparkles, Info } from 'lucide-react';

interface GalleryProps {
  paintings: (Painting | GeneratedPainting)[];
}

export function Gallery({ paintings }: GalleryProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {paintings.map((painting) => (
        <div key={painting.id} className="bg-white rounded-lg shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-[1.02] hover:shadow-xl">
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
  );
}