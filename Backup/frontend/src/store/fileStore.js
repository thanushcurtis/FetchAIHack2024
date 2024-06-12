import { defineStore } from 'pinia';

export const useFilesStore = defineStore('files', {
  state: () => ({
    files: [],
  }),
  actions: {

    deleteFile(fileId) {
      fetch('/api/delete/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: fileId }),
        credentials: 'include'
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            // Handle successful deletion here
            this.files = this.files.filter(file => file.name !== fileId);
          } else if (data.error) {
            console.error('Error:', data.error);
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    // Async action to fetch files from the server
    getFiles() {
      fetch('/api/get_files/', { credentials: 'include' })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          // Assuming the data.files is an array of filenames
          // Update the state with the new files, adding an empty note for each
          this.files = data.files.map(file => ({ name: file, note: '' }));
        })
        .catch(error => {
          console.error('Failed to retrieve files', error);
          alert('Failed to retrieve files');
        });
    }
  }
});
