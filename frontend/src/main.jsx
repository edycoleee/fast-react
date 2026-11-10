import React from "react";
import ReactDOM from "react-dom/client";
import { QueryProvider } from "./providers/QueryProvider";
import { AppRouter } from "./providers/AppRouter";
import "./shared/styles/tokens.css";
import "./shared/styles/global.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <QueryProvider>
      <AppRouter />
    </QueryProvider>
  </React.StrictMode>
);

