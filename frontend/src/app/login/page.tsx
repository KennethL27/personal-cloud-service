'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { GoogleLoginButton } from '@/components/GoogleLoginButton';
import { useAuthContext } from '@/contexts/AuthContext';

export default function LoginPage() {
  const { isAuthenticated, isLoading, error, clearError } = useAuthContext();
  const router = useRouter();

  // Redirect if already authenticated
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, isLoading, router]);

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-800 flex items-center justify-center">
      <div className="max-w-md w-full space-y-8 p-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-bold text-white">
            Personal Cloud Service
          </h2>
          <p className="mt-2 text-sm text-gray-400">
            Sign in to access your files
          </p>
        </div>

        <div className="mt-8 space-y-6">
          {error && (
            <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded">
              <div className="flex justify-between items-center">
                <span>{error}</span>
                <button
                  onClick={clearError}
                  className="text-red-300 hover:text-red-100"
                >
                  ×
                </button>
              </div>
            </div>
          )}

          <div className="space-y-4">
            <GoogleLoginButton className="w-full" />
          </div>

          <div className="text-center">
            <p className="text-xs text-gray-500">
              Only authorized email addresses can access this service.
              <br />
              Contact your administrator if you need access.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
