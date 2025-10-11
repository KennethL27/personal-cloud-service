import FileManager from '@/components/FileManager';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-800">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold text-center mb-8">Control Center!</h1>
        <FileManager />
      </div>
    </div>
  );
}
