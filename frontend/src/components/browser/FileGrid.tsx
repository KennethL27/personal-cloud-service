import React from 'react';
import { FolderItem } from '@/lib/api/types';
import { FileItem } from './FileItem';

interface FileGridProps {
  items: FolderItem[];
  onItemClick: (item: FolderItem) => void;
}

export function FileGrid({ items, onItemClick }: FileGridProps) {
  return (
    <div className="bg-gray-500 rounded-lg shadow p-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {items.map((item) => (
          <FileItem
            key={item.name}
            item={item}
            onClick={onItemClick}
          />
        ))}
      </div>
    </div>
  );
}