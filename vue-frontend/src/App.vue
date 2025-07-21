<template>
  <div id="main-layout">
    <header>
      <h1>DOCX Proof of Concept</h1>
      <div class="controls">
        <input type="file" @change="handleFileUpload" accept=".docx" />
        <div class="view-toggles">
          <!-- PDF checkbox is now removed -->
          <label><input type="checkbox" v-model="views.editor" /> Editor</label>
          <label><input type="checkbox" v-model="views.result" /> Result</label>
        </div>
      </div>
    </header>

    <div class="tab-bar">
      <!-- Tab bar logic remains the same -->
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

    <!-- The main content area, now using Flexbox -->
    <main class="view-container" v-if="store.activeQuestion">
      <!-- PDF view-pane is now removed -->
      <div v-if="views.editor" class="view-pane">
        <h3>Tiptap Editor</h3>
        <Editor v-model="editableHtml" />
      </div>
      <div v-if="views.result" class="view-pane">
        <h3>Live Result</h3>
        <div class="render-view" v-html="editableHtml"></div>
      </div>
    </main>
    <div v-else class="placeholder">
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
  // pdf property is now removed
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
    target.value = "";
  }
};
</script>

<style>
/* --- NEW LAYOUT AND THEME STYLES --- */

/* The main container for the two views */
.view-container {
  display: flex; /* Use flexbox for dynamic sizing */
  flex-grow: 1;
  overflow: hidden; /* Prevent content from overflowing the container */
}

/* Each individual view pane (Editor, Result) */
.view-pane {
  flex: 1; /* Each pane will take up equal space */
  min-width: 0; /* Important for flex items to shrink properly */
  border-left: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
}
.view-container > .view-pane:first-child {
  border-left: none;
}

/* Styling for the pane headers */
.view-pane h3 {
  padding: 0.5rem 1rem;
  margin: 0;
  background: var(--color-header-bg);
  color: var(--color-header-text);
  font-weight: 600;
  flex-shrink: 0; /* Prevent header from shrinking */
}

/* The rendered HTML view */
.render-view {
  padding: 1rem;
  overflow-y: auto;
  flex-grow: 1;
  background-color: var(--color-surface);
}

/* Placeholder text when no file is selected */
.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  color: var(--color-text-muted);
}

/* General layout and header styles */
#main-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--color-background);
  color: var(--color-text);
}
header {
  padding: 1rem;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}
.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}
.view-toggles label {
  margin-left: 1rem;
}

/* Tab bar styles */
.tab-bar {
  display: flex;
  background: var(--color-background);
  border-bottom: 1px solid var(--color-border);
  overflow-x: auto;
  flex-shrink: 0;
}
.tab {
  padding: 10px 15px;
  cursor: pointer;
  border-right: 1px solid var(--color-border);
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-muted);
}
.tab.active {
  background: var(--color-surface);
  color: var(--color-text);
  font-weight: 500;
}
.delete-btn {
  background: none;
  border: none;
  color: #e53e3e;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  line-height: 1;
}
</style>
