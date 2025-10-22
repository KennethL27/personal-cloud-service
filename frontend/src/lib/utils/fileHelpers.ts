// fileHelper.ts

export const getFileIcon = (type: string, isFolder: boolean): string => {
    if (isFolder) return '📁';
    if (type.endsWith('jpeg') || type.endsWith('jpg') || type.endsWith('png')) return '🖼️';
    if (type.endsWith('mp4')) return '🎥';
    if (type.endsWith('mp3')) return '🎵';
    if (type.endsWith('doc') || type.endsWith('pdf')) return '📝';
    if (type.endsWith('zip')) return '📦';
    return '📄';
  };
  
export const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString();
};

export const formatFileSize = (size: string | null): string => {
  return size || '—';
};