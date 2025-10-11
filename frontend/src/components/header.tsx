import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-gray-800 text-white p-4">
      <nav className="container mx-auto flex justify-between">
        <h1 className="text-xl font-bold">Personal Cloud Storage</h1>
        <ul className="flex gap-4">
          <li><Link href="/">Home</Link></li>
          <li><Link href="/browse">Browse</Link></li>
          <li><Link href="/settings">Settings</Link></li>
        </ul>
      </nav>
    </header>
  );
}