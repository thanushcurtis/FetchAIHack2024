<template>
  <div id="app">
    <!-- Header Section -->
    <header class="header">
      <div class="header-container">
        <h1 class="logo">TCS  Pension Proposer</h1>
        <nav>  
          <button @click="logout" class="btn btn-logout"><i class="fas fa-sign-out-alt"></i> Logout</button>
        </nav>
      </div>
    </header>
      
       <div class=content>
        <div class="welcom">
          <h1>Welcome to TCS Pension Proposer </h1>
        </div>
        <Query> </Query> 
       
       </div>

   

    
    <!-- Footer Section -->
    <footer>
      <p>&copy; 2024 TuiLearn. All rights reserved.</p>
    </footer>
  </div>
</template>
<script>
import { defineComponent } from "vue";
import Query from "./Query.vue";
import PDFs from "./SideBar.vue";
import Upload from "./Upload.vue";

export default defineComponent({
  data() {
    return {
      username: null,
      mode: 'query', // Initial mode is set to 'query'
      files: [] // Add files array
    };
  },
  components: {
    Query,
    PDFs,
    Upload,
  },
  methods: {
    logout() {
      fetch('/api/logout/', { method: 'POST', credentials: 'include' })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          console.log('Logout successful');
          this.$router.push('/'); 
        })
        .catch(error => {
          console.log('Logout failed:', error);
        });
    },
  
    getFiles() {
      fetch('/api/get_files/', { credentials: 'include' })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          
          }
          return response.json();
        })
        .then(data => {
          this.files = data.files.map(file => ({ name: file, note: '' }));
        })
        .catch(error => {
          console.error(error);
          alert('Failed to retrieve files');
        });
    }
  },

  created() {
    this.getFiles();
    fetch('/api/whoami/', { credentials: 'include' })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data.isAuthenticated === false) {
          this.username = 'Guest';
        } else {
          this.username = data.username;
        }
      })
      .catch(error => {
        console.log('Fetch failed:', error);
      });
  }
});
</script>

<style scoped>
/* Font Awesome Styles */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

/* Global styles */
body {
  margin: 0;
  padding: 0;
  font-family: "Arial", sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: rgb(246, 242, 232);
}

/* Header styles */
.header {
  background-color: #efa873;
  background-image: linear-gradient(to right, rgb(247, 157, 84), #af6b58);
  padding: 2em;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 3em;
  font-weight: bold;
  color: #fff;
  margin: 0;
}

.nav {
  display: flex;
  gap: 1em; 
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
}

.btn-logout {
  background-color: transparent;
  border: none;
  color: #fff;
  font-size: 1.5em;
  cursor: pointer;
}

/* Toggle button styles */
.toggle-container {
  display: fixed;
  flex-direction: column;
  align-items: center;
  position: absolute;
  top: 20%;
  left: 50%;
}



/* Main Content styles */
.main-container {
  display: flex;
  flex: 1;

}

.sidebar {
  background-color: #121519ba;
  color: #fcf6f6da;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  width: 25rem;  
  margin-left: 5px;
  padding-left: 30px;
  padding-top: 20px;
  max-height: 100vh; 
  
}

.username {
  color: #131212;
  font-size: 1.5em;
  margin-bottom: 1em;
  font-family: Georgia, 'Times New Roman', Times, serif;
}

.content {
  flex: 1;
  margin-left: 25em;
  color: #0b0b0b;

}
.welcom{
  font-size: 20em;
  margin-top: 100px;

}

/* Query Section styles */
.query-container {
  margin: 0 auto;
  background-color: #4b484859;
  margin-top: 100%;
}

/* Footer styles */
footer {
  background-color: #e3ac81;
  color: #fff;
  padding: 0.5em;
  text-align: center;
}

/* Upload Container styles */
.upload-container {
  display: fixed;
  flex-direction: column;
  align-items: center;
  position: absolute;
  top: 50%;
  left: 40%;
 
}


</style>




