<template>
  <div id="main-layout">
    <header>
      <h1>DOCX Proof of Concept</h1>
      <div class="controls">
        <input type="file" @change="handleFileUpload" accept=".docx" />
        <div class="view-toggles">
          <label><input type="checkbox" v-model="views.pdf" /> PDF View</label>
          <label><input type="checkbox" v-model="views.editor" /> Editor</label>
          <label><input type="checkbox" v-model="views.result" /> Result</label>
        </div>
      </div>
    </header>

    <div class="tab-bar">
      <div
        v-for="q in store.questions"
        :key="q.id"
        class="tab"
        :class="{ active: q.id === store.activeQuestionId }"
        @click="store.setActiveQuestion(q.id)"
      >
        <span>{{ q.original_filename }}</span>
        <button class="delete-btn" @click.stop="store.deleteQuestion(q.id)">
          ×
        </button>
      </div>
    </div>

    <main class="content-grid" v-if="store.activeQuestion">
      <div v-if="views.pdf" class="view-pane">
        <h3>Original DOCX (as PDF)</h3>
        <iframe :src="store.activeQuestion.pdf_url" frameborder="0"></iframe>
      </div>
      <div v-if="views.editor" class="view-pane">
        <h3>Tiptap Editor</h3>
        <Editor v-model="editableHtml" />
      </div>
      <div v-if="views.result" class="view-pane">
        <h3>Live Result</h3>
        <div class="render-view" v-html="editableHtml"></div>
      </div>
    </main>
    <div v-else>
      <p>Upload a .docx file to get started.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, watch } from "vue";
import { useQuestionStore } from "./stores/questions";
import Editor from "./components/Editor.vue";

const store = useQuestionStore();
const editableHtml = ref("");

const views = reactive({
  pdf: true,
  editor: true,
  result: true,
});

onMounted(() => {
  store.fetchQuestions();
});

watch(
  () => store.activeQuestion,
  (newQuestion) => {
    editableHtml.value = newQuestion?.html_content || "";
  },
  { immediate: true }
);

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    await store.uploadQuestion(target.files[0]);
    target.value = ""; // Reset file input
  }
};
</script>

<style>
/* Add some basic styling */
body {
  font-family: sans-serif;
  margin: 0;
}
#main-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
header {
  padding: 1rem;
  background: #333;
  color: white;
}
.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}
.tab-bar {
  display: flex;
  background: #f0f0f0;
  border-bottom: 1px solid #ccc;
  overflow-x: auto;
}
.tab {
  padding: 10px 15px;
  cursor: pointer;
  border-right: 1px solid #ccc;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
}
.tab.active {
  background: #ddd;
}
.delete-btn {
  background: none;
  border: none;
  color: red;
  cursor: pointer;
  font-size: 1.2rem;
}
.content-grid {
  display: flex;
  flex-grow: 1;
}
.view-pane {
  flex: 1;
  border-left: 1px solid #ccc;
  display: flex;
  flex-direction: column;
}
.view-pane:first-child {
  border-left: none;
}
.view-pane h3 {
  padding: 0.5rem;
  margin: 0;
  background: #eee;
}
.view-pane iframe {
  width: 100%;
  height: 100%;
  border: none;
}
.render-view {
  padding: 1rem;
  overflow-y: auto;
  flex-grow: 1;
}
</style>
