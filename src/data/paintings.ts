import { PaintingStyle } from '../types';

export const paintingCollections: PaintingStyle[] = [
  {
    id: 'impressionism',
    name: 'Impressionnisme',
    description: 'Caractérisé par de petits coups de pinceau et l\'accent mis sur la lumière',
    paintings: [
      {
        id: 'monet-1',
        title: 'Les Nymphéas',
        imageUrl: 'https://images.unsplash.com/photo-1580136579312-94651dfd596d',
        artist: 'Inspiré de Claude Monet',
        year: '2024',
        description: 'Une interprétation des célèbres nymphéas de Giverny, capturant la lumière et les reflets sur l\'eau.'
      },
      {
        id: 'monet-2',
        title: 'Le Jardin',
        imageUrl: 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5',
        artist: 'Inspiré de Claude Monet',
        year: '2024',
        description: 'Un chemin de jardin paisible, peint dans le style impressionniste caractéristique de Monet.'
      },
      {
        id: 'monet-3',
        title: 'Soleil Couchant',
        imageUrl: 'https://images.unsplash.com/photo-1507637246364-d8fce4a9850a',
        artist: 'Inspiré de Claude Monet',
        year: '2024',
        description: 'Un coucher de soleil vibrant sur l\'eau, capturant les reflets dorés et les nuances du ciel.'
      },
      {
        id: 'monet-4',
        title: 'Brume Matinale',
        imageUrl: 'https://images.unsplash.com/photo-1500462918059-b1a0cb512f1d',
        artist: 'Inspiré de Claude Monet',
        year: '2024',
        description: 'Une scène paisible du matin avec la brume qui se lève sur un paysage impressionniste.'
      }
    ]
  },
  {
    id: 'abstract',
    name: 'Art Abstrait',
    description: 'Art non représentatif utilisant formes, couleurs et compositions',
    paintings: [
      {
        id: 'kandinsky-1',
        title: 'Composition VIII',
        imageUrl: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262',
        artist: 'Inspiré de Vassily Kandinsky',
        year: '2024',
        description: 'Une composition dynamique de formes géométriques et de couleurs vives, typique du style de Kandinsky.'
      },
      {
        id: 'mondrian-1',
        title: 'Composition en Grid',
        imageUrl: 'https://images.unsplash.com/photo-1557672172-298e090bd0f1',
        artist: 'Inspiré de Piet Mondrian',
        year: '2024',
        description: 'Une œuvre géométrique abstraite utilisant des lignes droites et des couleurs primaires.'
      },
      {
        id: 'abstract-3',
        title: 'Flux Cosmique',
        imageUrl: 'https://images.unsplash.com/photo-1515405295579-ba7b45403062',
        artist: 'Art Contemporain',
        year: '2024',
        description: 'Une explosion de couleurs et de formes évoquant le mouvement des galaxies et des nébuleuses.'
      },
      {
        id: 'abstract-4',
        title: 'Résonance Chromatique',
        imageUrl: 'https://images.unsplash.com/photo-1499781350541-7783f6c6a0c8',
        artist: 'Art Moderne',
        year: '2024',
        description: 'Une exploration des harmonies de couleurs à travers des formes organiques abstraites.'
      }
    ]
  },
  {
    id: 'surrealism',
    name: 'Surréalisme',
    description: 'Imagerie onirique et inconsciente',
    paintings: [
      {
        id: 'dali-1',
        title: 'Le Temps Qui Fond',
        imageUrl: 'https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb',
        artist: 'Inspiré de Salvador Dalí',
        year: '2024',
        description: 'Une exploration surréaliste du temps et de la réalité, dans le style caractéristique de Dalí.'
      },
      {
        id: 'magritte-1',
        title: 'Le Faux Miroir',
        imageUrl: 'https://images.unsplash.com/photo-1547891654-e66ed7ebb968',
        artist: 'Inspiré de René Magritte',
        year: '2024',
        description: 'Une œuvre énigmatique jouant sur la perception et la réalité, typique de Magritte.'
      },
      {
        id: 'surreal-3',
        title: 'Rêves Liquides',
        imageUrl: 'https://images.unsplash.com/photo-1494122353634-c310f45a6d3c',
        artist: 'Art Contemporain',
        year: '2024',
        description: 'Une fusion onirique entre l\'eau et les éléments du rêve, créant un paysage surréaliste fluide.'
      },
      {
        id: 'surreal-4',
        title: 'Métamorphose Nocturne',
        imageUrl: 'https://images.unsplash.com/photo-1518998053901-5348d3961a04',
        artist: 'École Moderne',
        year: '2024',
        description: 'Une transformation surréaliste d\'objets quotidiens dans un contexte nocturne mystérieux.'
      }
    ]
  },
  {
    id: 'renaissance',
    name: 'Renaissance',
    description: 'Renouveau classique avec perspective et réalisme',
    paintings: [
      {
        id: 'davinci-1',
        title: 'Étude de Portrait',
        imageUrl: 'https://images.unsplash.com/photo-1578927333046-8c49c3c91b11',
        artist: 'Inspiré de Léonard de Vinci',
        year: '2024',
        description: 'Une étude détaillée du visage humain, reflétant la précision anatomique de la Renaissance.'
      },
      {
        id: 'botticelli-1',
        title: 'Vénus Naissante',
        imageUrl: 'https://images.unsplash.com/photo-1579783902439-0f26d8526508',
        artist: 'Inspiré de Sandro Botticelli',
        year: '2024',
        description: 'Une réinterprétation de la naissance de Vénus, capturant la grâce et l\'élégance de Botticelli.'
      },
      {
        id: 'renaissance-3',
        title: 'L\'Atelier du Maître',
        imageUrl: 'https://images.unsplash.com/photo-1577083552431-6e5fd75a9370',
        artist: 'École Florentine',
        year: '2024',
        description: 'Une scène d\'atelier représentant les techniques et l\'ambiance de la Renaissance italienne.'
      },
      {
        id: 'renaissance-4',
        title: 'Méditation Classique',
        imageUrl: 'https://images.unsplash.com/photo-1569172122301-bc5008bc09c5',
        artist: 'École Vénitienne',
        year: '2024',
        description: 'Un portrait contemplatif dans le style des grands maîtres de la Renaissance.'
      }
    ]
  },
  {
    id: 'postimpressionism',
    name: 'Post-Impressionnisme',
    description: 'Couleurs audacieuses et impact émotionnel',
    paintings: [
      {
        id: 'vangogh-1',
        title: 'Interprétation de La Nuit Étoilée',
        imageUrl: 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5',
        artist: 'Inspiré de Vincent van Gogh',
        year: '2024',
        description: 'Une vision moderne du chef-d\'œuvre de Van Gogh, avec ses tourbillons caractéristiques.'
      },
      {
        id: 'cezanne-1',
        title: 'Nature Morte aux Pommes',
        imageUrl: 'https://images.unsplash.com/photo-1579783902438-b80a3d02c67f',
        artist: 'Inspiré de Paul Cézanne',
        year: '2024',
        description: 'Une nature morte géométrique dans le style de Cézanne, explorant la forme et la perspective.'
      },
      {
        id: 'postimpressionism-3',
        title: 'Champs de Lavande',
        imageUrl: 'https://images.unsplash.com/photo-1499002238440-d264edd596ec',
        artist: 'École Provençale',
        year: '2024',
        description: 'Une vue vibrante des champs de lavande du sud de la France dans un style post-impressionniste.'
      },
      {
        id: 'postimpressionism-4',
        title: 'Café de Nuit',
        imageUrl: 'https://images.unsplash.com/photo-1517457373958-b7bdd4587205',
        artist: 'Style Moderne',
        year: '2024',
        description: 'Une scène nocturne de café avec des couleurs intenses et des coups de pinceau expressifs.'
      }
    ]
  },
  {
    id: 'cubism',
    name: 'Cubisme',
    description: 'Perspectives multiples et formes géométriques',
    paintings: [
      {
        id: 'picasso-1',
        title: 'Portrait Géométrique',
        imageUrl: 'https://images.unsplash.com/photo-1557672172-298e090bd0f1',
        artist: 'Inspiré de Pablo Picasso',
        year: '2024',
        description: 'Un portrait cubiste fragmenté, montrant plusieurs angles simultanément.'
      },
      {
        id: 'braque-1',
        title: 'Nature Morte Fragmentée',
        imageUrl: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262',
        artist: 'Inspiré de Georges Braque',
        year: '2024',
        description: 'Une composition cubiste complexe décomposant les objets en formes géométriques.'
      },
      {
        id: 'cubism-3',
        title: 'Jazz Cubique',
        imageUrl: 'https://images.unsplash.com/photo-1494232410401-ad00d5433cfa',
        artist: 'École Moderne',
        year: '2024',
        description: 'Une interprétation cubiste de musiciens de jazz, décomposant les instruments et les formes.'
      },
      {
        id: 'cubism-4',
        title: 'Ville Fragmentée',
        imageUrl: 'https://images.unsplash.com/photo-1501084817091-a4f3d1d19e07',
        artist: 'Style Contemporain',
        year: '2024',
        description: 'Un paysage urbain décomposé en formes géométriques selon les principes du cubisme.'
      }
    ]
  },
  {
    id: 'contemporary',
    name: 'Art Contemporain',
    description: 'Interprétations modernes et techniques mixtes',
    paintings: [
      {
        id: 'contemporary-1',
        title: 'Ère Numérique',
        imageUrl: 'https://images.unsplash.com/photo-1549490349-8643362247b5',
        artist: 'Collectif d\'Artistes Modernes',
        year: '2024',
        description: 'Une exploration de l\'intersection entre l\'art traditionnel et la technologie moderne.'
      },
      {
        id: 'contemporary-2',
        title: 'Expression Urbaine',
        imageUrl: 'https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8',
        artist: 'Mouvement Street Art',
        year: '2024',
        description: 'Une œuvre contemporaine reflétant la vie urbaine et la culture moderne.'
      },
      {
        id: 'contemporary-3',
        title: 'Fusion Digitale',
        imageUrl: 'https://images.unsplash.com/photo-1551913902-c92207136625',
        artist: 'Art Numérique',
        year: '2024',
        description: 'Une fusion entre l\'art traditionnel et les médias numériques, créant une expérience immersive.'
      },
      {
        id: 'contemporary-4',
        title: 'Échos Urbains',
        imageUrl: 'https://images.unsplash.com/photo-1501084291732-13b1ba8f0ebc',
        artist: 'Nouveau Réalisme',
        year: '2024',
        description: 'Une réflexion sur la vie urbaine moderne à travers des techniques mixtes contemporaines.'
      }
    ]
  }
];