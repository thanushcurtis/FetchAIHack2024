<template>

  <div class="login-container">   
    <div class="header-container"> 
      <h1 class="logo">TCS Pension Proposer</h1> 
    </div>
    <div class="registration-form">
      <h1 class="form-title">Login</h1>
      <form @submit.prevent="login" class="form">
        <div class="form-group">
          <label for="username" class="form-label">Username:</label>
          <input id="username" v-model="username" type="text" class="form-input" placeholder="Enter your username" required>
        </div>
        <div class="form-group">
          <label for="password" class="form-label">Password:</label>
          <input id="password" v-model="password" type="password" class="form-input" placeholder="Enter your password" required>
        </div>
        <label for="remember-me" class="form-label">
          <input id="remember-me" type="checkbox" class="form-checkbox">
          Remember me
        </label>
        <button type="submit" class="form-button">Login</button>
        <div class="registration-form">
            <router-link  class="reg" to="/register">Register here</router-link>
        </div>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>
     </div>
  
</div>
<div class="box"></div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    login() {
      fetch('/auth/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials:"include",
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      })
      .then(response => {
        if (!response.ok) {
          console.log('Invalid credentials.');
          throw new Error('Invalid credentials.');
        }
        return response.json();
      })
      .then(data => {
        this.$router.push('/home'); 
      })
      .catch(error => {
        console.error('Error:', error);
        this.errorMessage = error.message;
      });
    }
  }
};
</script>


<style scoped>
.header-container {
  z-index: 2;
  width: 800px;
  position: fixed;
  margin-bottom: 600px;
  padding: 30px;
  background-color: #af6b58; /* Butter */
  padding: 1em;
  color: #fff;
  text-align: center;
  border-radius: 8px 8px 8px 8px
}

.logo {
  font-size: 3em;
}

.login-container {
  display: flex;
  z-index: 2;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient( rgb(230, 178, 36), rgb(204, 83, 204));/* Butter Cream */
}

.registration-form {
  z-index: 2;
  margin: 0px 100px;
  padding: 10px 20px; /* Increased padding */
  border-radius: 10px;

}

.form-title {
  text-align: center;
  margin-bottom: 17px;
  color: #8b5a2b; 
  }

.form-group {
  margin-bottom: 15px;
}

.form-label {
  font-weight: bold;
  color: #8b5a2b;
}

.form-input {
  width: 100%;
  padding: 13px;
  border: 1px solid #af6b58;
  border-radius: 5px;
}

.form-button {
  width: 100%;
  padding: 10px 100px;
  border: none;
  border-radius: 5px;
  background-color: #af6b58;; /* Peach */
  color: #f8f5f2; /* Dark Brown */
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


.reg{
  width: 300%;
  padding: 10px 100px;
  border: none;
  border-radius: 5px;
  background-color: #af6b58;; /* Peach */
  color: #f5f4f4; /* Dark Brown */
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-decoration: none;
  text-align: center;

}
.box{
  position: absolute;
  z-index: 1;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 850px;
  height: 600px;
  background: #131d2ac2;
  border-radius: 30px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
  display: flex;
  background-color:  rgba(0, 0, 0, 0.441);
  overflow: hidden;
  justify-content: center;
  align-items: center;
}
.box::before{
  content: '';
  position: absolute;
  width: 140%;
  height: 300px;
  background: #f6f6f6;
  box-shadow: 0 0 20px  rgb(228, 190, 112);;
  animation: animate 4s linear infinite;  
}

.box::after{
  content: '';
  position: absolute;
  inset: 10px;
  background-color: rgb(241, 236, 234);
  border-radius: 30px;
}

@keyframes animate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 