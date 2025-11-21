import { useEffect, useState } from "react";

const usePollingFetch = (fetchFunction, interval) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetch = async () => {
    try {
      const result = await fetchFunction();
      setData(result);
      setError("");
    } catch (err) {
      setError(err.detail || "Failed to fetch data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetch();
    const intervalId = setInterval(fetch, interval);
    return () => clearInterval(intervalId);
  }, []);

  return { data, loading, error, setError, refetch: fetch };
};

export default usePollingFetch;
