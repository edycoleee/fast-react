import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../shared/ui/Button";
import { Input } from "../../shared/ui/Input";
import { useAuthStore } from "../../stores/authStore";

export function LoginPage() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = (event) => {
    event.preventDefault();
    if (!email || !password) {
      return;
    }
    login();
    navigate("/dashboard");
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
        <Button type="submit" data-testid="btn-submit-login">
          Sign in
        </Button>
      </form>
    </main>
  );
}

