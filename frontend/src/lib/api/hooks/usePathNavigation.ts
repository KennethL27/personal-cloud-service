import { useState, useCallback } from 'react';

export function usePathNavigation(initialPath: string = '') {
  const [currentPath, setCurrentPath] = useState<string>(initialPath);

  const navigateToFolder = useCallback((relativePath: string) => {
    setCurrentPath(relativePath);
  }, []);

  const navigateBack = useCallback(() => {
    const pathParts = currentPath.split('/').filter(Boolean);
    pathParts.pop();
    setCurrentPath(pathParts.join('/'));
  }, [currentPath]);

  const getPathDisplay = useCallback((basePath?: string) => {
    if (!currentPath) return basePath;
    return basePath ? `${basePath}/${currentPath}` : currentPath;
  }, [currentPath]);

  return {
    currentPath,
    navigateToFolder,
    navigateBack,
    getPathDisplay,
  };
}