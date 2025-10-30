<template>
  <el-container style="height: 100vh">
    <el-header height="56px" class="app-header">
      <div class="brand">种呱得呱助手</div>
      <div class="nav">
        <el-button link @click="$router.push('/cards')">卡牌</el-button>
        <el-button link @click="$router.push('/pendants')">挂件</el-button>
        <el-button link @click="$router.push('/help/effects')">效果教程</el-button>
      </div>
      <div class="spacer" />
      <div class="version">M1</div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
  
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-header { display: flex; align-items: center; gap: 16px; }
.brand { font-weight: 600; }
.nav { display: flex; gap: 8px; }
.spacer { flex: 1; }
.version { opacity: 0.7; }
</style>

