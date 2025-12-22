"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '../../api/axios';
import { Plus, Trash2, Save, FileText } from 'lucide-react';
import Header from '../../../components/Header';
import FormulaViewer from '../../../components/FormulaViewer';

interface EstimateItem {
    design: string;
    series: string;
    quality: string;
    color: string;
    width: number;
    height: number;
    quantity: number;
    is_active: boolean;
}

export default function NewEstimatePage() {
    const router = useRouter();
    const [customerName, setCustomerName] = useState('');
    const [customerPhone, setCustomerPhone] = useState('');
    const [items, setItems] = useState<EstimateItem[]>([]);
    const [showFormulas, setShowFormulas] = useState(false);

    // Project Settings State
    const [transportCost, setTransportCost] = useState(0);
    const [profitMargin, setProfitMargin] = useState(25); // Default 25%
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

    // Current Item State
    const [currentItem, setCurrentItem] = useState<EstimateItem>({
        design: '2panel',
        series: '90mm',
        quality: 'mount',
        color: 'mill',
        width: 0,
        height: 0,
        quantity: 1,
        is_active: true
    });

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
                    // Ensure current item color is valid or set to first available
                    if (!response.data.colors.includes(currentItem.color)) {
                        setCurrentItem(prev => ({ ...prev, color: response.data.colors[0] }));
                    }
                }
            } catch (error) {
                console.error('Failed to fetch rate structure', error);
            }
        };

        fetchStructure();
    }, []);

    const handleAddItem = () => {
        if (currentItem.width > 0 && currentItem.height > 0) {
            setItems([...items, currentItem]);
            // Reset dimensions but keep other selections
            setCurrentItem({ ...currentItem, width: 0, height: 0, quantity: 1, is_active: true });
        }
    };

    const handleRemoveItem = (index: number) => {
        setItems(items.filter((_, i) => i !== index));
    };

    const handleSubmit = async () => {
        if (!customerName || items.length === 0) return;

        try {
            await api.post('/estimates/', {
                customer_name: customerName,
                customer_phone: customerPhone,
                items: items,
                transport_cost: transportCost,
                profit_margin: profitMargin,
                labour_rate: labourRate,
                glass_rate: glassRate
            });
            router.push('/dashboard');
        } catch (error) {
            console.error('Failed to create estimate', error);
            alert('Failed to create estimate');
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <Header />
            <div className="py-8 px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl mx-auto">
                    <h1 className="text-3xl font-bold text-gray-900 mb-8">Create New Estimate</h1>

                    {/* Customer Details */}
                    <div className="bg-white shadow sm:rounded-lg p-6 mb-6">
                        <h2 className="text-xl font-semibold mb-4 text-gray-900">Customer Details</h2>
                        <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Customer Name</label>
                                <input
                                    type="text"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                    value={customerName}
                                    onChange={(e) => setCustomerName(e.target.value)}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Phone Number</label>
                                <input
                                    type="text"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                    value={customerPhone}
                                    onChange={(e) => setCustomerPhone(e.target.value)}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Project Settings */}
                    <div className="bg-white shadow sm:rounded-lg p-6 mb-6">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-semibold text-gray-900">Project Settings (Optional)</h2>
                        </div>
                        <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Transport Cost (₹)</label>
                                <input
                                    type="number"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 sm:text-sm"
                                    value={transportCost}
                                    onChange={(e) => setTransportCost(parseFloat(e.target.value) || 0)}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Profit Margin (%)</label>
                                <input
                                    type="number"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 sm:text-sm"
                                    value={profitMargin}
                                    onChange={(e) => setProfitMargin(parseFloat(e.target.value) || 0)}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Labour Override (₹/sqft)</label>
                                <input
                                    type="number"
                                    placeholder="Default"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 sm:text-sm"
                                    value={labourRate}
                                    onChange={(e) => setLabourRate(parseFloat(e.target.value) || 0)}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Glass Override (₹/sqft)</label>
                                <input
                                    type="number"
                                    placeholder="Default"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 sm:text-sm"
                                    value={glassRate}
                                    onChange={(e) => setGlassRate(parseFloat(e.target.value) || 0)}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Add Item Form */}
                    <div className="bg-white shadow sm:rounded-lg p-6 mb-6">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-xl font-semibold text-gray-900">Add Item</h2>
                            <button
                                onClick={() => setShowFormulas(true)}
                                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                            >
                                <FileText className="h-4 w-4 mr-2" />
                                View Formulas
                            </button>
                        </div>
                        <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-3">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Design</label>
                                <select
                                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                                    value={currentItem.design}
                                    onChange={(e) => setCurrentItem({ ...currentItem, design: e.target.value })}
                                >
                                    {availableDesigns.map(d => (
                                        <option key={d} value={d}>
                                            {d.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Series</label>
                                <select
                                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                                    value={currentItem.series}
                                    onChange={(e) => setCurrentItem({ ...currentItem, series: e.target.value })}
                                >
                                    {availableSeries.map(s => (
                                        <option key={s} value={s}>{s}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Quality</label>
                                <select
                                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                                    value={currentItem.quality}
                                    onChange={(e) => setCurrentItem({ ...currentItem, quality: e.target.value })}
                                >
                                    {availableQualities.map(q => (
                                        <option key={q} value={q}>
                                            {q.charAt(0).toUpperCase() + q.slice(1)}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Color</label>
                                <select
                                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                                    value={currentItem.color}
                                    onChange={(e) => setCurrentItem({ ...currentItem, color: e.target.value })}
                                >
                                    {availableColors.map(c => (
                                        <option key={c} value={c}>
                                            {c.charAt(0).toUpperCase() + c.slice(1)}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Width (ft)</label>
                                <input
                                    type="number"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                    value={currentItem.width}
                                    onChange={(e) => setCurrentItem({ ...currentItem, width: parseFloat(e.target.value) || 0 })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Height (ft)</label>
                                <input
                                    type="number"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                    value={currentItem.height}
                                    onChange={(e) => setCurrentItem({ ...currentItem, height: parseFloat(e.target.value) || 0 })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Quantity</label>
                                <input
                                    type="number"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                    value={currentItem.quantity}
                                    onChange={(e) => setCurrentItem({ ...currentItem, quantity: parseInt(e.target.value) || 1 })}
                                />
                            </div>
                        </div>
                        <div className="mt-4">
                            <button
                                onClick={handleAddItem}
                                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                            >
                                <Plus className="h-5 w-5 mr-2" />
                                Add Item
                            </button>
                        </div>
                    </div>

                    {/* Items List */}
                    {items.length > 0 && (
                        <div className="bg-white shadow sm:rounded-lg overflow-hidden mb-6">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Include</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Design</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Series</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Qty</th>
                                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {items.map((item, index) => (
                                        <tr key={index} className={!item.is_active ? 'bg-gray-50 opacity-50' : ''}>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <input
                                                    type="checkbox"
                                                    checked={item.is_active}
                                                    onChange={(e) => {
                                                        const newItems = [...items];
                                                        newItems[index].is_active = e.target.checked;
                                                        setItems(newItems);
                                                    }}
                                                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                                                />
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{item.design}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.series} - {item.quality} - {item.color}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.width} x {item.height}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.quantity}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                                <button onClick={() => handleRemoveItem(index)} className="text-red-600 hover:text-red-900">
                                                    <Trash2 className="h-5 w-5" />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}

                    {/* Submit Button */}
                    <div className="flex justify-end">
                        <button
                            onClick={handleSubmit}
                            disabled={items.length === 0 || !customerName}
                            className={`inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white ${items.length > 0 && customerName ? 'bg-green-600 hover:bg-green-700' : 'bg-gray-400 cursor-not-allowed'
                                }`}
                        >
                            <Save className="h-5 w-5 mr-2" />
                            Generate Estimate
                        </button>
                    </div>

                    {/* Formula Viewer Modal */}
                    {showFormulas && (
                        <FormulaViewer
                            productType="window"
                            designType={currentItem.design}
                            onClose={() => setShowFormulas(false)}
                        />
                    )}
                </div>
            </div>
        </div>

    );
}
