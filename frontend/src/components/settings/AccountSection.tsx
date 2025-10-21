import React from 'react';

type ViewMode = 'view' | 'edit';

interface User {
  name?: string;
  email: string;
}

interface AccountSectionProps {
  user: User | null;
  mode: ViewMode;
}

export function AccountSection({ user, mode }: AccountSectionProps) {
  return (
    <div className="bg-gray-500 rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Account Information</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Name</label>
          {mode === 'view' ? (
            <p className="text-gray-300">{user?.name || 'Not provided'}</p>
          ) : (
            <input
              type="text"
              value={user?.name || ''}
              disabled
              className="w-full px-3 py-2 bg-gray-600 text-gray-300 rounded border border-gray-400"
              placeholder="Name (read-only)"
            />
          )}
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Email</label>
          <p className="text-gray-300">{user?.email}</p>
          <p className="text-xs text-gray-400 mt-1">Email cannot be changed</p>
        </div>
      </div>
    </div>
  );
}
