"use client";

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import api from '../../api/axios';
import Link from 'next/link';
import { ArrowLeft, Edit2, Save, X, Trash2, Printer } from 'lucide-react';
import EstimatePreview from '../../../components/EstimatePreview';

interface EstimateItem {
    id: number;
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
    customer_phone: string | null;
    created_at: string;
    total_amount: number;
    total_area: number;
    transport_cost?: number;
    profit_margin?: number;
    items: EstimateItem[];
}

interface EditableItem {
    design: string;
    series: string;
    quality: string;
    color: string;
    width: number;
    height: number;
    quantity: number;
}

export default function EstimateDetailPage() {
    const [estimate, setEstimate] = useState<Estimate | null>(null);
    const [isEditing, setIsEditing] = useState(false);
    const [showPreview, setShowPreview] = useState(false);
    const [editedCustomerName, setEditedCustomerName] = useState('');
    const [editedCustomerPhone, setEditedCustomerPhone] = useState('');
    const [editedItems, setEditedItems] = useState<EditableItem[]>([]);

    // Project Settings State
    const [transportCost, setTransportCost] = useState(0);
    const [profitMargin, setProfitMargin] = useState(0);
    const [labourRate, setLabourRate] = useState(0);
    const [glassRate, setGlassRate] = useState(0);

    // Dynamic Data State
    const [availableSeries, setAvailableSeries] = useState<string[]>(['90mm', '78mm']);
    const [availableQualities, setAvailableQualities] = useState<string[]>(['mount', 'rohit']);
    const [availableDesigns, setAvailableDesigns] = useState<string[]>([
        '2panel', '3panel', '4panel', '2panel_topfix', '3panel_topfix', '4panel_topfix'
    ]);
    const [availableColors, setAvailableColors] = useState<string[]>([
        'mill', 'black', 'wood', 'champagne', 'grey', 'white'
    ]);

    const router = useRouter();
    const params = useParams();
    const id = params.id;

    useEffect(() => {
        const fetchStructure = async () => {
            try {
                const response = await api.get('/rates/structure');
                if (response.data.series && response.data.series.length > 0) {
                    setAvailableSeries(response.data.series);
                }
                if (response.data.qualities && response.data.qualities.length > 0) {
                    setAvailableQualities(response.data.qualities);
                }
                if (response.data.colors && response.data.colors.length > 0) {
                    setAvailableColors(response.data.colors);
                }
            } catch (error) {
                console.error('Failed to fetch rate structure', error);
            }
        };

        const fetchEstimate = async () => {
            try {
                const response = await api.get(`/estimates/${id}`);
                setEstimate(response.data);
                setEditedCustomerName(response.data.customer_name);
                setEditedCustomerPhone(response.data.customer_phone || '');
                setTransportCost(response.data.transport_cost || 0);
                setProfitMargin(response.data.profit_margin || 0);
                // Note: overrides are not currently stored in DB separate fields, 
                // engine merges them into items. 
                // We'll initialize overrides to 0 for edit mode as they are "action" parameters.
                setLabourRate(0);
                setGlassRate(0);

                setEditedItems(response.data.items.map((item: EstimateItem) => ({
                    design: item.design,
                    series: item.series,
                    quality: item.quality,
                    color: item.color || 'mill', // Default to mill if missing
                    width: item.width,
                    height: item.height,
                    quantity: item.quantity,
                })));
            } catch (error) {
                console.error('Failed to fetch estimate', error);
                router.push('/dashboard');
            }
        };

        if (id) {
            fetchStructure();
            fetchEstimate();
        }
    }, [id, router]);

    const handleDeleteEstimate = async () => {
        if (confirm('Are you sure you want to delete this estimate? This action cannot be undone.')) {
            try {
                await api.delete(`/estimates/${id}`);
                router.push('/dashboard');
            } catch (error) {
                console.error('Failed to delete estimate', error);
                alert('Failed to delete estimate');
            }
        }
    };

    const handleSave = async () => {
        try {
            await api.put(`/estimates/${id}`, {
                customer_name: editedCustomerName,
                customer_phone: editedCustomerPhone || null,
                items: editedItems,
                transport_cost: transportCost,
                profit_margin: profitMargin,
                labour_rate: labourRate,
                glass_rate: glassRate
            });

            // Refresh the estimate data
            const response = await api.get(`/estimates/${id}`);
            setEstimate(response.data);
            setTransportCost(response.data.transport_cost || 0);
            setProfitMargin(response.data.profit_margin || 0);
            setLabourRate(0);
            setGlassRate(0);
            setEditedItems(response.data.items.map((item: EstimateItem) => ({
                design: item.design,
                series: item.series,
                quality: item.quality,
                color: item.color || 'mill',
                width: item.width,
                height: item.height,
                quantity: item.quantity,
            })));
            setIsEditing(false);
        } catch (error) {
            console.error('Failed to update estimate', error);
            alert('Failed to update estimate');
        }
    };

    const handleCancel = () => {
        if (estimate) {
            setEditedCustomerName(estimate.customer_name);
            setEditedCustomerPhone(estimate.customer_phone || '');
            setTransportCost(estimate.transport_cost || 0);
            setProfitMargin(estimate.profit_margin || 0);
            setLabourRate(0);
            setGlassRate(0);
            setEditedItems(estimate.items.map(item => ({
                design: item.design,
                series: item.series,
                quality: item.quality,
                color: item.color || 'mill',
                width: item.width,
                height: item.height,
                quantity: item.quantity,
            })));
        }
        setIsEditing(false);
    };

    const handleItemChange = (index: number, field: keyof EditableItem, value: string | number) => {
        const newItems = [...editedItems];
        newItems[index] = { ...newItems[index], [field]: value };
        setEditedItems(newItems);
    };

    const handleDeleteItem = (index: number) => {
        if (editedItems.length <= 1) {
            alert('Cannot delete the last item. An estimate must have at least one item.');
            return;
        }
        const newItems = editedItems.filter((_, i) => i !== index);
        setEditedItems(newItems);
    };

    if (!estimate) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-gray-500">Loading...</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto">
                <div className="mb-6 flex justify-between items-center">
                    <Link href="/dashboard" className="inline-flex items-center text-indigo-600 hover:text-indigo-700">
                        <ArrowLeft className="h-5 w-5 mr-2" />
                        Back to Dashboard
                    </Link>

                    <div className="flex space-x-2">
                        {!isEditing ? (
                            <>
                                <button
                                    onClick={() => setShowPreview(true)}
                                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                                >
                                    <Printer className="h-4 w-4 mr-2" />
                                    Print Quote
                                </button>
                                <button
                                    onClick={() => setIsEditing(true)}
                                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                                >
                                    <Edit2 className="h-4 w-4 mr-2" />
                                    Edit
                                </button>
                            </>
                        ) : (
                            <div className="flex gap-2">
                                <button
                                    onClick={handleSave}
                                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                                >
                                    <Save className="h-4 w-4 mr-2" />
                                    Save
                                </button>
                                <button
                                    onClick={handleCancel}
                                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                                >
                                    <X className="h-4 w-4 mr-2" />
                                    Cancel
                                </button>
                            </div>
                        )}
                    </div>
                </div>

                <div className="bg-white shadow sm:rounded-lg p-6 mb-6">
                    <h1 className="text-3xl font-bold text-gray-900 mb-4">Estimate Details</h1>
                    <div className="grid grid-cols-1 gap-y-4 sm:grid-cols-2">
                        <div>
                            <p className="text-sm font-medium text-gray-500">Customer Name</p>
                            {isEditing ? (
                                <input
                                    type="text"
                                    value={editedCustomerName}
                                    onChange={(e) => setEditedCustomerName(e.target.value)}
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                />
                            ) : (
                                <p className="mt-1 text-lg font-semibold text-gray-900">{estimate.customer_name}</p>
                            )}
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Phone</p>
                            {isEditing ? (
                                <input
                                    type="text"
                                    value={editedCustomerPhone}
                                    onChange={(e) => setEditedCustomerPhone(e.target.value)}
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                />
                            ) : (
                                <p className="mt-1 text-lg text-gray-900">{estimate.customer_phone || 'N/A'}</p>
                            )}
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Date</p>
                            <p className="mt-1 text-lg text-gray-900">{new Date(estimate.created_at).toLocaleDateString()}</p>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Total Area</p>
                            <p className="mt-1 text-lg text-gray-900">{estimate.total_area.toFixed(2)} sq.ft</p>
                        </div>
                    </div>
                </div>

                {/* Project Settings for Edit Mode */}
                {isEditing && (
                    <div className="bg-white shadow sm:rounded-lg p-6 mb-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-4">Project Settings</h3>
                        <div className="grid grid-cols-1 gap-y-4 sm:grid-cols-4 gap-x-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Transport Cost</label>
                                <input
                                    type="number"
                                    value={transportCost}
                                    onChange={(e) => setTransportCost(parseFloat(e.target.value) || 0)}
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Profit Margin (%)</label>
                                <input
                                    type="number"
                                    value={profitMargin}
                                    onChange={(e) => setProfitMargin(parseFloat(e.target.value) || 0)}
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Labour Rate Override (₹/sqft)</label>
                                <input
                                    type="number"
                                    value={labourRate}
                                    onChange={(e) => setLabourRate(parseFloat(e.target.value) || 0)}
                                    placeholder="Optional"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Glass Rate Override (₹/sqft)</label>
                                <input
                                    type="number"
                                    value={glassRate}
                                    onChange={(e) => setGlassRate(parseFloat(e.target.value) || 0)}
                                    placeholder="Optional"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                />
                            </div>
                        </div>
                    </div>
                )}

                <div className="bg-white shadow sm:rounded-lg overflow-hidden mb-6">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <h2 className="text-xl font-semibold text-gray-900">Items</h2>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Design</th>
                                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Series</th>
                                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quality</th>
                                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Color</th>
                                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Width (ft)</th>
                                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Height (ft)</th>
                                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Qty</th>
                                    {!isEditing && (
                                        <>
                                            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Unit Rate</th>
                                            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                                        </>
                                    )}
                                    {isEditing && (
                                        <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                                    )}
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {isEditing ? (
                                    editedItems.map((item, index) => (
                                        <tr key={index}>
                                            <td className="px-4 py-3">
                                                <select
                                                    value={item.design}
                                                    onChange={(e) => handleItemChange(index, 'design', e.target.value)}
                                                    className="block w-full border border-gray-300 rounded-md py-1 px-2 text-sm text-gray-900"
                                                >
                                                    {availableDesigns.map(d => (
                                                        <option key={d} value={d}>
                                                            {d.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                                        </option>
                                                    ))}
                                                </select>
                                            </td>
                                            <td className="px-4 py-3">
                                                <select
                                                    value={item.series}
                                                    onChange={(e) => handleItemChange(index, 'series', e.target.value)}
                                                    className="block w-full border border-gray-300 rounded-md py-1 px-2 text-sm text-gray-900"
                                                >
                                                    {availableSeries.map(s => (
                                                        <option key={s} value={s}>{s}</option>
                                                    ))}
                                                </select>
                                            </td>
                                            <td className="px-4 py-3">
                                                <select
                                                    value={item.quality}
                                                    onChange={(e) => handleItemChange(index, 'quality', e.target.value)}
                                                    className="block w-full border border-gray-300 rounded-md py-1 px-2 text-sm text-gray-900"
                                                >
                                                    {availableQualities.map(q => (
                                                        <option key={q} value={q}>
                                                            {q.charAt(0).toUpperCase() + q.slice(1)}
                                                        </option>
                                                    ))}
                                                </select>
                                            </td>
                                            <td className="px-4 py-3">
                                                <select
                                                    value={item.color}
                                                    onChange={(e) => handleItemChange(index, 'color', e.target.value)}
                                                    className="block w-full border border-gray-300 rounded-md py-1 px-2 text-sm text-gray-900"
                                                >
                                                    {availableColors.map(c => (
                                                        <option key={c} value={c}>
                                                            {c.charAt(0).toUpperCase() + c.slice(1)}
                                                        </option>
                                                    ))}
                                                </select>
                                            </td>
                                            <td className="px-4 py-3">
                                                <input
                                                    type="number"
                                                    step="0.1"
                                                    value={item.width}
                                                    onChange={(e) => handleItemChange(index, 'width', parseFloat(e.target.value) || 0)}
                                                    className="block w-20 border border-gray-300 rounded-md py-1 px-2 text-sm text-gray-900"
                                                />
                                            </td>
                                            <td className="px-4 py-3">
                                                <input
                                                    type="number"
                                                    step="0.1"
                                                    value={item.height}
                                                    onChange={(e) => handleItemChange(index, 'height', parseFloat(e.target.value) || 0)}
                                                    className="block w-20 border border-gray-300 rounded-md py-1 px-2 text-gray-900"
                                                />
                                            </td>
                                            <td className="px-4 py-3">
                                                <input
                                                    type="number"
                                                    value={item.quantity}
                                                    onChange={(e) => handleItemChange(index, 'quantity', parseInt(e.target.value) || 1)}
                                                    className="block w-16 border border-gray-300 rounded-md py-1 px-2 text-sm text-gray-900"
                                                />
                                            </td>
                                            <td className="px-4 py-3 text-right">
                                                <button
                                                    onClick={() => handleDeleteItem(index)}
                                                    className="text-red-600 hover:text-red-900"
                                                    title="Delete item"
                                                >
                                                    <Trash2 className="h-5 w-5" />
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    estimate.items.map((item) => (
                                        <tr key={item.id}>
                                            <td className="px-4 py-3 text-sm text-gray-900">{item.design}</td>
                                            <td className="px-4 py-3 text-sm text-gray-500">{item.series}</td>
                                            <td className="px-4 py-3 text-sm text-gray-500">{item.quality}</td>
                                            <td className="px-4 py-3 text-sm text-gray-500">{item.color}</td>
                                            <td className="px-4 py-3 text-sm text-gray-500">{item.width}</td>
                                            <td className="px-4 py-3 text-sm text-gray-500">{item.height}</td>
                                            <td className="px-4 py-3 text-sm text-gray-500">{item.quantity}</td>
                                            <td className="px-4 py-3 text-sm text-right text-gray-900">₹{item.unit_rate.toFixed(2)}</td>
                                            <td className="px-4 py-3 text-sm text-right font-semibold text-gray-900">₹{item.amount.toFixed(2)}</td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                            {!isEditing && (
                                <tfoot className="bg-gray-50">
                                    <tr>
                                        <td colSpan={8} className="px-4 py-3 text-sm font-bold text-gray-900 text-right">Grand Total:</td>
                                        <td className="px-4 py-3 text-sm font-bold text-right text-indigo-600">₹{estimate.total_amount.toFixed(2)}</td>
                                    </tr>
                                </tfoot>
                            )}
                        </table>
                    </div>
                </div>
            </div>
            {showPreview && estimate && (
                <EstimatePreview
                    estimate={estimate}
                    onClose={() => setShowPreview(false)}
                />
            )}
        </div>
    );
}
