export default function Footer() {
    return (
      <footer className="bg-gray-900 text-white p-4 mt-auto">
        <div className="container mx-auto text-center">
          <p>Product of my year {new Date().getFullYear()}.</p>
        </div>
      </footer>
    );
  }