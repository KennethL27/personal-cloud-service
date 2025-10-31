import { useEffect, useCallback } from 'react';

declare global {
  interface Window {
    google: {
      accounts: {
        id: {
          initialize: (config: {
            client_id: string;
            callback: (response: { credential?: string }) => void;
            auto_select?: boolean;
            cancel_on_tap_outside?: boolean;
          }) => void;
          renderButton: (element: HTMLElement, config: {
            theme?: string;
            size?: string;
            width?: string | number;
            text?: string;
            shape?: string;
            [key: string]: unknown;
          }) => void;
          prompt: () => void;
        };
      };
    };
  }
}

interface UseGoogleLoginProps {
  onSuccess: (token: string) => void;
  onError?: (error: string) => void;
  clientId: string;
}

export const useGoogleLogin = ({ onSuccess, onError, clientId }: UseGoogleLoginProps) => {
  const initializeGoogle = useCallback(() => {
    if (typeof window !== 'undefined' && window.google) {
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: (response: { credential?: string }) => {
          if (response.credential) {
            onSuccess(response.credential);
          } else {
            onError?.('No credential received from Google');
          }
        },
        auto_select: false,
        cancel_on_tap_outside: true,
      });
    }
  }, [clientId, onSuccess, onError]);

  const renderButton = useCallback((element: HTMLElement) => {
    if (typeof window !== 'undefined' && window.google) {
      window.google.accounts.id.renderButton(element, {
        theme: 'outline',
        size: 'large',
        width: '100%',
        text: 'signin_with',
        shape: 'rectangular',
      });
    }
  }, []);

  const prompt = useCallback(() => {
    if (typeof window !== 'undefined' && window.google) {
      window.google.accounts.id.prompt();
    }
  }, []);

  useEffect(() => {
    // Load Google Sign-In script if not already loaded
    if (typeof window !== 'undefined' && !window.google) {
      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      document.head.appendChild(script);

      script.onload = () => {
        initializeGoogle();
      };

      return () => {
        // Cleanup script if component unmounts
        if (document.head.contains(script)) {
          document.head.removeChild(script);
        }
      };
    } else if (window.google) {
      initializeGoogle();
    }
  }, [initializeGoogle]);

  return {
    renderButton,
    prompt,
    isGoogleLoaded: typeof window !== 'undefined' && !!window.google,
  };
};
