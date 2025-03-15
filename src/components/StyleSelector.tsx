import React from 'react';
import { PaintingStyle, StyleSelection } from '../types';
import { Palette } from 'lucide-react';

interface StyleSelectorProps {
  styles: PaintingStyle[];
  onStyleSelect: (style: PaintingStyle) => void;
  selectedStyle: PaintingStyle | null;
}

export function StyleSelector({ styles, onStyleSelect, selectedStyle }: StyleSelectorProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
      {styles.map((style) => (
        <button
          key={style.id}
          className={`p-3 rounded-lg cursor-pointer transition-all duration-300 text-left ${
            selectedStyle?.id === style.id
              ? 'bg-indigo-100 ring-2 ring-indigo-500'
              : 'bg-white hover:bg-gray-50 hover:ring-2 hover:ring-gray-200'
          }`}
          onClick={() => onStyleSelect(style)}
        >
          <div className="flex items-center gap-2 mb-1">
            <Palette className="w-4 h-4 text-indigo-600" />
            <h3 className="text-sm font-medium">{style.name}</h3>
          </div>
          <p className="text-xs text-gray-600 line-clamp-2">{style.description}</p>
        </button>
      ))}
    </div>
  );
}