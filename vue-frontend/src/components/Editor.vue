<template>
  <div v-if="editor" class="editor-container">
    <div class="toolbar">
      <!-- History -->
      <button
        @click="editor.chain().focus().undo().run()"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M13.5,8C12.7,8,12,7.3,12,6.5V3.4C12,2.6,12.6,2,13.4,2C17.5,2,21,5.5,21,9.6C21,13.8,17.5,17.3,13.4,17.3C11.1,17.3,9.1,16.3,7.8,14.7L9.2,13.3C10.1,14.4,11.6,15.1,13.2,15.1C16.3,15.1,18.8,12.6,18.8,9.5C18.8,6.4,16.3,3.9,13.2,3.9C13.1,3.9,13,3.9,12.9,3.9L13.5,4.5V6.5C13.5,7.3,12.8,8,12,8H13.5Z"
          />
        </svg>
      </button>
      <button
        @click="editor.chain().focus().redo().run()"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M10.5,8C11.3,8,12,7.3,12,6.5V3.4C12,2.6,11.4,2,10.6,2C6.5,2,3,5.5,3,9.6C3,13.8,6.5,17.3,10.6,17.3C12.9,17.3,14.9,16.3,16.2,14.7L14.8,13.3C13.9,14.4,12.4,15.1,10.8,15.1C7.7,15.1,5.2,12.6,5.2,9.5C5.2,6.4,7.7,3.9,10.8,3.9C10.9,3.9,11,3.9,11.1,3.9L10.5,4.5V6.5C10.5,7.3,11.2,8,12,8H10.5Z"
          />
        </svg>
      </button>
      <div class="toolbar-separator"></div>
      <!-- Headings -->
      <button
        @click="editor.chain().focus().setParagraph().run()"
        :class="{ 'is-active': editor.isActive('paragraph') }"
        class="toolbar-button"
      >
        P
      </button>
      <button
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
        class="toolbar-button"
      >
        H1
      </button>
      <button
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
        class="toolbar-button"
      >
        H2
      </button>
      <button
        @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
        class="toolbar-button"
      >
        H3
      </button>
      <div class="toolbar-separator"></div>
      <!-- Marks -->
      <button
        @click="editor.chain().focus().toggleBold().run()"
        :class="{ 'is-active': editor.isActive('bold') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M13.5,15.5H10V12.5H13.5C14.3,12.5,15,13.2,15,14C15,14.8,14.3,15.5,13.5,15.5M10,6.5H13A1.5,1.5 0 0,1 14.5,8A1.5,1.5 0 0,1 13,9.5H10M15.6,10.79C16.57,10.11,17.25,9,17.25,8C17.25,5.74,15.5,4,13.25,4H7V18H14.04C16.14,18,17.75,16.3,17.75,14.21C17.75,12.69,16.89,11.39,15.6,10.79Z"
          />
        </svg>
      </button>
      <button
        @click="editor.chain().focus().toggleItalic().run()"
        :class="{ 'is-active': editor.isActive('italic') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path d="M10,4V7H12.21L8.79,15H6V18H14V15H11.79L15.21,7H18V4H10Z" />
        </svg>
      </button>
      <button
        @click="editor.chain().focus().toggleUnderline().run()"
        :class="{ 'is-active': editor.isActive('underline') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M5,21H19V19H5V21M12,17A6,6 0 0,0 18,11V3H15.5V11A3.5,3.5 0 0,1 12,14.5A3.5,3.5 0 0,1 8.5,11V3H6V11A6,6 0 0,0 12,17Z"
          />
        </svg>
      </button>
      <button
        @click="editor.chain().focus().toggleStrike().run()"
        :class="{ 'is-active': editor.isActive('strike') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M3,14H21V12H3M5,4V7H10.5V10H13.5V7H19V4M10.5,16H13.5V19H10.5V16Z"
          />
        </svg>
      </button>

      <!-- NEW SUPERSCRIPT BUTTON -->
      <button
        @click="editor.chain().focus().toggleSuperscript().run()"
        :class="{ 'is-active': editor.isActive('superscript') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M20.41,5.59L19,7L15.5,3.5L12,7L10.59,5.59L15.5,0.68L20.41,5.59M10,11A4,4 0 0,1 6,15A4,4 0 0,1 2,11V4H4V11A2,2 0 0,0 6,13A2,2 0 0,0 8,11V4H10V11Z"
          />
        </svg>
      </button>
      <!-- NEW SUBSCRIPT BUTTON -->
      <button
        @click="editor.chain().focus().toggleSubscript().run()"
        :class="{ 'is-active': editor.isActive('subscript') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M20.41,18.41L19,17L15.5,20.5L12,17L10.59,18.41L15.5,23.32L20.41,18.41M10,11A4,4 0 0,1 6,15A4,4 0 0,1 2,11V4H4V11A2,2 0 0,0 6,13A2,2 0 0,0 8,11V4H10V11Z"
          />
        </svg>
      </button>

      <div class="toolbar-separator"></div>
      <!-- Nodes -->
      <button
        @click="editor.chain().focus().toggleBulletList().run()"
        :class="{ 'is-active': editor.isActive('bulletList') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M7,5H21V7H7V5M7,11H21V13H7V11M7,17H21V19H7V17M4,4.5A1.5,1.5 0 0,1 5.5,6A1.5,1.5 0 0,1 4,7.5A1.5,1.5 0 0,1 2.5,6A1.5,1.5 0 0,1 4,4.5M4,10.5A1.5,1.5 0 0,1 5.5,12A1.5,1.5 0 0,1 4,13.5A1.5,1.5 0 0,1 2.5,12A1.5,1.5 0 0,1 4,10.5M4,16.5A1.5,1.5 0 0,1 5.5,18A1.5,1.5 0 0,1 4,19.5A1.5,1.5 0 0,1 2.5,18A1.5,1.5 0 0,1 4,16.5Z"
          />
        </svg>
      </button>
      <button
        @click="editor.chain().focus().toggleOrderedList().run()"
        :class="{ 'is-active': editor.isActive('orderedList') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M7,13V11H21V13H7M7,19V17H21V19H7M7,7V5H21V7H7M3,8H4.5V9H2V10H5V5H2V6H3.5V7H2V8H3M2,17H3.5V18H4.5V15H2V16H3.5V16.5H2V17M4.5,12H2V13H3.5V14H2V15H5V10H2V11H4.5V12Z"
          />
        </svg>
      </button>
      <button
        @click="editor.chain().focus().toggleBlockquote().run()"
        :class="{ 'is-active': editor.isActive('blockquote') }"
        class="toolbar-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path d="M14,17H17L19,13V7H13V13H16M6,17H9L11,13V7H5V13H8L6,17Z" />
        </svg>
      </button>
      <button @click="saveContent" class="toolbar-button save-button">
        Save
      </button>
    </div>
    <editor-content :editor="editor" />
  </div>
