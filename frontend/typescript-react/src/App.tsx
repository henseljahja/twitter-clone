import React from "react";
import "./App.css";
// import Layout from "./features/layout/main/Layout";
import { QueryClient, QueryClientProvider } from "react-query";
import { Layout } from "./features/layout/Layout";

function App() {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <Layout />
    </QueryClientProvider>
  );
}

export default App;
