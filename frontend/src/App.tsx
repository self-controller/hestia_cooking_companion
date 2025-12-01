import Home from "@/components/Home";
// import LoginPage from "@/components/LoginPage";
// import ShowPage from "@/components/ShowPage";
// import EditPage from "@/components/EditPage";
// import IndexPage from "@/components/IndexPage";
// import VolunteerMapDashboard from "@/components/VolunteerMapDashboard";
import RegisterPage from "@/components/RegisterPage";
import LoginPage from "@/components/LoginPage";

const currentPath = window.location.pathname;

export default function App() {
  // Route based on current path
  //   if (currentPath === "/charities/login") {
  //     return <LoginPage />;
  //   }

    if (currentPath === "/register") {
      return <RegisterPage />;
    }
    if (currentPath === "/login") {
      return <LoginPage />;
    }

  //   if (currentPath === "/charities/index") {
  //     return <IndexPage />;
  //   }

  //   if (currentPath === "/volunteer-dashboard") {
  //     return <VolunteerMapDashboard />;
  //   }

  //   // Match /charities/{id}/edit pattern
  //   if (currentPath.match(/^\/charities\/\d+\/edit$/)) {
  //     return <EditPage />;
  //   }

  //   // Match /charities/{id} pattern (must come after /edit route)
  //   if (currentPath.match(/^\/charities\/\d+$/)) {
  //     return <ShowPage />;
  //   }

  // Default to Home page
  return <Home />;
}
