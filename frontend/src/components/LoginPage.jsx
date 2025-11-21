import { useState } from 'react';
import { authAPI } from '../services/api';
import '../styles/LoginPage.css';
import FormInput from './FormInput';

function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(username, password);

      if (!response.success) {
        setError(response.message || 'Login failed');
        return;
      }

      onLoginSuccess(response.user_id);
    } catch (err) {
      setError(err.message || 'An error occurred during login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>Smart Home IoT System</h1>
          <p>Login to control your devices</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <FormInput
            id="username"
            label="Username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username"
            disabled={loading}
          />

          <FormInput
            id="password"
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password"
            disabled={loading}
          />

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>

          <div className="login-info">
            <p>Default credentials:</p>
            <p>Username: <strong>admin</strong></p>
            <p>Password: <strong>password123</strong></p>
          </div>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
