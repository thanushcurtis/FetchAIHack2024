<template>
  <div class="register-container">
    <div class="header-container">
      <h1 class="logo">TuiLearn</h1> 
    </div>
    <div class="registration-form">
      <h1 class="form-title">Register</h1>
      <form @submit.prevent="register" class="form">
        <div class="form-group">
          <label for="username" class="form-label">Username:</label>
          <input id="username" v-model="username" type="text" class="form-input" required>
        </div>
        <div class="form-group">
          <label for="email" class="form-label">Email:</label>
          <input id="email" v-model="email" type="email" class="form-input" required>
        </div>
        <div class="form-group">
          <label for="password1" class="form-label">Password:</label>
          <input id="password1" v-model="password1" type="password" class="form-input" required>
        </div>
        <div class="form-group">
          <label for="password2" class="form-label">Confirm Password:</label>
          <input id="password2" v-model="password2" type="password" class="form-input" required>
        </div>
        <button type="submit" class="form-button">Register</button>
        <p v-if="error" class="error-message">{{ error }}</p> 
      </form>
    </div>
    <div class="login registration-form">
      <p> Already have an account? </p>
      <router-link to="/" class="login-button"> Login</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
      error: '' 
    };
  },
  methods: {
    register() {
      const url = '/api/register/';
      const data = {
        username: this.username,
        email: this.email,
        password1: this.password1,
        password2: this.password2
      };
      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      };

      fetch(url, options)
        .then(response => {
          if (!response.ok) {
            return response.json().then(data => {
              const errors = data.errors || {};
              const firstErrorKey = Object.keys(errors)[0]; 
              const errorMessage = errors[firstErrorKey][0]; 
              throw new Error(errorMessage); 
            });
          }
          return response.json();
        })
        .then(data => {
          console.log(data);
          // Reset form fields and error message if registration is successful
          this.username = '';
          this.email = '';
          this.password1 = '';
          this.password2 = '';
          this.error = '';
          this.$router.push('/'); 
        })
        .catch(error => {
          console.error('Error:', error);
          this.error = error.message; // Update error message property
        });
    }
  }
};
</script>

<style scoped>
.header-container {
  width: 800px;
  position: fixed;
  margin-bottom: 700px;
  padding: 30px;
  background-color: #d1b06e; /* Butter */
  padding: 1em;
  color: #fff;
  text-align: center;
  border-radius: 8px 8px 8px 8px
}

.logo {
  font-size: 3em;
  font-weight: bold;
}

.login{
  width: 110%;
}
.login, .registration-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 70%;
}
.login-button {
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  margin-top: 10px;
  width:60%;
  border-radius: 5px;
  background-color: #ffe4b5; /* Peach */
  color: #8b5a2b; /* Dark Brown */
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-align: center; /* Add this line */
}
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #ec957082; /* White Smoke */
}

.registration-form {
  max-width: 500px;
  margin: 0 10px;
  padding: 30px;
  background-color: #fbf3e9; /* Butter Cream */
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  color: #8b5a2b;
  font-weight: bold;
}


.form-title {
  text-align: center;
  margin-bottom: 20px;
  color: #8b5a2b; /* Dark Brown */
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  font-weight: bold;
  color: #8b5a2b; /* Dark Brown */
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #d2b48c; /* Tan */
  border-radius: 5px;
}

.form-button {
  width: 100%;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #ffe4b5; /* Peach */
  color: #8b5a2b; /* Dark Brown */
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.form-button:hover {
  background-color: #ffc87a; /* Light Peach */
}

.error-message {
  color: #ff6347; /* Tomato */
  margin-top: 5px;
  text-align: center;
}
</style>
