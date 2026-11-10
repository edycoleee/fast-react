import { useAuthStore } from "../../stores/authStore";
import { Button } from "../../shared/ui/Button";

export function DashboardPage() {
  const logout = useAuthStore((state) => state.logout);
  return (
    <main className="container" data-testid="page-dashboard">
      <h1>Dashboard</h1>
      <p>Protected area skeleton.</p>
      <Button
        variant="secondary"
        onClick={logout}
        data-testid="btn-logout"
      >
        Logout
      </Button>
    </main>
  );
}

