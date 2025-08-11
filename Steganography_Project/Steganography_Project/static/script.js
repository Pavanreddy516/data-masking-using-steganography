const apiUrl = "http://127.0.0.1:5000"; 

// Login Form
document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${apiUrl}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (response.ok) {
        // Store token in localStorage
        localStorage.setItem('access_token', data.access_token);
        // Redirect to the token view page with token passed as query parameter
        window.location.href = `/view_token?token=${data.access_token}`;
    } else {
        alert(data.message || 'Login failed');
    }
});

// Token verification form

// Redirect to steganography page after token verification
document.getElementById('verify-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = document.getElementById('token').value;

    const response = await fetch(`${apiUrl}/verify_token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token }),
    });

    const data = await response.json();
    const resultDiv = document.getElementById('verification-result');
    
    if (response.ok) {
        // Token is verified
        resultDiv.innerHTML = `<p style="color: green;">${data.message}</p>`;
        setTimeout(() => {
            window.location.href = '/steganography'; // Navigate to steganography page
        }, 1000);
    } else {
        // Token verification failed
        resultDiv.innerHTML = `<p style="color: red;">${data.message}</p>`;
    }
});

// Embed Data into Image
document.getElementById('embed-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const image = document.getElementById('image').files[0];
    const data = document.getElementById('data').value;
    const password = document.getElementById('password').value;

    if (!image || !data || !password) {
        alert("Please fill all the fields.");
        return;
    }

    const formData = new FormData();
    formData.append('image', image);
    formData.append('data', data);
    formData.append('password', password);

    try {
        console.log("Sending request to backend...");
        const response = await fetch(`${apiUrl}/embed`, {
            method: 'POST',
            body: formData
        });

        console.log("Response received:", response);

        if (response.ok) {
            const result = await response.json();
            alert(`Data embedded successfully! File saved at: ${result.output_path}`);
        } else {
            const errorData = await response.json();
            alert(`Failed to embed data: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error during embedding:', error);
        alert('An error occurred while embedding data');
    }
});


document.getElementById('extract-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const image = document.getElementById('extract-image').files[0];
    const password = document.getElementById('extract-password').value;

    if (!image || !password) {
        alert("Please provide an image and password.");
        return;
    }

    const formData = new FormData();
    formData.append('image', image);
    formData.append('password', password);

    try {
        const response = await fetch(`${apiUrl}/extract`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('extracted-data').textContent = `Extracted Data: ${result.message}`;
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Error during extraction:', error);
        alert('An error occurred while extracting data.');
    }
});
