import FileBrowser from '@/components/FileBrowser';

export default function Browse() {
  return (
    <div className="min-h-screen bg-gray-800">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold text-center mb-8">Browse Files</h1>
        <FileBrowser />
      </div>
    </div>
  );
}
