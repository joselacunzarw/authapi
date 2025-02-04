# 📄 **Especificación para Desarrollador Frontend (React + TypeScript)**

## 🚀 **Objetivo**

Implementar un sistema de autenticación en el frontend que permita a los usuarios iniciar sesión y consumir una API de chat protegida mediante un token JWT.

---

## 🔐 **Proceso de Autenticación**

1. **Login**:
   - El usuario ingresa su **email** y **contraseña**.
   - Se envía una solicitud `POST` a la API de autenticación para obtener un **token JWT**.
   - Si el login es exitoso, el token JWT se almacena de forma segura (por ejemplo, en `localStorage` o `sessionStorage`).

2. **Consumo de la API de Chat**:
   - Todas las solicitudes a la API de chat deben incluir el token JWT en el encabezado `Authorization` con el formato `Bearer <token>`.

---

## 📥 **Endpoints Disponibles**

### 1. **Login de Usuario**

- **URL**: `POST http://localhost:8001/login`
- **Headers**:
  ```json
  Content-Type: application/json
  ```
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

- **Respuesta Exitosa**:
  ```json
  {
    "access_token": "<jwt-token>",
    "token_type": "bearer"
  }
  ```

### 2. **Consumo de la API de Chat**

- **URL Ejemplo**: `GET https://api.example.com/chat/messages`
- **Headers**:
  ```json
  Authorization: Bearer <jwt-token>
  ```

---

## 🛠️ **Implementación del Login en React con TypeScript**

### 1. **Instalar Dependencias**

```bash
npm install axios
```

### 2. **Crear el Servicio de Autenticación**

**`src/services/authService.ts`**

```typescript
import axios from 'axios';

const API_URL = 'http://localhost:8001/login';

export const login = async (email: string, password: string): Promise<string> => {
  try {
    const response = await axios.post(API_URL, { email, password });
    return response.data.access_token;
  } catch (error) {
    throw new Error('Invalid email or password');
  }
};
```

### 3. **Componente de Login**

**`src/components/Login.tsx`**

```tsx
import React, { useState } from 'react';
import { login } from '../services/authService';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const token = await login(email, password);
      localStorage.setItem('token', token);
      setError(null);
      alert('Login successful!');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default Login;
```

### 4. **Consumir la API de Chat con el Token**

**`src/services/chatService.ts`**

```typescript
import axios from 'axios';

const CHAT_API_URL = 'https://api.example.com/chat/messages';

export const getChatMessages = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No token found');
  }

  try {
    const response = await axios.get(CHAT_API_URL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch chat messages');
  }
};
```

### 5. **Ejemplo de Componente para Mostrar Mensajes del Chat**

**`src/components/Chat.tsx`**

```tsx
import React, { useEffect, useState } from 'react';
import { getChatMessages } from '../services/chatService';

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const data = await getChatMessages();
        setMessages(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchMessages();
  }, []);

  return (
    <div>
      <h2>Chat Messages</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>{msg}</li>
        ))}
      </ul>
    </div>
  );
};

export default Chat;
```

---

## 🔒 **Recomendaciones de Seguridad**

1. **Almacenar el Token**:
   - Usa `localStorage` o `sessionStorage` para almacenar el token JWT de forma segura.
   - Si es una aplicación sensible, considera almacenar el token en una cookie segura con `HttpOnly`.

2. **Manejo de Errores**:
   - Maneja errores de autenticación y expiración de tokens para redirigir al usuario a la página de login cuando sea necesario.

3. **Logout**:
   - Implementa una función de logout que elimine el token del almacenamiento.

---

## 🛠️ **Ejemplo de Logout**

**`src/services/authService.ts`**

```typescript
export const logout = () => {
  localStorage.removeItem('token');
};
```

---

## ✅ **Resumen**

- **Login**: El usuario ingresa su email y contraseña y obtiene un token JWT.
- **Consumo de API**: Todas las solicitudes a la API de chat incluyen el token JWT en el encabezado `Authorization`.
- **Seguridad**: Almacena el token de forma segura y maneja errores de autenticación.

