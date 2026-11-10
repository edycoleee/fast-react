import { Navigate, Route, Routes } from "react-router-dom";
import { BrowserRouter } from "react-router-dom";
import { HomePage } from "../pages/public/HomePage";
import { DashboardPage } from "../pages/protected/DashboardPage";
import { AdminAccessPage } from "../pages/protected/AdminAccessPage";
import { LoginPage } from "../features/auth/LoginPage";
import { useAuthStore } from "../stores/authStore";
import { ThemeToggle } from "../shared/ui/ThemeToggle";

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

export function AppRouter() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  return (
    <BrowserRouter>
      <div className="theme-toggle-container">
        <ThemeToggle />
      </div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/access"
          element={
            <ProtectedRoute>
              <AdminAccessPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="*"
          element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}
