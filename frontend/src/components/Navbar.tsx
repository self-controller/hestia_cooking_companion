import { useState, useEffect } from "react";

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isHomepage, setIsHomepage] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("access_token");
    setIsLoggedIn(!!token);

    // Check if on homepage
    setIsHomepage(window.location.pathname === "/");

    // Listen for path changes
    const handlePopState = () => {
      setIsHomepage(window.location.pathname === "/");
    };
    window.addEventListener("popstate", handlePopState);

    // Listen for storage changes (login/logout)
    const handleStorageChange = () => {
      const token = localStorage.getItem("access_token");
      setIsLoggedIn(!!token);
    };
    window.addEventListener("storage", handleStorageChange);

    return () => {
      window.removeEventListener("popstate", handlePopState);
      window.removeEventListener("storage", handleStorageChange);
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

  const handleLogoutClick = () => {
    // Clear authentication
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setIsLoggedIn(false);
    setDropdownOpen(false);
    // Redirect to home
    window.location.href = "/";
  };

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

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
