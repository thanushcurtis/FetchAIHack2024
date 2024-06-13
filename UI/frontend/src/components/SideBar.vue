<template>
  <div class="container">
    <ul class="file-list">
      <li v-for="(file, index) in files" :key="index" class="file-item">
        <button @click="goToNewPage(file.name)" class="btn-go">
          <i class="fas fa-search"></i>
        </button>
        <span >
          <h5>{{ file.name }}</h5>
        </span>
        <button class="delete-button" @click="deleteFile(file.name)">
          <i class="fas fa-trash-alt"></i>
        </button>       
      </li>
    </ul>
  </div>
  <div class="toggle-container">
    <button class="upload-button" @click="triggerFileInputClick">
      <input type="file" id="file-input" @change="onFileChange" style="display: none;"  accept=".pdf">
      <i class="fas fa-cloud-upload-alt" ></i> Upload 
    </button>
  </div>
</template>

<script>
import { useFilesStore } from '../store/fileStore.js'; // Ensure this path matches the actual location of your fileStore

export default {
  mounted() {
    const filesStore = useFilesStore();
    filesStore.getFiles();
  },
  computed: {
    files() {
      const filesStore = useFilesStore();
      return filesStore.files;
    },
  },
  created() {
    this.fetchUser();
  },
  methods: {
    triggerFileInputClick() {
      document.getElementById('file-input').click();
    },
    deleteFile(fileName) {
      const filesStore = useFilesStore();
      filesStore.deleteFile(fileName);
    },
    goToNewPage(fileName) {
      this.$router.push({ name: 'NewPage', params: { fileName: fileName } });
    },
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
      if (this.selectedFile) this.upload(); // Upload directly on file selection
    },
    
    fetchUser() {
      fetch('/api/whoami/', { credentials: 'include' })
        .then(response => response.json())
        .then(data => {
          this.username = data.username;
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
  },
  data() {
    return {
      selectedFile: null,
      username: '',
    };
  },
};
</script>
<style>
.file-list {
  list-style-type: none;
  padding: 0;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5em 1em;
  border-bottom: 1px solid #f0f0f0;
  background-color: #131d2a99;
  border: 1px solid #d8c8c86d;
  border-radius: 8px;
  width: 90%;
  margin:15px;
  padding: 15px;
  overflow-wrap: break-word;

}

.delete-button {
  background: none;
  border: none;
  color: rgb(219, 55, 19);
  cursor: pointer;
}

.delete-button:hover {
  color: darkred;
}

.btn-go {
  background: none;
  border: none;
  color: rgb(243, 239, 238);
  cursor: pointer;
}

.upload {
  position: absolute; /* Position the button independently of other elements */
  top: 22em; /* Position from the top */
  left: 1.5em; /* Position from the left */
  color: #f5f1f1;
  border: none;
  padding: 0.5em 1em;
  border-radius: 8px;
  font-size: 1.6em;
  cursor: pointer;
  background-color: rgba(250, 167, 84, 0.718);
  justify-content: center;
}
.upload-button {
  background: none;
  border: none;
  color: #f5f1f1;
  cursor: pointer;
  font-size: 2em;
  border-radius: 0.3em;
  padding: 0.25em ;
  top: 30em; /* Position from the top */
  left: 3.5em;
  position: absolute;

}
</style>