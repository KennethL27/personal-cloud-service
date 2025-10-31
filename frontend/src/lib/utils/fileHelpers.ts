// fileHelper.ts

export const getFileIcon = (type: string, isFolder: boolean): string => {
    if (isFolder) return '📁';
    const lowerType = type.toLowerCase();
    if (lowerType.endsWith('jpeg') || lowerType.endsWith('jpg') || lowerType.endsWith('png')) return '🖼️';
    if (lowerType.endsWith('mp4')) return '🎥';
    if (lowerType.endsWith('mp3')) return '🎵';
    if (lowerType.endsWith('doc') || lowerType.endsWith('pdf')) return '📝';
    if (lowerType.endsWith('zip')) return '📦';
    return '📄';
  };
  
export const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString();
};

export const formatFileSize = (size: string | null): string => {
  return size || '—';
};