'use client';

import { useState, useEffect } from 'react';
import { useFileBrowse, useFileDownload, useFileStream } from '@/lib/api';
import { FileMetadata } from '@/lib/api/types';
import FileStreamDisplay from './FileStreamDisplay';

// File type icons mapping
const getFileIcon = (type: string) => {
  if (type.startsWith('image/')) return '🖼️';
  if (type.startsWith('video/')) return '🎥';
  if (type.startsWith('audio/')) return '🎵';
  if (type === 'application/pdf') return '📄';
  if (type.includes('word') || type.includes('document')) return '📝';
  if (type.includes('zip') || type.includes('archive')) return '📦';
  return '📁';
};

// Format file size
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Format date
const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString();
};

// Category options
const categories = [
  { value: '', label: 'All Files' },
  { value: 'photos', label: 'Photos' },
  { value: 'videos', label: 'Videos' },
  { value: 'documents', label: 'Documents' },
  { value: 'audio', label: 'Audio' },
  { value: 'zip', label: 'Archives' },
  { value: 'others', label: 'Others' },
];

export default function FileBrowser() {
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [sortBy, setSortBy] = useState<'name' | 'size' | 'modified'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // API hooks
  const { data: browseData, loading: browseLoading, error: browseError, browseFiles } = useFileBrowse();
  const { downloadFile, loading: downloadLoading } = useFileDownload();
  const { streamFile, loading: streamLoading, error: streamError, data: streamData } = useFileStream();

  // Load files on component mount and when category changes
  useEffect(() => {
    browseFiles(selectedCategory || undefined);
  }, [selectedCategory]);

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
  };

  const handleViewModeToggle = () => {
    setViewMode(viewMode === 'grid' ? 'list' : 'grid');
  };

  const handleSort = (field: 'name' | 'size' | 'modified') => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('asc');
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

  // Sort files
  const sortedFiles = browseData?.files ? [...browseData.files].sort((a, b) => {
    let aValue: string | number, bValue: string | number;
    
    switch (sortBy) {
      case 'name':
        aValue = a.name.toLowerCase();
        bValue = b.name.toLowerCase();
        break;
      case 'size':
        aValue = a.size;
        bValue = b.size;
        break;
      case 'modified':
        aValue = new Date(a.modified).getTime();
        bValue = new Date(b.modified).getTime();
        break;
      default:
        return 0;
    }

    if (aValue < bValue) return sortOrder === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  }) : [];

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header Controls */}
      <div className="bg-gray-500 rounded-lg shadow p-6">
        <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
          <h2 className="text-xl font-semibold">Browse Files</h2>
          
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
            {/* Category Filter */}
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium">Category:</label>
              <select
                value={selectedCategory}
                onChange={(e) => handleCategoryChange(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {categories.map((category) => (
                  <option key={category.value} value={category.value}>
                    {category.label}
                  </option>
                ))}
              </select>
            </div>

            {/* View Toggle */}
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium">View:</label>
              <button
                onClick={handleViewModeToggle}
                className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                {viewMode === 'grid' ? 'List View' : 'Grid View'}
              </button>
            </div>
          </div>
        </div>

        {/* File Count */}
        {browseData && (
          <div className="mt-4 text-sm text-gray-300">
            {browseData.total_count} file{browseData.total_count !== 1 ? 's' : ''} found
          </div>
        )}
      </div>

      {/* Error Display */}
      {browseError && (
        <div className="bg-red-500 rounded-lg shadow p-6">
          <p className="text-red-100">Error: {browseError}</p>
        </div>
      )}

      {/* Loading State */}
      {browseLoading && (
        <div className="bg-gray-500 rounded-lg shadow p-6">
          <p className="text-gray-300">Loading files...</p>
        </div>
      )}

      {/* Empty State */}
      {!browseLoading && !browseError && browseData?.total_count === 0 && (
        <div className="bg-gray-500 rounded-lg shadow p-6 text-center">
          <p className="text-gray-300">No files found</p>
        </div>
      )}

      {/* File Stream Display */}
      <FileStreamDisplay 
        streamData={streamData}
        streamError={streamError}
        streamLoading={streamLoading}
      />

      {/* Files Display */}
      {!browseLoading && !browseError && browseData && browseData.total_count > 0 && (
        <div className="bg-gray-500 rounded-lg shadow p-6">
          {viewMode === 'grid' ? (
            /* Grid View */
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {sortedFiles.map((file) => (
                <div key={file.name} className="bg-gray-600 rounded-lg p-4 hover:bg-gray-700 transition-colors">
                  <div className="text-center">
                    <div className="text-4xl mb-2">{getFileIcon(file.type)}</div>
                    <h3 className="font-medium text-sm truncate" title={file.name}>
                      {file.name}
                    </h3>
                    <p className="text-xs text-gray-400 mt-1">
                      {formatFileSize(file.size)}
                    </p>
                    <p className="text-xs text-gray-400">
                      {formatDate(file.modified)}
                    </p>
                    <div className="flex gap-2 mt-3">
                      <button
                        onClick={() => handleDownload(file.name)}
                        disabled={downloadLoading}
                        className="flex-1 px-2 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700 disabled:opacity-50"
                      >
                        Download
                      </button>
                      <button
                        onClick={() => handleStream(file.name)}
                        disabled={streamLoading}
                        className="flex-1 px-2 py-1 bg-purple-600 text-white text-xs rounded hover:bg-purple-700 disabled:opacity-50"
                      >
                        Stream
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            /* List View */
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-400">
                    <th 
                      className="text-left py-2 cursor-pointer hover:bg-gray-600"
                      onClick={() => handleSort('name')}
                    >
                      Name {sortBy === 'name' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th className="text-left py-2">Type</th>
                    <th 
                      className="text-left py-2 cursor-pointer hover:bg-gray-600"
                      onClick={() => handleSort('size')}
                    >
                      Size {sortBy === 'size' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th 
                      className="text-left py-2 cursor-pointer hover:bg-gray-600"
                      onClick={() => handleSort('modified')}
                    >
                      Modified {sortBy === 'modified' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th className="text-left py-2">Category</th>
                    <th className="text-left py-2">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedFiles.map((file) => (
                    <tr key={file.name} className="border-b border-gray-600 hover:bg-gray-600">
                      <td className="py-2">
                        <div className="flex items-center gap-2">
                          <span>{getFileIcon(file.type)}</span>
                          <span className="truncate max-w-xs" title={file.name}>
                            {file.name}
                          </span>
                        </div>
                      </td>
                      <td className="py-2 text-sm text-gray-300">{file.type}</td>
                      <td className="py-2 text-sm text-gray-300">{formatFileSize(file.size)}</td>
                      <td className="py-2 text-sm text-gray-300">{formatDate(file.modified)}</td>
                      <td className="py-2 text-sm text-gray-300 capitalize">{file.category}</td>
                      <td className="py-2">
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleDownload(file.name)}
                            disabled={downloadLoading}
                            className="px-2 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700 disabled:opacity-50"
                          >
                            Download
                          </button>
                          <button
                            onClick={() => handleStream(file.name)}
                            disabled={streamLoading}
                            className="px-2 py-1 bg-purple-600 text-white text-xs rounded hover:bg-purple-700 disabled:opacity-50"
                          >
                            Stream
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
