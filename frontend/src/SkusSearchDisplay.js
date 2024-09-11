import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './DropdownSearch.css'; // Импортируем CSS файл для стилей

const SkusSearchDisplay = ({ skus }) => {
  const [selectedSKU, setSelectedSKU] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSelectSKU = (sku) => {
    setSelectedSKU(sku);
  };

  const filteredSKUs = skus.filter((sku) =>
    sku.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="dropdown">
      <input
        type="text"
        placeholder="Выберите продукт: "
        value={searchTerm}
        onChange={handleSearch}
      />
      <ul className="dropdown-list">
        {filteredSKUs.map((sku) => (
          <li
            key={sku}
            className={`dropdown-item ${selectedSKU === sku ? 'selected' : ''}`}
            onClick={() => handleSelectSKU(sku)}
          >
            {sku}
          </li>
        ))}
      </ul>
      {selectedSKU && <p>Выбранный продукт: {selectedSKU}</p>}
    </div>
  );
};

export default SkusSearchDisplay;