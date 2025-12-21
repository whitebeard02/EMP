// src/pages/Login.tsx
import React, { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();
    const { session } = useAuth();

    // SMART REDIRECT: If already logged in, go straight to Dashboard
    useEffect(() => {
        if (session) {
            navigate('/dashboard');
        }
    }, [session, navigate]);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        const { error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });

        if (error) {
            setError(error.message);
        } else {
            // Success! The AuthContext will detect the change and auto-redirect you.
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
            <form onSubmit={handleLogin} style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
                <h2>Clinician Login</h2>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                
                <div style={{ marginBottom: '10px' }}>
                    <label>Email:</label><br/>
                    <input 
                        type="email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>
                
                <div style={{ marginBottom: '20px' }}>
                    <label>Password:</label><br/>
                    <input 
                        type="password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <button type="submit" style={{ width: '100%', padding: '10px', background: 'blue', color: 'white', border: 'none', cursor: 'pointer' }}>
                    Log In
                </button>
            </form>
        </div>
    );
};

export default Login;