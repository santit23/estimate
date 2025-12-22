import api from './axios';

export interface RateStructure {
    series: string[];
    qualities: string[];
    materials: MaterialDef[]; // Changed from string[]
    colors: string[];
}

export interface MaterialRate {
    id?: number;
    series: string;
    quality: string;
    color: string;
    material_name: string;
    unit?: string;
    category?: string;
    rate: number;
}

export interface MaterialDef {
    name: string;
    category: string;
    default_unit: string;
}

export interface BulkRateUpdate {
    rates: MaterialRate[];
}

export const ratesApi = {
    getStructure: async (): Promise<RateStructure> => {
        const response = await api.get('/rates/structure');
        return response.data;
    },

    getRates: async (series?: string, quality?: string): Promise<MaterialRate[]> => {
        const params: any = {};
        if (series) params.series = series;
        if (quality) params.quality = quality;

        const response = await api.get('/rates/', { params });
        return response.data;
    },

    bulkUpdate: async (rates: MaterialRate[]): Promise<MaterialRate[]> => {
        const response = await api.post('/rates/bulk', { rates });
        return response.data;
    },

    deleteMaterial: async (materialName: string, series?: string): Promise<void> => {
        await api.delete('/rates/material', { params: { material_name: materialName, series } });
    },

    deleteScope: async (params: { series: string, quality?: string, color?: string }): Promise<void> => {
        await api.delete('/rates/scope', { params });
    }
};
