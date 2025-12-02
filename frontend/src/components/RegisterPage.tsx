import { useState } from "react";
import Navbar from "@/components/Navbar";

function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Validate passwords match
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ email, password, username }),
      });

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ detail: "Registration failed" }));
        throw new Error(errorData.detail || "Registration failed");
      }

      const data = await response.json();

      // Store user info if provided
      if (data.id) {
        localStorage.setItem("user", JSON.stringify(data));
      }

      // Redirect to home or dashboard
      window.location.href = "/";
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "An error occurred during registration"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />
      <div className="h-screen flex flex-col justify-center items-center px-6 py-8 relative overflow-hidden bg-gradient-to-br from-[#FEF3E2] via-[#FFF8F0] to-[#FEF3E2] bg-[length:400%_400%] animate-[gradient-shift_15s_ease_infinite]">
        {/* Floating Shapes Background */}
        <div className="absolute w-[200px] h-[200px] rounded-full bg-[radial-gradient(circle,#FA812F,transparent)] top-[10%] left-[10%] opacity-15 blur-[1px] pointer-events-none animate-[float_20s_ease-in-out_infinite]"></div>
        <div className="absolute w-[150px] h-[150px] rounded-full bg-[radial-gradient(circle,#DD0303,transparent)] top-[60%] right-[15%] opacity-15 blur-[1px] pointer-events-none animate-[float-slow_25s_ease-in-out_infinite] [animation-delay:-5s]"></div>
        <div className="absolute w-[180px] h-[180px] rounded-full bg-[radial-gradient(circle,#FA812F,transparent)] bottom-[15%] left-[20%] opacity-15 blur-[1px] pointer-events-none animate-[float_22s_ease-in-out_infinite] [animation-delay:-10s]"></div>
        <div className="absolute w-[120px] h-[120px] rounded-full bg-[radial-gradient(circle,#DD0303,transparent)] top-[30%] right-[30%] opacity-15 blur-[1px] pointer-events-none animate-[float-slow_18s_ease-in-out_infinite] [animation-delay:-7s]"></div>
        <div className="absolute w-[100px] h-[100px] rounded-full bg-[radial-gradient(circle,#FA812F,transparent)] bottom-[30%] right-[10%] opacity-15 blur-[1px] pointer-events-none animate-[float_24s_ease-in-out_infinite] [animation-delay:-12s]"></div>
        <div className="absolute w-[160px] h-[160px] rounded-full bg-[radial-gradient(circle,rgba(221,3,3,0.3),transparent)] top-[50%] left-[5%] opacity-15 blur-[1px] pointer-events-none animate-[float-slow_21s_ease-in-out_infinite] [animation-delay:-8s]"></div>

        {/* Radial Gradient Overlays */}
        <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_20%_30%,rgba(250,129,47,0.08)_0%,transparent_50%),radial-gradient(circle_at_80%_70%,rgba(221,3,3,0.06)_0%,transparent_50%),radial-gradient(circle_at_50%_50%,rgba(250,129,47,0.05)_0%,transparent_60%)]"></div>

        {/* Texture Overlay */}
        <div className="absolute inset-0 pointer-events-none opacity-50 bg-[repeating-linear-gradient(45deg,transparent,transparent_2px,rgba(250,129,47,0.02)_2px,rgba(250,129,47,0.02)_4px)]"></div>

        {/* Register Form Box */}
        <div className="w-full max-w-md relative z-10 -mt-20 md:-mt-26">
          <div className="bg-[#FEF3E2]/95 backdrop-blur-sm rounded-3xl shadow-2xl shadow-[#DD0303]/20 border border-[#FA812F]/30 p-6 md:p-8 space-y-5">
            <h1 className="text-4xl md:text-5xl font-black text-[#DD0303] text-center mb-2 font-['Playfair_Display',serif] tracking-[-0.03em]">
              Register
            </h1>
            <p className="text-center text-[#DD0303]/70 text-sm font-['Montserrat',sans-serif] mb-6">
              Join the Hestia community
            </p>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-2">
                <label
                  htmlFor="username"
                  className="block text-sm font-semibold text-[#DD0303] font-['Montserrat',sans-serif] tracking-[0.05em]"
                >
                  Username
                </label>
                <input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  className="w-full px-4 py-3 rounded-xl border-2 border-[#FA812F]/40 bg-white/80 text-[#DD0303] placeholder-[#DD0303]/50 focus:outline-none focus:border-[#DD0303] focus:ring-2 focus:ring-[#FA812F]/30 transition-all font-['Montserrat',sans-serif]"
                  placeholder="Enter your username"
                />
              </div>

              <div className="space-y-2">
                <label
                  htmlFor="email"
                  className="block text-sm font-semibold text-[#DD0303] font-['Montserrat',sans-serif] tracking-[0.05em]"
                >
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full px-4 py-3 rounded-xl border-2 border-[#FA812F]/40 bg-white/80 text-[#DD0303] placeholder-[#DD0303]/50 focus:outline-none focus:border-[#DD0303] focus:ring-2 focus:ring-[#FA812F]/30 transition-all font-['Montserrat',sans-serif]"
                  placeholder="Enter your email"
                />
              </div>

              <div className="space-y-2">
                <label
                  htmlFor="password"
                  className="block text-sm font-semibold text-[#DD0303] font-['Montserrat',sans-serif] tracking-[0.05em]"
                >
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full px-4 py-3 rounded-xl border-2 border-[#FA812F]/40 bg-white/80 text-[#DD0303] placeholder-[#DD0303]/50 focus:outline-none focus:border-[#DD0303] focus:ring-2 focus:ring-[#FA812F]/30 transition-all font-['Montserrat',sans-serif]"
                  placeholder="Enter your password"
                />
              </div>

              <div className="space-y-2">
                <label
                  htmlFor="confirmPassword"
                  className="block text-sm font-semibold text-[#DD0303] font-['Montserrat',sans-serif] tracking-[0.05em]"
                >
                  Confirm Password
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  className="w-full px-4 py-3 rounded-xl border-2 border-[#FA812F]/40 bg-white/80 text-[#DD0303] placeholder-[#DD0303]/50 focus:outline-none focus:border-[#DD0303] focus:ring-2 focus:ring-[#FA812F]/30 transition-all font-['Montserrat',sans-serif]"
                  placeholder="Confirm your password"
                />
              </div>

              {error && (
                <div className="bg-[#DD0303]/10 border border-[#DD0303]/30 rounded-xl px-4 py-3 text-sm text-[#DD0303] font-semibold font-['Montserrat',sans-serif]">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-full bg-[#DD0303] px-8 py-3 text-base font-bold text-[#FEF3E2] shadow-lg shadow-[#DD0303]/30 transition hover:bg-[#FA812F] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#FA812F]/60 disabled:opacity-50 disabled:cursor-not-allowed font-['Montserrat',sans-serif] tracking-[0.05em]"
              >
                {loading ? "Registering..." : "Register"}
              </button>
            </form>

            <div className="text-center pt-4">
              <p className="text-sm text-[#DD0303]/70 font-['Montserrat',sans-serif]">
                Already have an account?{" "}
                <a
                  href="/login"
                  className="text-[#FA812F] font-semibold hover:text-[#DD0303] transition-colors"
                >
                  Sign in
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default RegisterPage;
