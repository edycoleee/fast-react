import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { apiClient } from "../../api/client";
import { useAuthStore } from "../../stores/authStore";
import { Button } from "../../shared/ui/Button";

export function DashboardPage() {
  const logout = useAuthStore((state) => state.logout);
  const user = useAuthStore((state) => state.user);
  const { data, isLoading, error } = useQuery({
    queryKey: ["access-summary"],
    queryFn: async () => {
      const response = await apiClient.get("/access/summary");
      return response.data?.data;
    }
  });
  return (
    <main className="container" data-testid="page-dashboard">
      <h1>Dashboard</h1>
      <p>Welcome, {user?.username || "user"}.</p>
      {isLoading ? (
        <p data-testid="loading-access-summary">Loading access summary...</p>
      ) : error ? (
        <p data-testid="error-access-summary">Failed to load access summary.</p>
      ) : (
        <pre data-testid="access-summary">{JSON.stringify(data || {}, null, 2)}</pre>
      )}
      <div className="actions-inline">
        <Link to="/admin/access">
          <Button variant="outline" data-testid="btn-go-admin-access">
            Go to Access Management
          </Button>
        </Link>
        <Button
          variant="danger"
          onClick={logout}
          data-testid="btn-logout"
        >
          Logout
        </Button>
      </div>
    </main>
  );
}
