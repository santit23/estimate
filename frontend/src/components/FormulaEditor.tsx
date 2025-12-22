"use client";

import { useState, useEffect } from 'react';
import { X, Save, RotateCcw, CheckCircle, XCircle } from 'lucide-react';
import { formulaApi, type FormulaDisplay, type ValidationResponse } from '../api/formulaApi';

interface FormulaEditorProps {
    productType: string;
    designType: string;
    material: string;
    formula: FormulaDisplay;
    onClose: () => void;
    onSave: () => void;
}

export default function FormulaEditor({
    productType,
    designType,
    material,
    formula,
    onClose,
    onSave
}: FormulaEditorProps) {
    const [expression, setExpression] = useState(formula.expression);
    const [validation, setValidation] = useState<ValidationResponse | null>(null);
    const [isValidating, setIsValidating] = useState(false);
    const [isSaving, setIsSaving] = useState(false);

    // Validate on expression change (debounced)
    useEffect(() => {
        const timer = setTimeout(() => {
            if (expression && expression !== formula.expression) {
                validateExpression();
            }
        }, 500);

        return () => clearTimeout(timer);
    }, [expression]);

    const validateExpression = async () => {
        setIsValidating(true);
        try {
            const result = await formulaApi.validateFormula(
                productType,
                designType,
                material,
                expression
            );
            setValidation(result);
        } catch (error) {
            setValidation({
                valid: false,
                error: 'Failed to validate formula'
            });
        } finally {
            setIsValidating(false);
        }
    };

    const handleSave = async () => {
        if (!validation?.valid) {
            alert('Please fix validation errors before saving');
            return;
        }

        setIsSaving(true);
        try {
            await formulaApi.updateFormula(productType, designType, material, expression);
            alert('Formula updated successfully');
            onSave();
            onClose();
        } catch (error) {
            alert('Failed to update formula');
        } finally {
            setIsSaving(false);
        }
    };

    const handleReset = async () => {
        if (!confirm('Reset this formula to its default value?')) {
            return;
        }

        try {
            await formulaApi.resetFormula(productType, designType, material);
            alert('Formula reset to default');
            onSave();
            onClose();
        } catch (error) {
            alert('Failed to reset formula');
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b">
                    <h2 className="text-xl font-semibold text-gray-900">
                        Edit Formula: {material}
                    </h2>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-500"
                    >
                        <X className="h-6 w-6" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 space-y-6">
                    {/* Formula Info */}
                    <div className="bg-gray-50 p-4 rounded-md">
                        <p className="text-sm text-gray-600 mb-2">
                            <span className="font-medium">Description:</span> {formula.description}
                        </p>
                        <p className="text-sm text-gray-600">
                            <span className="font-medium">Unit:</span> {formula.unit}
                        </p>
                    </div>

                    {/* Expression Input */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Formula Expression
                        </label>
                        <input
                            type="text"
                            value={expression}
                            onChange={(e) => setExpression(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 font-mono text-gray-900"
                            placeholder="e.g., l * 2 or max(l, h)"
                        />
                        <p className="mt-2 text-xs text-gray-500">
                            Variables: <code className="bg-gray-100 px-1 py-0.5 rounded">l</code> (length/width),{' '}
                            <code className="bg-gray-100 px-1 py-0.5 rounded">h</code> (height)
                        </p>
                        <p className="mt-1 text-xs text-gray-500">
                            Functions: max, min, round, ceiling, floor, if
                        </p>
                    </div>

                    {/* Validation Feedback */}
                    {isValidating && (
                        <div className="flex items-center text-sm text-gray-600">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-indigo-600 mr-2"></div>
                            Validating...
                        </div>
                    )}

                    {validation && !isValidating && (
                        <div className={`flex items-start p-4 rounded-md ${validation.valid
                                ? 'bg-green-50 text-green-800'
                                : 'bg-red-50 text-red-800'
                            }`}>
                            {validation.valid ? (
                                <CheckCircle className="h-5 w-5 mr-2 flex-shrink-0 mt-0.5" />
                            ) : (
                                <XCircle className="h-5 w-5 mr-2 flex-shrink-0 mt-0.5" />
                            )}
                            <div className="flex-1">
                                {validation.valid ? (
                                    <div>
                                        <p className="font-medium">Valid formula</p>
                                        {validation.test_result !== undefined && (
                                            <p className="text-sm mt-1">
                                                Test result (l=5, h=4): {validation.test_result.toFixed(2)}
                                            </p>
                                        )}
                                    </div>
                                ) : (
                                    <div>
                                        <p className="font-medium">Invalid formula</p>
                                        {validation.error && (
                                            <p className="text-sm mt-1">{validation.error}</p>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Original Formula */}
                    {formula.expression !== expression && (
                        <div className="bg-blue-50 p-4 rounded-md">
                            <p className="text-sm text-blue-800">
                                <span className="font-medium">Original formula:</span>{' '}
                                <code className="bg-blue-100 px-2 py-1 rounded">{formula.expression}</code>
                            </p>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="flex items-center justify-between p-6 border-t bg-gray-50">
                    <button
                        onClick={handleReset}
                        className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                        <RotateCcw className="h-4 w-4 mr-2" />
                        Reset to Default
                    </button>
                    <div className="flex space-x-3">
                        <button
                            onClick={onClose}
                            className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={handleSave}
                            disabled={!validation?.valid || isSaving}
                            className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white ${validation?.valid && !isSaving
                                    ? 'bg-indigo-600 hover:bg-indigo-700'
                                    : 'bg-gray-400 cursor-not-allowed'
                                }`}
                        >
                            <Save className="h-4 w-4 mr-2" />
                            {isSaving ? 'Saving...' : 'Save Formula'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
