<template>
  <form @submit.prevent="uploadFile">
    <div>
      <label for="account_id">Account ID:</label>
      <input type="text" v-model="accountId" required />
    </div>
    <div>
      <label for="file">Upload CSV:</label>
      <input type="file" @change="handleFileUpload" required />
    </div>
    <div>
      <label for="column_mapper">Column Mapper (JSON):</label>
      <textarea v-model="columnMapper" required rows="10" cols="35"></textarea>
    </div>
    <button type="submit">Upload</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const accountId = ref('')
const file = ref<File | null>(null)
const columnMapper = ref(`
    {
      "date": "Date",
      "description": "Description",
      "amount": "Amount",
      "date_format": "%d/%m/%Y",
      "category": "Category"
    }`)

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    file.value = target.files[0]
  }
}

const uploadFile = async () => {
  if (!file.value || !accountId.value || !columnMapper.value) return

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('column_mapper', JSON.stringify(JSON.parse(columnMapper.value)))

  try {
    await axios.post(`http://localhost:5001/accounts/${accountId.value}/transactions/import`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    alert('File uploaded successfully')
  } catch (error) {
    console.error('Error uploading file:', error)
    alert('Failed to upload file')
  }
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
