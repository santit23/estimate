"use client";

import { useState, useEffect } from 'react';
import { X, Edit2, Info } from 'lucide-react';
import { formulaApi, type FormulaListResponse, type FormulaDisplay } from '../api/formulaApi';
import FormulaEditor from './FormulaEditor';

interface FormulaViewerProps {
    productType: string;
    designType: string;
    onClose: () => void;
}

export default function FormulaViewer({ productType, designType, onClose }: FormulaViewerProps) {
    const [formulas, setFormulas] = useState<Record<string, FormulaDisplay>>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [editingFormula, setEditingFormula] = useState<{
        material: string;
        formula: FormulaDisplay;
    } | null>(null);

    useEffect(() => {
        loadFormulas();
    }, [productType, designType]);

    const loadFormulas = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await formulaApi.getFormulas(productType, designType);
            setFormulas(response.formulas);
        } catch (err: any) {
            setError(err.message || 'Failed to load formulas');
        } finally {
            setLoading(false);
        }
    };

    const handleFormulaUpdate = () => {
        setEditingFormula(null);
        loadFormulas(); // Reload to get updated formulas
    };

    // Categorize formulas
    const categorizeFormulas = () => {
        const categories: Record<string, Array<[string, FormulaDisplay]>> = {
            'Profiles': [],
            'Hardware': [],
            'Glass & Seals': [],
            'Mesh/Jali': [],
            'Other': []
        };

        Object.entries(formulas).forEach(([material, formula]) => {
            if (material.includes('fr') || material.includes('sht') || material.match(/^\d/)) {
                categories['Profiles'].push([material, formula]);
            } else if (material.includes('jali')) {
                categories['Mesh/Jali'].push([material, formula]);
            } else if (material.includes('glass') || material.includes('gasket') || material.includes('brush') || material.includes('silicon')) {
                categories['Glass & Seals'].push([material, formula]);
            } else if (material.includes('roller') || material.includes('lock') || material.includes('guide') || material.includes('handle') || material.includes('clip') || material.includes('angle')) {
                categories['Hardware'].push([material, formula]);
            } else {
                categories['Other'].push([material, formula]);
            }
        });

        return categories;
    };

    const categories = categorizeFormulas();

    return (
        <>
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-40">
                <div className="bg-white rounded-lg shadow-xl max-w-5xl w-full mx-4 max-h-[90vh] overflow-hidden flex flex-col">
                    {/* Header */}
                    <div className="flex items-center justify-between p-6 border-b">
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900">
                                Formulas: {designType}
                            </h2>
                            <p className="mt-1 text-sm text-gray-500">
                                View and edit calculation formulas for this design
                            </p>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-500"
                        >
                            <X className="h-6 w-6" />
                        </button>
                    </div>

                    {/* Content */}
                    <div className="flex-1 overflow-y-auto p-6">
                        {loading && (
                            <div className="flex items-center justify-center py-12">
                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                                <span className="ml-3 text-gray-600">Loading formulas...</span>
                            </div>
                        )}

                        {error && (
                            <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-800">
                                <p className="font-medium">Error loading formulas</p>
                                <p className="text-sm mt-1">{error}</p>
                            </div>
                        )}

                        {!loading && !error && (
                            <div className="space-y-6">
                                {/* Info Banner */}
                                <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                                    <div className="flex">
                                        <Info className="h-5 w-5 text-blue-600 mr-2 flex-shrink-0 mt-0.5" />
                                        <div className="text-sm text-blue-800">
                                            <p className="font-medium">Formula Variables</p>
                                            <p className="mt-1">
                                                <code className="bg-blue-100 px-1 py-0.5 rounded">l</code> = length/width (feet), {' '}
                                                <code className="bg-blue-100 px-1 py-0.5 rounded">h</code> = height (feet)
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                {/* Categories */}
                                {Object.entries(categories).map(([category, items]) => {
                                    if (items.length === 0) return null;

                                    return (
                                        <div key={category} className="border border-gray-200 rounded-lg overflow-hidden">
                                            <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
                                                <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider">
                                                    {category}
                                                </h3>
                                            </div>
                                            <div className="overflow-x-auto">
                                                <table className="min-w-full divide-y divide-gray-200">
                                                    <thead className="bg-gray-50">
                                                        <tr>
                                                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                                Material
                                                            </th>
                                                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                                Formula
                                                            </th>
                                                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                                Description
                                                            </th>
                                                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                                Unit
                                                            </th>
                                                            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                                Action
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="bg-white divide-y divide-gray-200">
                                                        {items.map(([material, formula]) => (
                                                            <tr key={material} className="hover:bg-gray-50">
                                                                <td className="px-4 py-3 whitespace-nowrap">
                                                                    <div className="flex items-center">
                                                                        <span className="text-sm font-medium text-gray-900">
                                                                            {material}
                                                                        </span>
                                                                        {formula.is_custom && (
                                                                            <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                                                                                Custom
                                                                            </span>
                                                                        )}
                                                                    </div>
                                                                </td>
                                                                <td className="px-4 py-3">
                                                                    <code className="text-sm text-indigo-600 bg-indigo-50 px-2 py-1 rounded font-mono">
                                                                        {formula.expression}
                                                                    </code>
                                                                </td>
                                                                <td className="px-4 py-3 text-sm text-gray-600">
                                                                    {formula.description}
                                                                </td>
                                                                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                                                                    {formula.unit}
                                                                </td>
                                                                <td className="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
                                                                    <button
                                                                        onClick={() => setEditingFormula({ material, formula })}
                                                                        className="text-indigo-600 hover:text-indigo-900 inline-flex items-center"
                                                                    >
                                                                        <Edit2 className="h-4 w-4 mr-1" />
                                                                        Edit
                                                                    </button>
                                                                </td>
                                                            </tr>
                                                        ))}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>

                    {/* Footer */}
                    <div className="flex justify-end p-6 border-t bg-gray-50">
                        <button
                            onClick={onClose}
                            className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                        >
                            Close
                        </button>
                    </div>
                </div>
            </div>

            {/* Formula Editor Modal */}
            {editingFormula && (
                <FormulaEditor
                    productType={productType}
                    designType={designType}
                    material={editingFormula.material}
                    formula={editingFormula.formula}
                    onClose={() => setEditingFormula(null)}
                    onSave={handleFormulaUpdate}
                />
            )}
        </>
    );
}
