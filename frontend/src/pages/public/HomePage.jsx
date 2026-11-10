import { Link } from "react-router-dom";
import { Button } from "../../shared/ui/Button";

export function HomePage() {
  return (
    <main className="container" data-testid="page-home">
      <h1>Fast Boilerplate</h1>
      <p>Reusable foundation for future applications.</p>
      <Link to="/login">
        <Button data-testid="btn-go-login">Go to Login</Button>
      </Link>
    </main>
  );
}

