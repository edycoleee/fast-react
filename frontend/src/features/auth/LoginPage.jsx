import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../shared/ui/Button";
import { Input } from "../../shared/ui/Input";
import { useAuthStore } from "../../stores/authStore";
import { apiClient } from "../../api/client";

export function LoginPage() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const onSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage("");
    if (!email || !password) {
      setErrorMessage("Email dan password wajib diisi.");
      return;
    }
    setIsLoading(true);
    try {
      const response = await apiClient.post("/auth/login", { email, password });
      const authData = response.data?.data;
      login({
        token: authData.access_token,
        user: authData.user
      });
      navigate("/dashboard");
    } catch (error) {
      setErrorMessage(
        error?.response?.data?.detail ||
          error?.response?.data?.message ||
          "Login gagal."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="container" data-testid="page-login">
      <h1>Login</h1>
      <form onSubmit={onSubmit} className="card" data-testid="form-login">
        <label htmlFor="email">Email</label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          data-testid="input-email"
        />
        <label htmlFor="password">Password</label>
        <Input
          id="password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          data-testid="input-password"
        />
        <Button type="submit" data-testid="btn-submit-login" disabled={isLoading}>
          {isLoading ? "Signing in..." : "Sign in"}
        </Button>
        {errorMessage ? (
          <p className="message-error" data-testid="error-login">
            {errorMessage}
          </p>
        ) : null}
      </form>
    </main>
  );
}
