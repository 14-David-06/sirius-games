// Tipos globales para el proyecto Sirius Games

export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Game {
  id: string;
  title: string;
  description: string;
  genre: string;
  releaseDate: Date;
  rating: number;
  imageUrl?: string;
  developer: string;
  platform: Platform[];
}

export interface Platform {
  id: string;
  name: string;
  icon?: string;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  error?: string;
}

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ComponentProps {
  className?: string;
  children?: React.ReactNode;
}