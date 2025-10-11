'use client';

import { useState, useEffect } from 'react';

// Component for displaying text file content
function FileContentDisplay({ blob }: { blob: Blob }) {
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const readBlob = async () => {
      try {
        const text = await blob.text();
        setContent(text);
      } catch (error) {
        setContent('Error reading file content');
      } finally {
        setLoading(false);
      }
    };

    readBlob();
  }, [blob]);

  if (loading) {
    return <span className="text-gray-400">Loading content...</span>;
  }

  return <>{content}</>;
}

interface FileStreamDisplayProps {
  streamData: {
    blob: Blob;
    url: string;
    type: string;
    name: string;
  } | null;
  streamError: string | null;
  streamLoading: boolean;
}

export default function FileStreamDisplay({ streamData, streamError, streamLoading }: FileStreamDisplayProps) {
  // Cleanup object URLs when component unmounts
  useEffect(() => {
    return () => {
      if (streamData?.url) {
        URL.revokeObjectURL(streamData.url);
      }
    };
  }, [streamData?.url]);

  if (streamError) {
    return (
      <div className="bg-red-500 rounded-lg shadow p-6">
        <p className="text-red-100">Stream error: {streamError}</p>
      </div>
    );
  }

  if (streamLoading) {
    return (
      <div className="bg-gray-500 rounded-lg shadow p-6">
        <p className="text-gray-300">Loading file...</p>
      </div>
    );
  }

  if (!streamData) {
    return null;
  }

  return (
    <div className="bg-gray-500 rounded-lg shadow p-6">
      <h3 className="text-lg font-medium mb-2 text-gray-200">File: {streamData.name}</h3>
      <div className="bg-gray-700 p-4 rounded-md overflow-auto">
        {/* Display different file types appropriately */}
        {streamData.type.startsWith('image/') ? (
          <img 
            src={streamData.url} 
            alt={streamData.name}
            className="max-w-full h-auto mx-auto"
          />
        ) : streamData.type.startsWith('video/') ? (
          <video 
            src={streamData.url} 
            controls 
            className="max-w-full h-auto mx-auto"
          >
            Your browser does not support the video tag.
          </video>
        ) : streamData.type.startsWith('audio/') ? (
          <audio 
            src={streamData.url} 
            controls 
            className="w-full"
          >
            Your browser does not support the audio tag.
          </audio>
        ) : streamData.type === 'application/pdf' ? (
          <iframe 
            src={streamData.url} 
            className="w-full h-96 border-0"
            title={streamData.name}
          />
        ) : streamData.type.startsWith('text/') || streamData.type === 'application/json' ? (
          <pre className="text-gray-200 whitespace-pre-wrap break-words">
            {/* For text files, we need to read the blob content */}
            <FileContentDisplay blob={streamData.blob} />
          </pre>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-400 mb-4">File type: {streamData.type}</p>
            <a 
              href={streamData.url} 
              download={streamData.name}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Download File
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
