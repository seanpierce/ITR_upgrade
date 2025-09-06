import apiClient from "./apiClient";

export const fetchSchedule = async () => {
    try {
        const response = await apiClient.get('api/schedule/shows');
        return response?.data;
    } catch (error) {
        console.error("Error fetching schedule content:", error);
        throw error;
    }
};
