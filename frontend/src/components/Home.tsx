function Home() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center text-[#DD0303] px-6 py-16 relative overflow-hidden bg-gradient-to-br from-[#FEF3E2] via-[#FFF8F0] to-[#FEF3E2] bg-[length:400%_400%] animate-[gradient-shift_15s_ease_infinite]">
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

      <main className="w-full max-w-3xl text-center space-y-12 relative z-10">
        <div className="space-y-0">
          <img
            src="/hestiaLogo.png"
            alt="Hestia Logo"
            className="w-[200px] h-[200px] mx-auto opacity-0 animate-[fade-in_0.8s_ease-out_forwards]"
          />
          <h1 className="text-6xl md:text-7xl font-black text-[#DD0303] opacity-0 animate-[fade-in-up_0.8s_ease-out_forwards] [animation-delay:0.2s] font-['Playfair_Display',serif] tracking-[-0.03em] leading-[1.1]">
            Hestia
          </h1>
        </div>

        <section className="space-y-6 w-full max-w-full md:max-w-5xl lg:max-w-6xl mx-auto">
          <div className="space-y-4">
            <p className="text-2xl md:text-6xl text-[#FA812F] opacity-0 animate-[fade-in-up_0.8s_ease-out_forwards] [animation-delay:0.4s] font-['Montserrat',sans-serif] font-bold tracking-[0.01em]">
              Fueling creativity in every kitchen.
            </p>
          </div>

          <p className="text-base md:text-lg text-[#DD0303]/80 leading-relaxed opacity-0 animate-[fade-in-up_0.8s_ease-out_forwards] [animation-delay:0.6s] font-['Montserrat',sans-serif] font-semibold tracking-[0.01em]">
            We help home cooks push past the ordinary with curated recipes,
            hands-on guidance, and a community that celebrates experimentation.
            Create meals that surprise, delight, and bring people together.
          </p>
        </section>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-6 opacity-0 animate-[fade-in-up_0.8s_ease-out_forwards] [animation-delay:0.8s]">
          <button 
            className="w-full sm:w-auto rounded-full bg-[#DD0303] px-8 py-3 text-base font-bold text-[#FEF3E2] shadow-lg shadow-[#DD0303]/30 transition hover:bg-[#FA812F] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#FA812F]/60 font-['Montserrat',sans-serif] tracking-[0.05em]"
            onClick ={() => (window.location.href = "/register")}
          >
            Get Started
          </button>
          <button className="w-full sm:w-auto rounded-full border border-[#FA812F]/60 px-8 py-3 text-base font-bold text-[#FA812F] transition hover:border-[#DD0303] hover:text-[#DD0303] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#FA812F]/40 font-['Montserrat',sans-serif] tracking-[0.05em]">
            Learn More
          </button>
        </div>
      </main>
    </div>
  );
}

export default Home;
