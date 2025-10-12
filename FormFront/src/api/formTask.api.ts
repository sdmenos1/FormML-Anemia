import axios from "axios";
import type { people } from "../types/peopleData";

const API_URL = import.meta.env.VITE_API_URL;

const taskAPI = axios.create({
  baseURL: `${API_URL}/tasks/data/tasks/`,
});

export const addData = (data: people) => taskAPI.post("/", data);
