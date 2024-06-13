<template> 
      <button @click="clearChatHistory" class="btn-clear">
        <i class="fa fa-refresh"></i> 
        Clear
      </button>
   
    
    <div class="chat-container">
      <div v-for="(message, index) in chatHistory[currentTitle] || []" :key="index" class="chat-message">
        <p :class="{ 'user-message': message.type === 'query', 'tui-message': message.type === 'response' }">
          <span class="username">
            {{ message.type === 'query' ? 'You:' : 'Tui:' }}
          </span>
          {{ message.text }}
        </p>
      </div>
  </div>

  <button class="upload-button" @click="triggerFileInputClick">
    <input type="file" id="file-input" @change="onFileChange" style="display: none;"  accept=".pdf">
    <i class="fas fa-cloud-upload-alt" ></i> Upload User Data
  </button>

    <form @submit.prevent="submitForm" class="chat-form">
      
      
      <div class="input-group">
        <label for="query" class="label">Query:</label>
        <input type="text" id="query" v-model="newQuery" required>
      </div>
      <button type="submit" class="btn-submit"><i class="fas fa-paper-plane"></i></button>
      <button @click="toggleListening" class="btn-listen">
        <i class="fas fa-microphone"></i>
      </button>
    </form>
   

</template>
<script>
export default {
  data() {
    return {
      username: null,
      chatHistory: {},
      newQuery: '',
      currentTitle: '',
      fileContent: '',
      isListening: false,
    };
  },
  watch: {
    '$route.params.fileName': function(newVal, oldVal) {
      this.currentTitle = newVal;
      this.fetchFileContent();
      this.loadChatHistory(); // Load chat history when the route changes
    },
  },
  created() {
    this.currentTitle = this.$route.params.fileName;
    this.loadChatHistory();
    this.fetchUser();
    this.fetchFileContent(); // Load chat history when the component is created
  },
  methods: {
    triggerFileInputClick() {
      document.getElementById('file-input').click();
    },
     submitForm() {
      const currentTitle = this.currentTitle;

      if (!this.chatHistory[currentTitle]) {
        this.chatHistory[currentTitle] = [];
      }

      this.chatHistory[currentTitle].push({
        type: 'query',
        text: this.newQuery,
      });

      // Simulate server response
      fetch('/api/server_pdf/', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: currentTitle,
          query: this.chatHistory[currentTitle][this.chatHistory[currentTitle].length - 1].text, // Send the latest query
        }),
      })
      .then(response => response.json())
      .then(data => {
        this.chatHistory[currentTitle].push({ type: 'response', text: data.cohere_response });
        this.saveChatHistory(); // Save chat history after updating it
      })
      .catch(error => console.error('Error:', error));

      this.newQuery = '';
    },
    saveChatHistory() {
      localStorage.setItem('chatHistory', JSON.stringify(this.chatHistory));
    },
    loadChatHistory() {
      if (localStorage.getItem('chatHistory')) {
        this.chatHistory = JSON.parse(localStorage.getItem('chatHistory'));
      }
    },
    clearChatHistory() {
      if (this.chatHistory[this.currentTitle]) {
        this.chatHistory[this.currentTitle] = [];
        this.saveChatHistory(); // Save  to local storage
      }
    },
    fetchFileContent() {
        fetch(`/api/retrieve/?title=${encodeURIComponent(this.currentTitle)}`, {
          credentials: 'include'
        })
          .then(response => response.blob())
          .then(blob => {
            this.fileContent = URL.createObjectURL(blob);
          });
      },
      upload() {
      if (!this.selectedFile) return; // Handle no file selected

      let formData = new FormData();
      formData.append('pdf_file', this.selectedFile);

      let uploadUrl = '/api/upload/'; // Replace with your actual upload URL
      const filesStore = useFilesStore();

      fetch(uploadUrl, {
        method: 'POST',
        body: formData,
        credentials: 'include', // Include credentials if necessary for your server
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            filesStore.getFiles(); // Update the store on successful upload
          }
        })
        .catch((error) => {
          console.error(error);
          alert('Failed to upload file');
        });
    },

    fetchUser() {
      fetch('/api/whoami/', { credentials: 'include' })
        .then(response => response.json())
        .then(data => {
          this.username = data.username;
        });
    },
    toggleListening() {
      const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      if (this.isListening) {
        recognition.stop();
      } else {
        recognition.lang = 'en-US';
        recognition.onresult = event => {
          this.newQuery = event.results[0][0].transcript;
          this.submitForm();
        };
        recognition.start();
      }
      this.isListening = !this.isListening;
    }
  }, 
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 67%; 
  max-height: 600px;
  padding: 0.8rem;
  overflow-y: auto;
  margin: 1rem auto; 
  width: 90%;
  
}

.chat-title {
  color: #333;
  font-size: 2rem;
  
  border-bottom: 1px solid #ccc;
}

.chat-message {
  margin-bottom: 0.5rem;
}

.user-message,
.tui-message {
  display: inline-block;
  padding: 10px;
  border-radius: 10px;
  margin: 5px 0;
  max-width: 70%;
}

.user-message {
  align-self: flex-end;
  color: #f5f5f0; 
  background-color: #163dd9e3;
  border-radius: 20px 20px 0 20px;
  padding: 8px 16px;
  font-family: 'Georgia', serif;
  font-size: 1.3em;
}

.tui-message {
  align-self: flex-start;
  color: #000;
  background-color:  #fff;
  border-radius: 20px 20px 20px 0;
  font-family: 'Georgia', serif;
  font-size: 1.3em;
}

.chat-form {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1em;
  background-color: #e6c09cf9;
  border-radius: 20px;
  width: 60%;
  top: 55em; /* Position from the top */
  left: 36em;
  position: absolute;
  
}

.input-group {
  flex-grow: 1;
  margin-right: 1em;
 
}

.label {
  display: none;
}

#query {
  width: 100%;
  padding: 0.5em;
  border: 1px solid #ddd;
  border-radius: 4px;
  
}

.btn-submit{
  padding: 0.5em 1em;
  background-color: #f67352af;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-listen {
  padding: 0.5em 1em;
  background-color: #5a46edaf;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-left: 10px;
}

.btn-submit:hover {
  background-color: #0056b3;
}


.btn-clear {
  padding: 0.5em 1em;
  background-color: #ff6666;
  color: #fff;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;  
  font-size:large;
  margin-left: 20px;
  margin-bottom: 10px;
  margin-right: 40px;
}

.btn-clear:hover {
  background-color: #cc0000;
}
.btn-speak {
  margin-left: 5px;
  border: none;
  background: none;
  color: #007bff;
  cursor: pointer;
}


.file_content {
  position: fixed;
  right: 0;
  width: 22%;
  height: 60%;
  overflow: auto;
  background-color: #120e0e5c;
  border-radius: 3%;
  margin-right: 20px;
  display: flex;
  top:15%;
  border: #000;
  
}

.upload-button {
  padding: 1.2em 2em;
  background-color:#135ee8fa;
  color: #fff;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;  
  font-size:large;
  margin-left: 240px;
  margin-top: 340px;

}
</style>





