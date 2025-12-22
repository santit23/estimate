import React, { useState, useEffect } from 'react';
import { ratesApi, MaterialRate, RateStructure, MaterialDef } from '../app/api/ratesApi';
import { Save, RefreshCw, Plus, Grid, List, X, Settings as SettingsIcon, Trash2, Link, AlertCircle } from 'lucide-react';

export default function PriceManager() {
    const [structure, setStructure] = useState<RateStructure | null>(null);
    const [rates, setRates] = useState<MaterialRate[]>([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    // UI State
    const [activeTab, setActiveTab] = useState<'profiles' | 'hardware'>('profiles');
    const [showAddAttribute, setShowAddAttribute] = useState(false);
    const [showAddMaterialModal, setShowAddMaterialModal] = useState(false);

    // Filters
    const [series, setSeries] = useState<string>('');
    const [quality, setQuality] = useState<string>('');

    // Custom Attributes
    const [customSeries, setCustomSeries] = useState('');
    const [customQuality, setCustomQuality] = useState('');
    const [customColor, setCustomColor] = useState('');

    // Add Material State
    const [newItemName, setNewItemName] = useState('');
    const [newItemUnit, setNewItemUnit] = useState('nos');
    const [newItemCategory, setNewItemCategory] = useState<'profile' | 'hardware'>('profile');

    useEffect(() => {
        init();
    }, []);

    const init = async () => {
        setLoading(true);
        try {
            const struct = await ratesApi.getStructure();
            setStructure(struct);
            if (struct.series.length > 0 && !series) setSeries(struct.series[0]);
            if (struct.qualities.length > 0 && !quality) setQuality(struct.qualities[0]);

            // Load ALL rates at once so we can edit across series without losing state
            const allRates = await ratesApi.getRates();
            setRates(allRates);
        } catch (error) {
            console.error("Error loading data:", error);
        } finally {
            setLoading(false);
        }
    };

    // No useEffect on [series] anymore! We filter locally.

    const handleSave = async () => {
        if (!structure) return;
        setSaving(true);
        try {
            await ratesApi.bulkUpdate(rates);
            alert("All changes saved successfully!");
            // Reload to sync state (IDs etc)
            const allRates = await ratesApi.getRates();
            setRates(allRates);
        } catch (error) {
            alert("Error saving rates: " + error);
        } finally {
            setSaving(false);
        }
    };

    const handleRateUpdate = (updatedRate: MaterialRate) => {
        // Check if global hardware update is needed
        const isHardware = updatedRate.category === 'hardware' || structure?.materials.find(m => m.name === updatedRate.material_name)?.category === 'hardware';

        if (isHardware && structure) {
            // Update this rate for ALL series in local state
            // We iterate through all known series in structure
            const newRates = [...rates];

            structure.series.forEach(s => {
                // Find existing entry for this series/material
                // Hardware is usually Quality=Manual?, Color=Mill? -> Whatever is passed in updatedRate
                // But we want to replicate the PRICE (Rate) to all series entries for this material

                const matchIdx = newRates.findIndex(r =>
                    r.series === s &&
                    r.material_name === updatedRate.material_name
                    // For hardware, we might ignore quality/color or assume they match the updatedRate's Q/C
                    // Usually hardware has one global entry per series.
                );

                if (matchIdx >= 0) {
                    newRates[matchIdx] = {
                        ...newRates[matchIdx],
                        rate: updatedRate.rate
                    };
                } else {
                    // Create new entry if it doesn't exist for this series
                    newRates.push({
                        ...updatedRate,
                        series: s,
                        id: undefined // New entry
                    });
                }
            });
            setRates(newRates);

        } else {
            // Normal update (Profile) - Specific to Series/Quality/Color
            const idx = rates.findIndex(r =>
                (updatedRate.id && r.id === updatedRate.id) ||
                (r.series === updatedRate.series && r.quality === updatedRate.quality && r.color === updatedRate.color && r.material_name === updatedRate.material_name)
            );

            if (idx >= 0) {
                const newRates = [...rates];
                newRates[idx] = updatedRate;
                setRates(newRates);
            } else {
                setRates([...rates, updatedRate]);
            }
        }
    };

    const handleAddMaterial = () => {
        if (!structure || !newItemName) return;
        const newMat: MaterialDef = {
            name: newItemName,
            category: newItemCategory,
            default_unit: newItemUnit
        };
        setStructure({
            ...structure,
            materials: [...structure.materials, newMat]
        });
        setShowAddMaterialModal(false);
        setNewItemName('');
    };

    // ... (handleDeleteMaterial and handleDeleteRow logic remains similar but acts on local state)
    const handleDeleteMaterial = async (name: string) => {
        if (!structure) return;
        const isProfile = structure.materials.find(m => m.name === name)?.category === 'profile';
        const msg = isProfile ?
            `Delete profile "${name}"? This removes it from THIS series.` :
            `Delete hardware "${name}"? This removes it from ALL series.`;

        if (!confirm(msg)) return;

        try {
            await ratesApi.deleteMaterial(name, isProfile ? series : undefined);
            const newMats = structure.materials.filter(m => m.name !== name);
            setStructure({ ...structure, materials: newMats });
            const newRates = rates.filter(r => r.material_name !== name);
            setRates(newRates);
        } catch (error) {
            console.error("Error deleting material:", error);
            alert("Failed to delete material.");
        }
    };

    const handleDeleteRow = async (scopeColor: string) => {
        if (!confirm(`Delete all rates for color "${scopeColor}" in this Series/Quality?`)) return;
        try {
            await ratesApi.deleteScope({ series, quality, color: scopeColor });
            if (structure) {
                const nextColors = structure.colors.filter(c => c !== scopeColor);
                setStructure({ ...structure, colors: nextColors });
            }
            if (scopeColor === customColor) setCustomColor('');
            const newRates = rates.filter(r => !(r.series === series && r.quality === quality && r.color === scopeColor));
            setRates(newRates);
        } catch (error) {
            console.error("Error deleting row:", error);
            alert("Failed to delete row.");
        }
    };

    const handleUnitChange = (matName: string, newUnit: string) => {
        if (!structure) return;
        const newMats = structure.materials.map(m => m.name === matName ? { ...m, default_unit: newUnit } : m);
        setStructure({ ...structure, materials: newMats });
        // Update unit for all rates of this material
        const newRates = rates.map(r => r.material_name === matName ? { ...r, unit: newUnit } : r);
        setRates(newRates);
    };

    if (!structure) return <div className="p-8 text-center text-gray-700">Loading configuration...</div>;

    const availableSeries = structure.series.includes(customSeries) || !customSeries ? structure.series : [...structure.series, customSeries];
    const availableQualities = structure.qualities.includes(customQuality) || !customQuality ? structure.qualities : [...structure.qualities, customQuality];
    const availableColors = structure.colors.includes(customColor) || !customColor ? structure.colors : [...structure.colors, customColor];

    return (
        <div className="space-y-6 h-full flex flex-col text-gray-900">
            {/* Header controls */}
            <div className="bg-white p-4 rounded-lg shadow border border-gray-200 flex flex-col gap-4 flex-shrink-0">
                <div className="flex flex-wrap gap-4 items-end">

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Series</label>
                        <select
                            value={activeTab === 'hardware' ? 'all' : series}
                            onChange={(e) => setSeries(e.target.value)}
                            disabled={activeTab === 'hardware'}
                            className={`mt-1 block w-32 rounded-md border-gray-300 shadow-sm border p-2 text-sm text-black focus:ring-indigo-500 focus:border-indigo-500 
                                ${activeTab === 'hardware' ? 'bg-gray-100 text-gray-500' : ''}`}
                        >
                            {activeTab === 'hardware' ? <option value="all">All Series</option> : availableSeries.map(s => <option key={s} value={s}>{s}</option>)}
                        </select>
                    </div>

                    {activeTab === 'profiles' && (
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Quality</label>
                            <select
                                value={quality}
                                onChange={(e) => setQuality(e.target.value)}
                                className="mt-1 block w-32 rounded-md border-gray-300 shadow-sm border p-2 text-sm text-black focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                {availableQualities.map(q => <option key={q} value={q}>{q}</option>)}
                            </select>
                        </div>
                    )}

                    <div className="flex-grow">
                        <div className="flex space-x-2 bg-gray-100 p-1 rounded-md w-fit">
                            <button
                                onClick={() => setActiveTab('profiles')}
                                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${activeTab === 'profiles' ? 'bg-white shadow text-indigo-600' : 'text-gray-600 hover:text-gray-900'}`}
                            >
                                <Grid className="w-4 h-4 inline mr-1" /> Profiles
                            </button>
                            <button
                                onClick={() => setActiveTab('hardware')}
                                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${activeTab === 'hardware' ? 'bg-white shadow text-indigo-600' : 'text-gray-600 hover:text-gray-900'}`}
                            >
                                <List className="w-4 h-4 inline mr-1" /> Hardware (Global)
                            </button>
                        </div>
                    </div>

                    <div className="flex gap-2">
                        <button
                            onClick={() => setShowAddAttribute(!showAddAttribute)}
                            className="flex items-center px-3 py-2 border border-blue-300 rounded-md shadow-sm text-sm font-medium text-blue-700 bg-blue-50 hover:bg-blue-100"
                        >
                            <SettingsIcon className="h-4 w-4 mr-2" />
                            Add Type
                        </button>

                        <button
                            onClick={() => {
                                setNewItemCategory(activeTab === 'hardware' ? 'hardware' : 'profile');
                                setShowAddMaterialModal(true);
                            }}
                            className="flex items-center px-3 py-2 border border-blue-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-blue-50"
                        >
                            <Plus className="h-4 w-4 mr-2" />
                            Add Material
                        </button>

                        <button
                            onClick={handleSave}
                            disabled={saving}
                            className={`flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${saving ? 'bg-gray-400' : 'bg-green-600 hover:bg-green-700'}`}
                        >
                            {saving ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <Save className="h-4 w-4 mr-2" />}
                            Save All
                        </button>
                    </div>
                </div>

                {showAddAttribute && (
                    <div className="p-4 bg-blue-50 rounded border border-blue-100 grid grid-cols-4 gap-4 relative">
                        <button onClick={() => setShowAddAttribute(false)} className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"><X className="h-4 w-4" /></button>
                        <div className="col-span-4 text-xs font-semibold text-blue-800 uppercase tracking-wide">Define New Types</div>

                        <div><input placeholder="New Series Name" className="border p-2 rounded text-sm w-full text-black" value={customSeries} onChange={e => setCustomSeries(e.target.value)} /></div>
                        <div><input placeholder="New Quality Name" className="border p-2 rounded text-sm w-full text-black" value={customQuality} onChange={e => setCustomQuality(e.target.value)} /></div>
                        <div><input placeholder="New Color Name" className="border p-2 rounded text-sm w-full text-black" value={customColor} onChange={e => setCustomColor(e.target.value)} /></div>
                        <div className="flex items-center"><span className="text-xs text-blue-600 italic">Types appear in dropdowns immediately. Save a rate to persist.</span></div>
                    </div>
                )}
            </div>

            <div className="flex-grow min-h-0 bg-white shadow rounded-lg border border-gray-200 overflow-hidden relative">
                {loading ? (
                    <div className="absolute inset-0 flex items-center justify-center bg-gray-50 bg-opacity-75 z-50">
                        <div className="text-gray-900 font-medium">Loading All Rates...</div>
                    </div>
                ) : null}

                <div className="h-full overflow-auto">
                    {activeTab === 'profiles' ? (
                        // Pass ONLY the rates relevant to current view for rendering, but update handler deals with global state
                        <ProfileMatrix
                            structure={structure}
                            rates={rates}
                            series={series}
                            quality={quality}
                            availableColors={availableColors}
                            onUpdate={handleRateUpdate}
                            onUnitChange={handleUnitChange}
                            onDeleteColumn={handleDeleteMaterial}
                            onDeleteRow={handleDeleteRow}
                        />
                    ) : (
                        <HardwareList
                            structure={structure}
                            rates={rates}
                            // Use the first series for display logic if needed, but updates are global
                            series={structure.series[0]}
                            onUpdate={handleRateUpdate}
                            onUnitChange={handleUnitChange}
                            onDelete={handleDeleteMaterial}
                        />
                    )}
                </div>
            </div>

            {showAddMaterialModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
                    <div className="bg-white rounded-lg p-6 w-96 shadow-xl text-black">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-lg font-medium text-black">Add New {newItemCategory === 'profile' ? 'Profile' : 'Hardware'}</h3>
                            <button onClick={() => setShowAddMaterialModal(false)}><X className="w-5 h-5 text-gray-400" /></button>
                        </div>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Name</label>
                                <input className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-black" value={newItemName} onChange={e => setNewItemName(e.target.value)} placeholder="e.g. New Track" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Unit</label>
                                <input className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-black" value={newItemUnit} onChange={e => setNewItemUnit(e.target.value)} placeholder="e.g. nos, kg, ft" />
                            </div>
                            <button onClick={handleAddMaterial} className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700">Add {newItemCategory}</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

// Sub-components unchanged in logic/UI, but receiving FULL rates array and filtering locally.
// ProfileMatrix needs to filter 'rates' to show only current series/quality.
// (Actually it finds rate by find(), so it works fine with full array).

function ProfileMatrix({ structure, rates, series, quality, availableColors, onUpdate, onUnitChange, onDeleteColumn, onDeleteRow }: any) {
    const sortOrder = [
        'topfr', 'bottomfr', 'botmfr', 'sidefr',
        'topsht', 'bottomsht', 'botmsht', 'sidesht',
        'interlocksht', 'intsht',
        'jali', 'jali_track', '11b', '13d', '13', '18', 'clip'
    ];

    const materials = structure.materials
        .filter((m: MaterialDef) => (m.category || 'other').toLowerCase() === 'profile')
        .sort((a: MaterialDef, b: MaterialDef) => {
            const idxA = sortOrder.indexOf(a.name.toLowerCase());
            const idxB = sortOrder.indexOf(b.name.toLowerCase());
            if (idxA !== -1 && idxB !== -1) return idxA - idxB;
            if (idxA !== -1) return -1;
            if (idxB !== -1) return 1;
            return a.name.localeCompare(b.name);
        });

    return (
        <table className="min-w-full divide-y divide-gray-200 border-collapse">
            <thead className="bg-gray-50 sticky top-0 z-10 shadow-sm">
                <tr>
                    <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-20 border-b border-r border-gray-200 w-[120px]">
                        Color ({quality})
                    </th>
                    {materials.map((mat: MaterialDef) => (
                        <th key={mat.name} className="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200 min-w-[100px] border-r group relative">
                            <div className="truncate font-semibold text-gray-900" title={mat.name}>{mat.name}</div>
                            <div className="flex items-center justify-center mt-1">
                                <input value={mat.default_unit} onChange={(e) => onUnitChange(mat.name, e.target.value)} className="bg-transparent border-b border-gray-300 text-center w-12 text-[10px] focus:outline-none focus:border-indigo-500 text-gray-600 font-normal" placeholder="unit" />
                            </div>
                            <button onClick={() => onDeleteColumn(mat.name)} className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-600 rounded">
                                <Trash2 className="w-3 h-3" />
                            </button>
                        </th>
                    ))}
                </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
                {availableColors.map((c: string) => (
                    <tr key={c} className="hover:bg-gray-50 group/row">
                        <td className="px-3 py-2 text-sm font-medium text-gray-900 sticky left-0 bg-white z-10 border-r border-gray-200 align-middle relative group/cell">
                            {c}
                            <button onClick={() => onDeleteRow(c)} className="absolute right-1 top-1/2 -translate-y-1/2 opacity-0 group-hover/row:opacity-100 p-1 text-gray-400 hover:text-red-600 rounded">
                                <Trash2 className="w-3 h-3" />
                            </button>
                        </td>
                        {materials.map((mat: MaterialDef) => {
                            const rateObj = rates.find((r: MaterialRate) =>
                                r.series === series &&
                                r.quality === quality &&
                                r.color === c &&
                                r.material_name === mat.name
                            );
                            const val = rateObj ? rateObj.rate : 0;
                            return (
                                <td key={mat.name} className="p-0 border-r border-gray-100">
                                    <input
                                        type="number"
                                        value={val === 0 ? '' : val}
                                        placeholder="-"
                                        className="block w-full text-right h-full py-2 px-2 border-transparent focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 sm:text-xs bg-transparent text-gray-900"
                                        onChange={(e) => {
                                            const newVal = parseFloat(e.target.value) || 0;
                                            onUpdate({
                                                id: rateObj?.id,
                                                series,
                                                quality: quality,
                                                color: c,
                                                material_name: mat.name,
                                                rate: newVal,
                                                category: 'profile',
                                                unit: mat.default_unit
                                            });
                                        }}
                                    />
                                </td>
                            );
                        })}
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

function HardwareList({ structure, rates, series, onUpdate, onUnitChange, onDelete }: any) {
    const materials = structure.materials
        .filter((m: MaterialDef) => (m.category || 'other').toLowerCase() !== 'profile')
        .sort((a: MaterialDef, b: MaterialDef) => a.name.localeCompare(b.name));

    const defaultQuality = structure.qualities[0] || 'manual';
    const defaultColor = structure.colors[0] || 'mill';

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">
                <div className="flex items-center">
                    <div className="flex-shrink-0"><List className="h-5 w-5 text-blue-400" /></div>
                    <div className="ml-3">
                        <p className="text-sm text-blue-700">
                            <b>Global Hardware Rates</b>: Changes here will apply to <b>ALL Series</b> upon saving.
                        </p>
                    </div>
                </div>
            </div>

            <table className="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg overflow-hidden">
                <thead className="bg-gray-50">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/2">Item Name</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unit</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price (Rate)</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                    </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                    {materials.map((mat: MaterialDef, idx: number) => {
                        // Find match in current displayed series (which is essentially random/first series to show values)
                        // But since we sync hardware, any series value is fine.
                        const rateObj = rates.find((r: MaterialRate) => r.series === series && r.material_name === mat.name);
                        const val = rateObj ? rateObj.rate : 0;
                        return (
                            <tr key={mat.name} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{mat.name}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    <input value={mat.default_unit} onChange={(e) => onUnitChange(mat.name, e.target.value)} className="w-20 border-b border-gray-300 bg-transparent focus:outline-none focus:border-indigo-500 text-center text-gray-900" />
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    <div className="relative rounded-md shadow-sm max-w-[200px]">
                                        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"><span className="text-gray-500 sm:text-sm">₹</span></div>
                                        <input type="number" value={val === 0 ? '' : val} onChange={(e) => {
                                            const newVal = parseFloat(e.target.value) || 0;
                                            onUpdate({
                                                id: rateObj?.id,
                                                series,
                                                quality: defaultQuality,
                                                color: defaultColor,
                                                material_name: mat.name,
                                                rate: newVal,
                                                category: 'hardware',
                                                unit: mat.default_unit
                                            });
                                        }} className="block w-full rounded-md border-gray-300 pl-7 pr-4 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2 text-gray-900" placeholder="0.00" />
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    <button onClick={() => onDelete(mat.name)} className="text-gray-400 hover:text-red-600 transition-colors p-1"><Trash2 className="w-4 h-4" /></button>
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}
