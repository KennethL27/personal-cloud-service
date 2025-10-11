'use client';

import { useState } from 'react';
import { useHealthCheck, useFileUpload, useFileDownload, useFileStream } from '@/lib/api';
import FileStreamDisplay from './FileStreamDisplay';

export default function FileManager() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  
  // API hooks
  const { data: health, loading: healthLoading, error: healthError } = useHealthCheck();
  const { uploadFiles, loading: uploadLoading, error: uploadError, data: uploadData } = useFileUpload();
  const { downloadFile, loading: downloadLoading, error: downloadError } = useFileDownload();
  const { streamFile, loading: streamLoading, error: streamError, data: streamData } = useFileStream();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFiles(Array.from(event.target.files));
    }
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;
    
    try {
      await uploadFiles(selectedFiles);
      setSelectedFiles([]);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  const handleDownload = async (fileName: string) => {
    try {
      await downloadFile(fileName);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  const handleStream = async (fileName: string) => {
    try {
      await streamFile(fileName);
    } catch (error) {
      console.error('Stream failed:', error);
    }
  };


  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Health Status */}
      <div className="bg-gray-500 rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Backend Status</h2>
        {healthLoading ? (
          <p className="text-gray-600">Checking health...</p>
        ) : healthError ? (
          <p className="text-red-600">Error: {healthError}</p>
        ) : (
          <p className="text-green-600">Status: {health?.status}</p>
        )}
      </div>

      {/* File Upload */}
      <div className="bg-gray-500 rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Upload Files</h2>
        
        <div className="space-y-4">
          <input
            type="file"
            multiple
            onChange={handleFileSelect}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          
          {selectedFiles.length > 0 && (
            <div className="text-sm text-gray-600">
              Selected files: {selectedFiles.map(f => f.name).join(', ')}
            </div>
          )}
          
          <button
            onClick={handleUpload}
            disabled={selectedFiles.length === 0 || uploadLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploadLoading ? 'Uploading...' : 'Upload Files'}
          </button>
          
          {uploadError && (
            <p className="text-red-600">Upload error: {uploadError}</p>
          )}
          
          {uploadData && (
            <div className="text-green-600">
              Successfully uploaded: {uploadData.uploaded_files.join(', ')}
            </div>
          )}
        </div>
      </div>

      {/* File Download Example */}
      <div className="bg-gray-500 rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Download Files</h2>
        
        <div className="space-y-4">
          <p className="text-gray-300">
            Enter a filename to download (this will trigger a download in your browser):
          </p>
          
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="filename.pdf"
              id="downloadFileName"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={() => {
                const input = document.getElementById('downloadFileName') as HTMLInputElement;
                if (input.value.trim()) {
                  handleDownload(input.value.trim());
                }
              }}
              disabled={downloadLoading}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {downloadLoading ? 'Downloading...' : 'Download'}
            </button>
          </div>
          
          {downloadError && (
            <p className="text-red-600">Download error: {downloadError}</p>
          )}
        </div>
      </div>

      {/* File Stream Display */}
      <div className="bg-gray-500 rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Stream Files to Display</h2>
        
        <div className="space-y-4">
          <p className="text-gray-300">
            Enter a filename to stream and display its content on the page:
          </p>
          
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="filename.txt"
              id="streamFileName"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={() => {
                const input = document.getElementById('streamFileName') as HTMLInputElement;
                if (input.value.trim()) {
                  handleStream(input.value.trim());
                }
              }}
              disabled={streamLoading}
              className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {streamLoading ? 'Streaming...' : 'Stream File'}
            </button>
          </div>
          
          <FileStreamDisplay 
            streamData={streamData}
            streamError={streamError}
            streamLoading={streamLoading}
          />
        </div>
      </div>
    </div>
  );
}
