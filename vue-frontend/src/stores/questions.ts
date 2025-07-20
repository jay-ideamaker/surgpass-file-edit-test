import { defineStore } from "pinia";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

export interface Question {
  id: number;
  original_filename: string;
  html_content: string;
  pdf_url: string;
}

export const useQuestionStore = defineStore("questions", {
  state: () => ({
    questions: [] as Question[],
    activeQuestionId: null as number | null,
    isLoading: false,
    error: null as string | null,
  }),
  getters: {
    activeQuestion: (state): Question | undefined => {
      return state.questions.find((q) => q.id === state.activeQuestionId);
    },
  },
  actions: {
    async fetchQuestions() {
      this.isLoading = true;
      try {
        const response = await axios.get(`${API_URL}/questions/`);
        this.questions = response.data;
        if (this.questions.length > 0 && !this.activeQuestionId) {
          this.activeQuestionId = this.questions[0].id;
        }
      } catch (e) {
        this.error = "Failed to fetch questions.";
      } finally {
        this.isLoading = false;
      }
    },
    async uploadQuestion(file: File) {
      this.isLoading = true;
      const formData = new FormData();
      formData.append("file", file);
      try {
        const response = await axios.post(`${API_URL}/questions/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        this.questions.push(response.data);
        this.activeQuestionId = response.data.id;
      } catch (e) {
        this.error = "Failed to upload file.";
      } finally {
        this.isLoading = false;
      }
    },
    async deleteQuestion(id: number) {
      try {
        await axios.delete(`${API_URL}/questions/${id}/`);
        this.questions = this.questions.filter((q) => q.id !== id);
        if (this.activeQuestionId === id) {
          this.activeQuestionId = this.questions[0]?.id || null;
        }
      } catch (e) {
        this.error = "Failed to delete question.";
      }
    },
    async saveQuestionContent(id: number, html_content: string) {
      try {
        await axios.put(`${API_URL}/questions/${id}/`, { html_content });
        const question = this.questions.find((q) => q.id === id);
        if (question) {
          question.html_content = html_content;
        }
      } catch (e) {
        this.error = "Failed to save content.";
      }
    },
    setActiveQuestion(id: number) {
      this.activeQuestionId = id;
    },
  },
});
