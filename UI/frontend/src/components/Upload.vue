<template>
  <div class="upload-container">
    <input type="file" id="file-input" @change="onFileChange" accept=".pdf" />
    <label for="file-input">Select PDF File</label> <button class="upload-button" @click="upload">Upload</button>
  </div>
</template>

<script>
import { useFilesStore } from '../store/fileStore.js';

export default {
  data() {
    return {
      selectedFile: null,
    };
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
    },
    fetchUser() {
      fetch('/api/whoami/', { credentials: 'include' })
        .then(response => response.json())
        .then(data => {
          this.username = data.username;
        });
    },

    upload() {
      if (!this.selectedFile) {
        alert('No file selected!');
        return;
      }

      let formData = new FormData();
      formData.append('pdf_file', this.selectedFile);

      let uploadUrl = '/api/upload/';
      const filesStore = useFilesStore();

      fetch(uploadUrl, {
        method: 'POST',
        body: formData,
        credentials: 'include',
      })  
      .then(response => {
          if (response.status === 409) {
            throw new Error('A file with this name already exists.');
          }
          return response.json();
        })
              .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            filesStore.getFiles({ name: this.selectedFile.name }); // Update the store
          }
        })
        .catch((error) => {
          console.error(error);
          alert('Failed to upload file');
        });
    },
  },
};
</script>




 