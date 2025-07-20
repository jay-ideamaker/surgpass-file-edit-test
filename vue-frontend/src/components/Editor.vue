<template>
  <div v-if="editor" class="editor-container">
    <div class="toolbar">
      <button @click="editor.chain().focus().toggleBold().run()">Bold</button>
      <button @click="editor.chain().focus().toggleItalic().run()">
        Italic
      </button>
      <button @click="editor.chain().focus().toggleStrike().run()">
        Strike
      </button>
      <button @click="editor.chain().focus().toggleUnderline().run()">
        Underline
      </button>
      <button @click="editor.chain().focus().toggleSuperscript().run()">
        Super
      </button>
      <button @click="editor.chain().focus().toggleSubscript().run()">
        Sub
      </button>
      <button @click="saveContent">Save</button>
    </div>
    <editor-content :editor="editor" />
  </div>
</template>

<script setup lang="ts">
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Underline from "@tiptap/extension-underline";
import Subscript from "@tiptap/extension-subscript";
import Superscript from "@tiptap/extension-superscript";
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
    Subscript,
    Superscript,
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
  border: 1px solid #ccc;
}
.ProseMirror {
  padding: 1rem;
  min-height: 400px;
}
.ProseMirror:focus {
  outline: none;
}
.ProseMirror img {
  max-width: 100%;
  height: auto;
}
.ProseMirror img.ProseMirror-selectednode {
  outline: 3px solid #68cef8;
}
.toolbar {
  padding: 8px;
  background: #f0f0f0;
  border-bottom: 1px solid #ccc;
}
</style>
