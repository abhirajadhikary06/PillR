// static/js/appwrite_auth.js

// Initialize Appwrite client
const client = new Appwrite();
client.setEndpoint('https://cloud.appwrite.io/v1'); // Replace with your Appwrite endpoint
client.setProject('67bc53100003093552a9'); // Replace with your Appwrite project ID

const account = new Appwrite.Account(client);

// Check if the user is logged in
async function checkAuthStatus() {
    try {
        const session = await account.get();
        document.getElementById('auth-status').innerText = 'Logout';
        document.getElementById('auth-status').href = '#';
        document.getElementById('auth-status').onclick = logout;
    } catch (error) {
        document.getElementById('auth-status').innerText = 'Login';
        document.getElementById('auth-status').href = '/login/';
    }
}

// Register a new user
async function registerUser(email, password, name) {
    try {
        const response = await account.create(Appwrite.ID.unique(), email, password, name);
        alert('Registration successful! Please log in.');
        window.location.href = '/login/';
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Log in a user
async function loginUser(email, password) {
    try {
        const response = await account.createSession(email, password);
        alert('Login successful!');
        window.location.href = '/dashboard/';
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Log out a user
async function logout() {
    try {
        await account.deleteSession('current');
        alert('Logged out successfully!');
        window.location.href = '/login/';
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Call checkAuthStatus on page load
checkAuthStatus();