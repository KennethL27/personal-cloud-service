'use client';

import { useEffect, useState } from 'react';
import { useListFolderItems } from '@/lib/api/hooks/useListFolderItems';
import { useUserSettings } from '@/lib/api/hooks/useUserSettings';
import { usePathNavigation } from '@/lib/api/hooks/usePathNavigation';
import { useFileStream } from '@/lib/api/hooks/useFileStream';
import { useFileUpload } from '@/lib/api/hooks/useFileUpload';
import { FolderItem } from '@/lib/api/types';
import { BrowserHeader } from '@/components/browser/BrowserHeader';
import { ErrorMessage } from '@/components/browser/ErrorMessage';
import { LoadingState } from '@/components/browser/LoadingState';
import { EmptyState } from '@/components/browser/EmptyState';
import { FileGrid } from '@/components/browser/FileGrid';
import { Banner } from '@/components/browser/Banner';
import FileStreamDisplay from '@/components/FileStreamDisplay';

export default function FileBrowserNew() {
  const { data: folderData, loading, error, listFolderItems } = useListFolderItems();
  const { settings, fetchSettings } = useUserSettings();
  const { currentPath, navigateToFolder, navigateBack, getPathDisplay } = usePathNavigation();
  const { streamFile, data: streamData, loading: streamLoading, error: streamError } = useFileStream();
  const { uploadFiles, loading: uploadLoading, error: uploadError, data: uploadData } = useFileUpload();

  const [selectedFile, setSelectedFile] = useState<FolderItem | null>(null);
  const [banner, setBanner] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

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

  const handleUpload = async (files: File[]) => {
    try {
      // Construct the full path by combining user's hard drive path with current relative path
      const basePath = settings?.hard_drive_path_selection || '';
      const fullUploadPath = currentPath ? `${basePath}/${currentPath}` : basePath;
      
      await uploadFiles(files, fullUploadPath);
      // Refresh the folder view to show new files
      await listFolderItems(currentPath);
      // Show success banner
      setBanner({
        message: `Successfully uploaded ${files.length} file${files.length > 1 ? 's' : ''}`,
        type: 'success'
      });
    } catch (error) {
      // Show error banner
      setBanner({
        message: uploadError || 'Failed to upload files',
        type: 'error'
      });
    }
  };

  const handleBackToBrowser = () => {
    setSelectedFile(null);
  };

  const closeBanner = () => {
    setBanner(null);
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

      {banner && (
        <Banner
          message={banner.message}
          type={banner.type}
          onClose={closeBanner}
        />
      )}

      {error && <ErrorMessage message={error} />}

      {loading && <LoadingState />}

      {!loading && !error && itemCount === 0 && <EmptyState />}

      {!loading && !error && folderData && folderData.length > 0 && (
        <FileGrid 
          items={folderData} 
          onItemClick={handleItemClick}
          onUpload={handleUpload}
          uploadLoading={uploadLoading}
        />
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