</template>

<script setup lang="ts">
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Underline from "@tiptap/extension-underline";
import Superscript from "@tiptap/extension-superscript"; // Extension for superscript
import Subscript from "@tiptap/extension-subscript"; // Extension for subscript
import Image from "@tiptap/extension-image";
import { watch, onBeforeUnmount } from "vue";
import { useQuestionStore } from "../stores/questions";
import ResizeImage from "tiptap-extension-resize-image";

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits(["update:modelValue", "save"]);

const editor = useEditor({
  extensions: [
    StarterKit,
    Underline,
    Superscript, // Make sure the extension is registered
    Subscript, // Make sure the extension is registered
    Image.configure({ inline: true }),
    ResizeImage,
  ],
  content: props.modelValue,
  onUpdate: () => {
    emit("update:modelValue", editor.value?.getHTML() || "");
  },
});

watch(
  () => props.modelValue,
  (value) => {
    if (editor.value && editor.value.getHTML() !== value) {
      editor.value.commands.setContent(value, false);
    }
  }
);

const store = useQuestionStore();
const saveContent = () => {
  if (store.activeQuestionId) {
    store.saveQuestionContent(
      store.activeQuestionId,
      editor.value?.getHTML() || ""
    );
  }
};

onBeforeUnmount(() => {
  editor.value?.destroy();
});
</script>

<style>
.editor-container {
  display: flex;
  flex-direction: column;
}

.toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  padding: 8px;
  background: var(--color-header-bg);
  border-bottom: 1px solid var(--color-border);
}

.toolbar-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 25px;
  height: 25px;
  margin-right: 4px;
  border: none;
  background-color: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: 4px;
  font-weight: 500;
}
.toolbar-button svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
}
.toolbar-button:hover {
  background-color: var(--color-border);
  color: var(--color-text);
}
.toolbar-button.is-active {
  background-color: var(--color-accent);
  color: white;
}
.toolbar-button.save-button {
  margin-left: auto;
  width: auto;
  padding: 0 12px;
  background-color: var(--color-accent);
  color: white;
}

.toolbar-separator {
  width: 1px;
  height: 20px;
  background-color: var(--color-border);
  margin: 0 8px;
}

/* This is a shared class with the render-view for consistent styling */
.ProseMirror {
  padding: 1rem 2rem;
  min-height: 400px;
}
.ProseMirror:focus {
  outline: none;
}
.ProseMirror img {
  max-width: 100%;
  height: auto;
  cursor: pointer;
}
.ProseMirror img.ProseMirror-selectednode {
  outline: 3px solid var(--color-accent);
}
.ProseMirror p {
  margin: 0 0 1rem 0;
}
.ProseMirror h1,
.ProseMirror h2,
.ProseMirror h3 {
  margin: 1.5rem 0 1rem 0;
  line-height: 1.2;
}
.ProseMirror blockquote {
  border-left: 3px solid var(--color-border);
  margin: 1.5rem 0;
  padding-left: 1rem;
  color: var(--color-text-muted);
}
</style>
