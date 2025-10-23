import React from 'react';
import { FolderItem } from '@/lib/api/types';
import { FileItem } from './FileItem';
import { UploadCard } from './UploadCard';

interface FileGridProps {
  items: FolderItem[];
  onItemClick: (item: FolderItem) => void;
  onUpload: (files: File[]) => void;
  uploadLoading?: boolean;
}

export function FileGrid({ items, onItemClick, onUpload, uploadLoading = false }: FileGridProps) {
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
        
        {/* Upload card - placed after all files */}
        <UploadCard 
          onUpload={onUpload} 
          loading={uploadLoading} 
        />
      </div>
    </div>
  );
}