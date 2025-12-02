import { useState, useEffect } from "react";

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<{ id: number; username: string; email: string } | null>(null);
  const [isHomepage, setIsHomepage] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [loading, setLoading] = useState(true);

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
    } finally {
      setLoading(false);
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

  const handleLoginClick = () => {
    // Navigate to login page
    window.location.href = "/login";
  };

  const handleProfileClick = () => {
    // Navigate to profile page
    window.location.href = "/profile";
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

  // Don't render until we've checked auth status
  if (loading) {
    return <nav>Loading...</nav>; // Or return null, or a loading spinner
  }

  return (
    <nav>
      <div>
        <div>
          <img src="/hestiaLogo.png" alt="Hestia Logo" />
          <span>Hestia</span>
        </div>
        <div>
          {isHomepage && !isLoggedIn && (
            <button onClick={handleLoginClick}>Login</button>
          )}
          {isLoggedIn && (
            <>
              <button onClick={handleProfileClick}>Profile</button>
              <div>
                <button onClick={toggleDropdown}>Dropdown</button>
                {dropdownOpen && (
                  <div>
                    <button onClick={handleSettingsClick}>Settings</button>
                    <button onClick={handleLogoutClick}>Logout</button>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;