<script setup>
import WelcomeItem from './WelcomeItem.vue'
import IconDocumentation from './icons/IconDocumentation.vue'
</script>

<template>
  <WelcomeItem>
    <template #icon>
      <IconDocumentation />
    </template>
    <template #heading>
      Drop your files here
    </template>
    <p>
      Drag and drop your files into this area to upload them.
    </p>
  </WelcomeItem>
</template>
