import React from 'react';

const ParametersDisplay = ({ data }) => {
  return (
    <div className='report-container'>
      {data.map((item, index) => {
        const [title, values] = Object.entries(item)[0]; 
        return (
          <div key={index} className='report-theme-container'>
            <h3 className="title">{title}</h3>
            {Object.entries(values).map(([key, value]) => (
              <div key={key} className="data-row">
                <span className="key">{key}</span>
                <span className="dots"></span> {/* Псевдоэлемент для точек */}
                <span className="value">{value.toString()}</span>
              </div>
            ))}
          </div>
        );
      })}
    </div>
  );
};

export default ParametersDisplay;