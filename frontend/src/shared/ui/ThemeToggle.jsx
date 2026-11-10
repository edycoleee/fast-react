import { Button } from "./Button";
import { useTheme } from "../theme/useTheme";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const nextTheme = theme === "dark" ? "Light" : "Dark";

  return (
    <Button
      variant="outline"
      onClick={toggleTheme}
      className="theme-toggle"
      data-testid="btn-toggle-theme"
      aria-label={`Switch to ${nextTheme} mode`}
    >
      {nextTheme} Mode
    </Button>
  );
}
