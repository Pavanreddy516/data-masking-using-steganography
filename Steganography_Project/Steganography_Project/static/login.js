// Wait for the DOM to fully load before executing the script
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form'); // Get the login form
  
    // Add a submit event listener to the form
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault(); // Prevent the default form submission behavior
  
      // Get form data
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
  
      // Prepare the data to be sent in the POST request
      const data = {
        email: email,
        password: password,
      };
  
      try {
        // Send the data to the Flask backend
        const response = await fetch('/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json', // Specify the content type
          },
          body: JSON.stringify(data), // Send data as a JSON string
        });
  
        const result = await response.json(); // Parse the JSON response
  
        if (response.ok) {
          // If login is successful, redirect to the dashboard
          alert(result.message); // Show a success message (from Flask)
          window.location.href = '/dashboard'; // Redirect to the dashboard
        } else {
          // If login fails, show an error message
          alert(result.message || 'Login failed. Please try again.');
        }
      } catch (error) {
        console.error('Error:', error); // Log any errors
        alert('An error occurred while processing your login. Please try again.');
      }
    });
  });
                          