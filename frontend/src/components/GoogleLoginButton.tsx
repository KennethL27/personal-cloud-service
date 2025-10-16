'use client';

import React, { useRef, useEffect } from 'react';
import { useGoogleLogin } from '@/lib/api/hooks/useGoogleLogin';
import { useAuthContext } from '@/contexts/AuthContext';

interface GoogleLoginButtonProps {
  className?: string;
}

export const GoogleLoginButton: React.FC<GoogleLoginButtonProps> = ({ className = '' }) => {
  const buttonRef = useRef<HTMLDivElement>(null);
  const { login, clearError } = useAuthContext();

  const handleSuccess = async (token: string) => {
    try {
      clearError();
      await login(token);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleError = (error: string) => {
    console.error('Google login error:', error);
  };

  const { renderButton, isGoogleLoaded } = useGoogleLogin({
    onSuccess: handleSuccess,
    onError: handleError,
    clientId: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '',
  });

  useEffect(() => {
    if (isGoogleLoaded && buttonRef.current) {
      renderButton(buttonRef.current);
    }
  }, [isGoogleLoaded, renderButton]);

  return (
    <div className={`google-login-container ${className}`}>
      <div ref={buttonRef} className="w-full"></div>
      {!isGoogleLoaded && (
        <div className="text-center text-gray-400 text-sm">
          Loading Google Sign-In...
        </div>
      )}
    </div>
  );
};
