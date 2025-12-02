import { useState, useEffect } from "react";

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<{
    id: number;
    username: string;
    email: string;
  } | null>(null);
  const [isHomepage, setIsHomepage] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  // Function to check authentication status via API
  const checkAuth = async () => {
    try {
      const response = await fetch("http://localhost:8000/auth/me", {
        method: "GET",
        credentials: "include", // Required for cookies
      });

      if (response.ok) {
        const userData = await response.json();
        setIsLoggedIn(true);
        setUser(userData);
      } else {
        // 401 or other error - not authenticated
        setIsLoggedIn(false);
        setUser(null);
      }
    } catch (error) {
      // Network error or other issue
      setIsLoggedIn(false);
      setUser(null);
    }
  };

  useEffect(() => {
    // Check authentication status on mount
    checkAuth();

    // Check if on homepage
    setIsHomepage(window.location.pathname === "/");

    // Listen for path changes
    const handlePopState = () => {
      setIsHomepage(window.location.pathname === "/");
    };
    window.addEventListener("popstate", handlePopState);

    return () => {
      window.removeEventListener("popstate", handlePopState);
    };
  }, []);

  const handleHomeClick = () => {
    // Navigate to home page
    window.location.href = "/";
  };

  const handleLoginClick = () => {
    // Navigate to login page
    window.location.href = "/login";
  };

  const handleProfileClick = () => {
    // Navigate to profile page
    window.location.href = "/profile";
    setDropdownOpen(false);
  };

  const handleSettingsClick = () => {
    // Navigate to settings page
    window.location.href = "/settings";
    setDropdownOpen(false);
  };

  const handleLogoutClick = async () => {
    try {
      // Call backend logout endpoint
      await fetch("http://localhost:8000/logout", {
        method: "POST",
        credentials: "include", // Required for cookies
      });
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      // Clear local state regardless of API call result
      setIsLoggedIn(false);
      setUser(null);
      localStorage.removeItem("user"); // Clear any cached user data
      setDropdownOpen(false);
      // Redirect to home
      window.location.href = "/";
    }
  };

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (dropdownOpen && !target.closest(".dropdown-container")) {
        setDropdownOpen(false);
      }
    };

    if (dropdownOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownOpen]);

  return (
    <nav className="w-full bg-gradient-to-br from-[#FEF3E2] via-[#FFF8F0] to-[#FEF3E2] border-b border-[#FA812F]/20 shadow-sm">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-18">
          {/* Left side - Hestia Logo and Name (Home button) */}
          <button
            onClick={handleHomeClick}
            className="flex items-center gap-3 hover:opacity-80 transition-opacity focus:outline-none focus-visible:ring-2 focus-visible:ring-[#FA812F]/60 rounded-lg px-2 py-1"
          >
            <img
              src="/hestiaLogo.png"
              alt="Hestia Logo"
              className="w-12 h-12 object-contain"
            />
            <span className="text-3xl font-black text-[#DD0303] font-['Playfair_Display',serif] tracking-[-0.03em]">
              Hestia
            </span>
          </button>

          {/* Right side - Login button or Dropdown menu */}
          <div className="flex items-center">
            {!isLoggedIn ? (
              <button
                onClick={handleLoginClick}
                className="text-[#DD0303] text-base font-semibold hover:text-[#FA812F] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#FA812F]/60 font-['Montserrat',sans-serif] tracking-[0.05em]"
              >
                Login
              </button>
            ) : (
              <div className="relative dropdown-container">
                <button
                  onClick={toggleDropdown}
                  className="flex items-center gap-2 rounded-full bg-[#DD0303] px-6 py-2 text-sm font-bold text-[#FEF3E2] shadow-md shadow-[#DD0303]/30 transition hover:bg-[#FA812F] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#FA812F]/60 font-['Montserrat',sans-serif] tracking-[0.05em]"
                >
                  Menu
                  <svg
                    className={`w-4 h-4 transition-transform ${
                      dropdownOpen ? "rotate-180" : ""
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </button>
                {dropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 rounded-lg bg-[#FEF3E2] border border-[#FA812F]/30 shadow-lg z-50 overflow-hidden">
                    <button
                      onClick={handleProfileClick}
                      className="w-full text-left px-4 py-3 text-sm font-semibold text-[#DD0303] hover:bg-[#FA812F]/20 transition font-['Montserrat',sans-serif]"
                    >
                      Profile
                    </button>
                    <button
                      onClick={handleSettingsClick}
                      className="w-full text-left px-4 py-3 text-sm font-semibold text-[#DD0303] hover:bg-[#FA812F]/20 transition font-['Montserrat',sans-serif] border-t border-[#FA812F]/20"
                    >
                      Settings
                    </button>
                    <button
                      onClick={handleLogoutClick}
                      className="w-full text-left px-4 py-3 text-sm font-semibold text-[#DD0303] hover:bg-[#FA812F]/20 transition font-['Montserrat',sans-serif] border-t border-[#FA812F]/20"
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
