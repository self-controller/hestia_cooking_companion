import { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";

function Kitchen() {
  const [user, setUser] = useState<{
    id: number;
    username: string;
    email: string;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication and get user data
    const checkAuth = async () => {
      try {
        const response = await fetch("http://localhost:8000/auth/me", {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        } else {
          // Not authenticated, redirect to login
          window.location.href = "/login";
        }
      } catch (error) {
        // Error checking auth, redirect to login
        window.location.href = "/login";
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#FEF3E2] via-[#FFF8F0] to-[#FEF3E2]">
          <p className="text-[#DD0303] font-['Montserrat',sans-serif]">Loading...</p>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-[#FEF3E2] via-[#FFF8F0] to-[#FEF3E2] px-6 py-8">
        <main className="max-w-7xl mx-auto">
          <div className="space-y-6">
            <h1 className="text-4xl md:text-5xl font-black text-[#DD0303] font-['Playfair_Display',serif] tracking-[-0.03em]">
              My Kitchen
            </h1>
            
            {user && (
              <p className="text-lg text-[#DD0303]/80 font-['Montserrat',sans-serif]">
                Welcome back, {user.username}!
              </p>
            )}

            {/* Add your content here */}
            <div className="mt-8">
              <p className="text-[#DD0303]/70 font-['Montserrat',sans-serif]">
                Your kitchen content will go here.
              </p>
            </div>
          </div>
        </main>
      </div>
    </>
  );
}

export default Kitchen;