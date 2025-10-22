import React from 'react';
import { FolderItem } from '@/lib/api/types';
import { getFileIcon, formatDate, formatFileSize } from '../../lib/utils/fileHelpers';

interface FileItemProps {
  item: FolderItem;
  onClick: (item: FolderItem) => void;
}

export function FileItem({ item, onClick }: FileItemProps) {
  const isFolder = item.type === 'folder';
  
  return (
    <div
      className="bg-gray-600 rounded-lg p-4 hover:bg-gray-700 transition-colors cursor-pointer"
      onClick={() => onClick(item)}
    >
      <div className="text-center">
        <div className="text-4xl mb-2">
          {getFileIcon(item.name, isFolder)}
        </div>
        <h3 className="font-medium text-sm truncate" title={item.name}>
          {item.name}
        </h3>
        <p className="text-xs text-gray-400 mt-1">
          {isFolder ? 'Folder' : formatFileSize(item.size)}
        </p>
        <p className="text-xs text-gray-400">
          {formatDate(item.modified)}
        </p>
      </div>
    </div>
  );
}
