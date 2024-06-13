<template>
  <div class="container">
    <div v-if="response" class="response">
      <p class="response-content">{{ response }}</p>
    </div>

    <div class="query-section">
      <h2 class="query-heading">Enter Query</h2>
      <div class="input-group">
        <label for="title" class="label">Title:</label>
        <input v-model="formData.title" type="text" id="title" class="input" placeholder="Enter title" required>
      </div>
      <div class="input-group">
        <label for="query" class="label">Query:</label>
        <input v-model="formData.query" type="text" id="query" class="input" placeholder="Enter query" required>
      </div>
      <button @click.prevent="submitForm" class="btn-submit">Submit Query</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        title: '',
        query: ''
      },
      response: null
    }
  },
  methods: {
    submitForm() {
      fetch('/api/server_pdf/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.formData)
      })
      .then(response => response.json())
      .then(data => {
        this.response = data.cohere_response;
      })
      .catch(error => console.error('Error:', error));
    }
  }
}
</script>



