import React from 'react';

interface SettingsInfoProps {
  createdAt: string;
  updatedAt: string;
}

export function SettingsInfo({ createdAt, updatedAt }: SettingsInfoProps) {
  return (
    <div className="bg-gray-500 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-2">Settings Information</h3>
      <div className="text-sm text-gray-300 space-y-1">
        <p>Created: {new Date(createdAt).toLocaleString()}</p>
        <p>Last Updated: {new Date(updatedAt).toLocaleString()}</p>
      </div>
    </div>
  );
}