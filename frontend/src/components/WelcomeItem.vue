<template>
  <div class="upload-container">
    <div 
      class="item dropzone"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @dragenter.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      :class="{ 'dragging': isDragging }"
    >
      <div class="dropzone-content">
        <i class="dropzone-icon">
          <slot name="icon"></slot>
        </i>
        <div class="details">
          <h3>
            <slot name="heading"></slot>
          </h3>
          <slot></slot>
          <div v-if="droppedFiles.length" class="dropped-files">
            <p>Dropped files:</p>
            <ul>
              <li v-for="file in droppedFiles" :key="file.name">
                {{ file.name }} ({{ (file.size / 1024).toFixed(2) }} KB)
                <span v-if="file.uploadStatus" :class="['upload-status', file.uploadStatus]">
                  {{ getStatusText(file.uploadStatus) }}
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <div class="action-buttons" v-if="droppedFiles.length">
      <button 
        class="action-button export-csv" 
        @click="exportToCSV"
        :disabled="isUploading"
      >
        <span class="button-icon">📊</span>
        Export to CSV
      </button>
      <button 
        class="action-button export-html" 
        @click="exportToHTML"
        :disabled="isUploading"
      >
        <span class="button-icon">🌐</span>
        Export to HTML
      </button>
      <button 
        class="action-button import-db" 
        @click="uploadToServer"
        :disabled="isUploading"
      >
        <span class="button-icon">💾</span>
        {{ isUploading ? 'Uploading...' : 'Import to Database' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const isDragging = ref(false)
const droppedFiles = ref([])
const isUploading = ref(false)
const error = ref(null)

const handleDrop = (event) => {
  isDragging.value = false
  const files = Array.from(event.dataTransfer.files)
  droppedFiles.value = files.map(file => ({
    ...file,
    uploadStatus: null
  }))
  error.value = null
}

const getStatusText = (status) => {
  switch (status) {
    case 'uploading': return 'Uploading...'
    case 'success': return '✓ Uploaded'
    case 'error': return '✗ Failed'
    default: return ''
  }
}

const uploadToServer = async () => {
  isUploading.value = true
  error.value = null

  try {
    for (const file of droppedFiles.value) {
      file.uploadStatus = 'uploading'
      
      const formData = new FormData()
      formData.append('file', file)

      await axios.post('/api/reservations/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      file.uploadStatus = 'success'
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to upload files. Please try again.'
    droppedFiles.value.forEach(file => {
      if (file.uploadStatus === 'uploading') {
        file.uploadStatus = 'error'
      }
    })
  } finally {
    isUploading.value = false
  }
}

const exportToCSV = () => {
  // TODO: Implement CSV export
  console.log('Exporting to CSV...')
}

const exportToHTML = () => {
  // TODO: Implement HTML export
  console.log('Exporting to HTML...')
}
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.dropzone {
  margin: 2rem auto;
  padding: 2rem;
  border: 2px dashed var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-soft);
  transition: all 0.3s ease;
  cursor: pointer;
  text-align: center;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.dropzone.dragging {
  border-color: var(--color-heading);
  background-color: var(--color-background-mute);
  transform: scale(1.02);
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.dropzone-icon {
  display: flex;
  place-items: center;
  place-content: center;
  width: 64px;
  height: 64px;
  color: var(--color-heading);
  margin-bottom: 1rem;
}

.details {
  flex: 1;
  text-align: center;
}

h3 {
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 0.8rem;
  color: var(--color-heading);
}

p {
  color: var(--color-text);
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.dropped-files {
  margin-top: 2rem;
  padding: 1rem;
  background-color: var(--color-background);
  border-radius: 6px;
  border: 1px solid var(--color-border);
  width: 100%;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.dropped-files p {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.dropped-files ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropped-files li {
  font-size: 0.9rem;
  color: var(--color-text);
  padding: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.dropped-files li:last-child {
  border-bottom: none;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  color: white;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-button:active {
  transform: translateY(0);
}

.button-icon {
  font-size: 1.2rem;
}

.export-csv {
  background-color: #4CAF50;
}

.export-csv:hover {
  background-color: #45a049;
}

.export-html {
  background-color: #2196F3;
}

.export-html:hover {
  background-color: #1e88e5;
}

.import-db {
  background-color: #9C27B0;
}

.import-db:hover {
  background-color: #8e24aa;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .action-button {
    width: 100%;
    justify-content: center;
  }
}

@media (min-width: 1024px) {
  .dropzone {
    max-width: 800px;
  }
}

.upload-status {
  margin-left: 0.5rem;
  font-size: 0.9rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.upload-status.uploading {
  color: #2196F3;
}

.upload-status.success {
  color: #4CAF50;
}

.upload-status.error {
  color: #f44336;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #ffebee;
  color: #f44336;
  border-radius: 4px;
  text-align: center;
}

.action-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

.action-button:disabled:hover {
  box-shadow: none;
}
</style>
