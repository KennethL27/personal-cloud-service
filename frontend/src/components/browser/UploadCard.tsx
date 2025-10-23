import React, { useRef } from 'react';

interface UploadCardProps {
  onUpload: (files: File[]) => void;
  loading?: boolean;
}

export function UploadCard({ onUpload, loading = false }: UploadCardProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    if (files.length > 0) {
      onUpload(files);
    }
    // Reset the input so the same file can be selected again
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <>
      <div
        className={`bg-blue-600 rounded-lg p-4 hover:bg-blue-700 transition-colors cursor-pointer border-2 border-dashed border-blue-400 ${
          loading ? 'opacity-50 cursor-not-allowed' : ''
        }`}
        onClick={!loading ? handleClick : undefined}
      >
        <div className="text-center">
          <div className="text-4xl mb-2">
            {loading ? '⏳' : '➕'}
          </div>
          <h3 className="font-medium text-sm text-white">
            {loading ? 'Uploading...' : 'Upload Files'}
          </h3>
          <p className="text-xs text-blue-200 mt-1">
            Click to add files
          </p>
        </div>
      </div>
      
      <input
        ref={fileInputRef}
        type="file"
        multiple
        onChange={handleFileChange}
        className="hidden"
        accept="*/*"
      />
    </>
  );
}
