<template>
  <div id="main-layout">
    <header>
      <h1>DOCX Proof of Concept</h1>
      <div class="controls">
        <input type="file" @change="handleFileUpload" accept=".docx" />
        <div class="view-toggles">
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

    <main class="view-container" v-if="store.activeQuestion">
      <div v-if="views.editor" class="view-pane">
        <Editor v-model="editableHtml" />
      </div>
      <div v-if="views.result" class="view-pane">
        <!-- This placeholder ensures the content below aligns with the editor's content -->
        <div class="toolbar-placeholder">Live Result</div>
        <div class="render-view ProseMirror" v-html="editableHtml"></div>
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
/* The main container for the two views */
.view-container {
  display: flex;
  padding: 1rem;
  gap: 1rem;
}

/* Each individual view pane (Editor, Result) */
.view-pane {
  flex: 1;
  min-width: 0;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden; /* This is for the rounded corners */
}

/* The rendered HTML view */
.render-view {
  padding: 1rem 2rem;
}

/* Placeholder text when no file is selected */
.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 0;
  color: var(--color-text-muted);
}

/* General layout and header styles */
#main-layout {
  min-height: 100vh;
  background-color: var(--color-background);
  color: var(--color-text);
}
header {
  padding: 1rem;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
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
  padding: 0 1rem;
}
.tab {
  padding: 10px 15px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-muted);
}
.tab.active {
  color: var(--color-text);
  border-bottom-color: var(--color-accent);
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

/* This is the key to aligning the content */
.toolbar-placeholder {
  padding: 8px 1rem;
  background: var(--color-header-bg);
  border-bottom: 1px solid var(--color-border);
  color: var(--color-header-text);
  font-weight: 600;
  min-height: 25px; /* Match the toolbar's icon button height */
}
</style>
