'use client';

import React, { createContext, useContext, ReactNode } from 'react';
import { useAuth } from '@/lib/api/hooks/useAuth';
import { AuthState, LoginResponse } from '@/lib/api/types';

interface AuthContextType extends AuthState {
  login: (googleToken: string) => Promise<LoginResponse>;
  logout: () => Promise<void>;
  verifyAuth: () => Promise<void>;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const auth = useAuth();

  return (
    <AuthContext.Provider value={auth}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};
