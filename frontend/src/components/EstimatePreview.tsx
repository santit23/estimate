import React, { useState } from 'react';
import { X, Printer, Edit2 } from 'lucide-react';

interface EstimateItem {
    design: string;
    series: string;
    quality: string;
    color: string;
    width: number;
    height: number;
    quantity: number;
    area: number;
    unit_rate: number;
    amount: number;
    is_active?: boolean;
}

interface Estimate {
    id: number;
    customer_name: string;
    customer_phone: string | null | undefined;
    created_at: string;
    total_amount: number;
    total_area: number;
    transport_cost?: number;
    profit_margin?: number;
    items: EstimateItem[];
}

interface EstimatePreviewProps {
    estimate: Estimate;
    onClose: () => void;
}

export default function EstimatePreview({ estimate, onClose }: EstimatePreviewProps) {
    const [editableNote, setEditableNote] = useState(
        "Thank you for your business! This quotation is valid for 15 days."
    );
    const [isEditingNote, setIsEditingNote] = useState(false);

    const handlePrint = () => {
        window.print();
    };

    // Filter active items for the manufacturing/client view
    const activeItems = estimate.items.filter(item => item.is_active !== false);

    // Calculate totals based on active items if not strictly enforced by backend yet
    // (Though backend should have handled this, we double check for display)
    const subtotal = activeItems.reduce((sum, item) => sum + item.amount, 0);
    const transport = estimate.transport_cost || 0;
    const total = subtotal + transport;

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center print:bg-white print:static print:h-auto print:w-auto print:block">
            <div className="relative bg-white rounded-lg shadow-xl max-w-4xl w-full mx-auto my-8 print:shadow-none print:w-full print:max-w-none print:m-0 print:rounded-none">

                {/* Header / Actions - Hidden in Print */}
                <div className="flex justify-between items-center p-4 border-b print:hidden">
                    <h2 className="text-xl font-semibold text-gray-900">Quotation Preview</h2>
                    <div className="flex space-x-2">
                        <button
                            onClick={handlePrint}
                            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                        >
                            <Printer className="h-4 w-4 mr-2" />
                            Print / Download PDF
                        </button>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-500"
                        >
                            <X className="h-6 w-6" />
                        </button>
                    </div>
                </div>

                {/* Printable Content */}
                <div className="p-8 print:p-0" id="quotation-content">
                    {/* Header */}
                    <div className="flex justify-between items-start mb-8 border-b pb-8">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">QUOTATION</h1>
                            <p className="text-sm text-gray-500 mt-2">Estimate #{estimate.id}</p>
                            <p className="text-sm text-gray-500">Date: {new Date(estimate.created_at).toLocaleDateString()}</p>
                        </div>
                        <div className="text-right">
                            <h3 className="text-lg font-bold text-gray-900">Baba Aluminium</h3>
                            <p className="text-gray-600 text-sm">Kathmandu, Nepal</p>
                            <p className="text-gray-600 text-sm">Phone: 9800000000</p>
                        </div>
                    </div>

                    {/* Customer Info */}
                    <div className="mb-8">
                        <h3 className="text-gray-600 text-sm font-semibold uppercase tracking-wider mb-2">Bill To:</h3>
                        <p className="text-xl font-bold text-gray-900">{estimate.customer_name}</p>
                        {estimate.customer_phone && (
                            <p className="text-gray-600">{estimate.customer_phone}</p>
                        )}
                    </div>

                    {/* Items Table */}
                    <table className="min-w-full divide-y divide-gray-200 mb-8">
                        <thead>
                            <tr className="border-b border-gray-200">
                                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Dimensions</th>
                                <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Qty</th>
                                <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Rate</th>
                                <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {activeItems.map((item, index) => (
                                <tr key={index}>
                                    <td className="px-3 py-4 text-sm text-gray-900">
                                        <div className="font-medium">
                                            {item.design.replace(/_/g, ' ').toUpperCase()}
                                        </div>
                                        <div className="text-gray-500 text-xs">
                                            {item.series} | {item.quality.toUpperCase()} | {item.color.toUpperCase()}
                                        </div>
                                    </td>
                                    <td className="px-3 py-4 text-sm text-gray-500">
                                        {item.width}ft x {item.height}ft
                                        <div className="text-xs">({item.area.toFixed(2)} sqft)</div>
                                    </td>
                                    <td className="px-3 py-4 text-sm text-gray-900 text-right">{item.quantity}</td>
                                    <td className="px-3 py-4 text-sm text-gray-900 text-right">₹{item.unit_rate.toFixed(2)}</td>
                                    <td className="px-3 py-4 text-sm text-gray-900 text-right font-medium">₹{item.amount.toFixed(2)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    {/* Totals */}
                    <div className="flex justify-end border-t pt-8">
                        <div className="w-64">
                            <div className="flex justify-between py-2">
                                <span className="text-gray-600">Subtotal:</span>
                                <span className="text-gray-900 font-medium">₹{subtotal.toFixed(2)}</span>
                            </div>
                            {transport > 0 && (
                                <div className="flex justify-between py-2">
                                    <span className="text-gray-600">Transportation:</span>
                                    <span className="text-gray-900 font-medium">₹{transport.toFixed(2)}</span>
                                </div>
                            )}
                            <div className="flex justify-between py-2 border-t border-gray-200 mt-2">
                                <span className="text-lg font-bold text-gray-900">Total:</span>
                                <span className="text-lg font-bold text-indigo-600">₹{total.toFixed(2)}</span>
                            </div>
                        </div>
                    </div>

                    {/* Footer / Notes */}
                    <div className="mt-12 pt-8 border-t border-gray-200">
                        <div className="group relative">
                            {isEditingNote ? (
                                <textarea
                                    className="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                    rows={3}
                                    value={editableNote}
                                    onChange={(e) => setEditableNote(e.target.value)}
                                    onBlur={() => setIsEditingNote(false)}
                                    autoFocus
                                />
                            ) : (
                                <div
                                    className="text-gray-600 text-sm cursor-text hover:bg-gray-50 p-2 rounded relative"
                                    onClick={() => setIsEditingNote(true)}
                                >
                                    {editableNote}
                                    <Edit2 className="h-4 w-4 absolute top-2 right-2 text-gray-400 opacity-0 group-hover:opacity-100 print:hidden" />
                                </div>
                            )}
                        </div>
                        <div className="mt-8 text-center text-xs text-gray-500">
                            <p>This is a computer generated document.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
