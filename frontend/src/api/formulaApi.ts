import api from '../app/api/axios';

export interface FormulaDisplay {
    expression: string;
    description: string;
    unit: string;
    constraints: Record<string, any>;
    is_custom: boolean;
    modified_by?: string;
    modified_at?: string;
}

export interface FormulaListResponse {
    formulas: Record<string, FormulaDisplay>;
    product_type: string;
    design_type: string;
}

export interface ValidationResponse {
    valid: boolean;
    error?: string;
    test_result?: number;
}

export const formulaApi = {
    /**
     * Get all formulas for a product type and design
     */
    async getFormulas(productType: string, designType: string): Promise<FormulaListResponse> {
        const response = await api.get(`/estimates/formulas/${productType}/${designType}`);
        return response.data;
    },

    /**
     * Update a specific formula
     */
    async updateFormula(
        productType: string,
        designType: string,
        material: string,
        expression: string
    ): Promise<{ success: boolean; message: string }> {
        const response = await api.put(
            `/estimates/formulas/${productType}/${designType}/${material}`,
            { expression }
        );
        return response.data;
    },

    /**
     * Reset a formula to default
     */
    async resetFormula(
        productType: string,
        designType: string,
        material: string
    ): Promise<{ success: boolean; message: string }> {
        const response = await api.post(
            `/estimates/formulas/${productType}/${designType}/${material}/reset`
        );
        return response.data;
    },

    /**
     * Validate a formula expression
     */
    async validateFormula(
        productType: string,
        designType: string,
        material: string,
        expression: string
    ): Promise<ValidationResponse> {
        const response = await api.post(
            `/estimates/formulas/${productType}/${designType}/${material}/validate`,
            { expression }
        );
        return response.data;
    },
};
