import Home from "@/components/Home";
import Kitchen from "@/components/Kitchen"
import RegisterPage from "@/components/RegisterPage";
import LoginPage from "@/components/LoginPage";

const currentPath = window.location.pathname;

export default function App() {
    if (currentPath === "/register") {
      return <RegisterPage />;
    }
    if (currentPath === "/login") {
      return <LoginPage />;
    }
    if (currentPath ===  "/kitchen"){
      return <Kitchen />
    }

  return <Home />;
}
