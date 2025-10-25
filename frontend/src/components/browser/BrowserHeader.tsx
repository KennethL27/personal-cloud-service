import React, { useState } from 'react';
import { ShareModal } from '@/components/share_modal/ShareModal';
import { useShare } from '@/lib/api/hooks/useShare';

interface BrowserHeaderProps {
  currentPath: string;
  pathDisplay: string;
  itemCount: number;
  onBack: () => void;
}

export function BrowserHeader({ 
  currentPath, 
  pathDisplay, 
  itemCount, 
  onBack 
}: BrowserHeaderProps) {
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);
  const { share, loading: shareLoading, error: shareError, reset: resetShare } = useShare();

  const handleShare = async (data: { name: string; email: string; hard_drive_path_selection: string }) => {
    await share(data);
    resetShare();
  };

  const handleCloseShareModal = () => {
    setIsShareModalOpen(false);
    resetShare();
  };

  return (
    <>
      <div className="bg-gray-500 rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            {currentPath && (
              <button
                onClick={onBack}
                className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
              >
                ← Back
              </button>
            )}
            <h2 className="text-xl font-semibold">
              {pathDisplay}
            </h2>
            <div className="text-sm text-gray-300">
              {itemCount} item{itemCount !== 1 ? 's' : ''}
            </div>
          </div>
          
          <button
            onClick={() => setIsShareModalOpen(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            <span>Share</span>
          </button>
        </div>
      </div>

      <ShareModal
        isOpen={isShareModalOpen}
        onClose={handleCloseShareModal}
        pathDisplay={pathDisplay}
        onShare={handleShare}
        loading={shareLoading}
        error={shareError}
      />
    </>
  );
}