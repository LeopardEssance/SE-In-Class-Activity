import { useState } from 'react';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import { getSessionId } from './services/api';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!getSessionId());
  const [userId, setUserId] = useState(null);

  const handleLoginSuccess = (id) => {
    setUserId(id);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserId(null);
  };

  return (
    <div className="app">
      {isLoggedIn ? (
        <Dashboard userId={userId} onLogout={handleLogout} />
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;
