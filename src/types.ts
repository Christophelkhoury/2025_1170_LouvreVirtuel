export interface Painting {
  id: string;
  title: string;
  imageUrl: string;
  artist: string;
  year: string;
  description: string;
}

export interface PaintingStyle {
  id: string;
  name: string;
  description: string;
  paintings: Painting[];
}

export interface StyleSelection {
  style: PaintingStyle;
  selected: boolean;
}

export interface AIGenerationPrompt {
  style: string;
  subject: string;
  mood: string;
}

export interface GeneratedPainting extends Painting {
  prompt: string;
}