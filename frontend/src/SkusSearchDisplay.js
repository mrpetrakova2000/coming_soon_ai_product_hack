import React, { useState, useRef, useEffect  } from 'react';

const SkusSearchDisplay = ({ data, onSelect, mode="sku" }) => {
    const [selectedSKU, setSelectedSKU] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [isDropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    const fillText = (mode == "sku") ? "продуктов" : "категорий";

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
        setDropdownOpen(true); // Открываем dropdown при вводе
    };

    const handleSelectSKU = (sku) => {
        setSelectedSKU(sku);
        setSearchTerm(sku);
        onSelect(sku);
        setDropdownOpen(false); // Закрываем dropdown после выбора
    };

    // Извлекаем значения из объекта skus и фильтруем их
    const filteredSKUs = Object.values(data).filter((sku) =>
        sku.toLowerCase().startsWith(searchTerm.toLowerCase())
    );

    const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
            setDropdownOpen(false); // Закрываем dropdown при клике вне его
        }
    };

    useEffect(() => {
        // Добавляем обработчик клика вне dropdown
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    return (
        <div className="dropdown" ref={dropdownRef}>
            <input
                type="text"
                placeholder="Введите название"
                value={searchTerm}
                onChange={handleSearch}
                onFocus={() => setDropdownOpen(true)} // Открываем dropdown при фокусе на input
            />
            {isDropdownOpen &&
                (<ul className="dropdown-list">
                    {filteredSKUs.map((sku, index) => (
                        <li
                            key={index}
                            className={`dropdown-item ${selectedSKU === sku ? 'selected' : ''}`}
                            onClick={() => handleSelectSKU(sku)}
                        >
                            {sku}
                        </li>
                    ))}
                </ul>)}
            <h4>{"Всего " + fillText + ": " + data.length}</h4>
        </div>
    );
};

export default SkusSearchDisplay;