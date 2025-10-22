'use client';

import { useEffect, useState } from 'react';
import { useListFolderItems } from '@/lib/api/hooks/useListFolderItems';
import { useUserSettings } from '@/lib/api/hooks/useUserSettings';
import { usePathNavigation } from '@/lib/api/hooks/usePathNavigation';
import { useFileStream } from '@/lib/api/hooks/useFileStream';
import { FolderItem } from '@/lib/api/types';
import { BrowserHeader } from '@/components/browser/BrowserHeader';
import { ErrorMessage } from '@/components/browser/ErrorMessage';
import { LoadingState } from '@/components/browser/LoadingState';
import { EmptyState } from '@/components/browser/EmptyState';
import { FileGrid } from '@/components/browser/FileGrid';
import FileStreamDisplay from '@/components/FileStreamDisplay';

export default function FileBrowserNew() {
  const { data: folderData, loading, error, listFolderItems } = useListFolderItems();
  const { settings, fetchSettings } = useUserSettings();
  const { currentPath, navigateToFolder, navigateBack, getPathDisplay } = usePathNavigation();
  const { streamFile, data: streamData, loading: streamLoading, error: streamError } = useFileStream();

  const [selectedFile, setSelectedFile] = useState<FolderItem | null>(null);

  useEffect(() => {
    listFolderItems(currentPath);
    fetchSettings();
  }, [currentPath]);

  const handleItemClick = async (item: FolderItem) => {
    if (item.type === 'folder') {
      setSelectedFile(null);
      navigateToFolder(item.relative_path);
    } else if (item.type === 'file') {
      try {
        await streamFile(item.relative_path);
        setSelectedFile(item)
      }
      catch (error) {
        console.error('Failed to stream file:', error);
      }
    }
  };

  const handleBackToBrowser = () => {
    setSelectedFile(null);
  };

  const pathDisplay = getPathDisplay(settings?.hard_drive_path_selection);
  const itemCount = folderData?.length || 0;

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <BrowserHeader
        currentPath={currentPath}
        pathDisplay={pathDisplay || ''}
        itemCount={itemCount}
        onBack={selectedFile ? handleBackToBrowser : navigateBack}
      />

      {error && <ErrorMessage message={error} />}

      {loading && <LoadingState />}

      {!loading && !error && itemCount === 0 && <EmptyState />}

      {!loading && !error && folderData && folderData.length > 0 && (
        <FileGrid items={folderData} onItemClick={handleItemClick} />
      )}

      {selectedFile && (
        <FileStreamDisplay 
          streamData={streamData}
          streamError={streamError}
          streamLoading={streamLoading}
        />
      )}
    </div>
  );
}