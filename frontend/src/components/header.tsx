'use client';

import Link from 'next/link';
import { useAuthContext } from '@/contexts/AuthContext';

export default function Header() {
  const { user, logout, isLoading } = useAuthContext();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <header className="bg-gray-800 text-white p-4">
      <nav className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">Personal Cloud Storage</h1>
        
        <div className="flex items-center gap-4">
          <ul className="flex gap-4">
            <li><Link href="/" className="hover:text-gray-300">Home</Link></li>
            <li><Link href="/browse" className="hover:text-gray-300">Browse</Link></li>
            <li><Link href="/settings" className="hover:text-gray-300">Settings</Link></li>
          </ul>
          
          {!isLoading && user && (
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                {user.picture && (
                  <img
                    src={user.picture}
                    alt={user.name || user.email}
                    className="w-8 h-8 rounded-full"
                  />
                )}
                <span className="text-sm text-gray-300">
                  {user.name || user.email}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm transition-colors"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>
    </header>
  );
}