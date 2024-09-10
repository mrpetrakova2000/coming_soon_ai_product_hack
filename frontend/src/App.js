import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';


function App() {
  const [files, setFiles] = useState([]);
  const [predictionPeriod, setPredictionPeriod] = useState('1'); // По умолчанию 1 день
  const [drag, setDrag] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(false);
  const [message, setMessage] = useState("");
  const [plots, setPlots] = useState(null);
  const [loaded, setLoaded] = useState(false);
  const [activeTab, setActiveTab] = useState(0); // Состояние для активной вкладки

  const tabs = {
    0: 'Прогноз',
    1: 'Аналитика',
    2: 'Кластеризация'
  };

  const handleFileChange = (event) => {
    event.preventDefault();
    let files = [...event.dataTransfer.files];
    console.log(files);

    const csvFiles = files.filter(file => file.name.endsWith('.csv'));

    if (csvFiles.length !== files.length) {
      setError(true);
      setMessage("Пожалуйста, загрузите только файлы с расширением .csv");
    }
    else {
      setFiles(files);
    }
    setDrag(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    files.forEach((file) => {
      console.log(file);
      formData.append('files', file);
    });
    console.log(predictionPeriod)
    formData.append('prediction_period', Number(predictionPeriod)); // Добавляем выбранный период предсказания

    try {
      setIsLoading(true)
      const response = await axios.post("http://localhost:8000/prediction/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setError(false);
      setMessage(response.data.message);
      setPlots(response.data.plots);
      console.log(response);
      console.log(response.data);
      console.log(response.data.message);
      console.log(response.data.plots);
    } catch (error) {
      console.error("Ошибка загрузки файла:", error);
      setError(true);
      setMessage("Ошибка загрузки файла");
    } finally {
      setIsLoading(false);
      setLoaded(true);
    }
  };

  function dragStartHandler(event) {
    event.preventDefault();
    setDrag(true);
  }

  function dragLeaveHandler(event) {
    event.preventDefault();
    setDrag(false);
  }

  const removeFile = (index) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };


  return (
    <div className="App">
      <h1>Napoleon Plan - ваш помощник в бизнесе</h1>
      <div className='form-container'>
        <div className="tabs">
          {Object.keys(tabs).map((tab) => (
            <div
              key={tab}
              className={`tab ${activeTab === Number(tab) ? 'active' : ''}`}
              onClick={() => handleTabChange(Number(tab))}
            >
              {tabs[tab]}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit}>
          <div className='drop-area'>
            {drag
              ? <div className='files-down'
                onDragStart={e => dragStartHandler(e)}
                onDragLeave={e => dragLeaveHandler(e)}
                onDragOver={e => dragStartHandler(e)}
                onDrop={e => handleFileChange(e)}
              > <p>Отпустите CSV файлы, чтобы загрузить </p></div>
              : <div className='files-up'
                onDragStart={e => dragStartHandler(e)}
                onDragLeave={e => dragLeaveHandler(e)}
                onDragOver={e => dragStartHandler(e)}
              > <p>Переместите CSV файлы, чтобы загрузить </p></div>
            }
          </div>

          {files.length > 0 && (<div>
            <h3>Выбранные файлы:</h3>
            <ul className='files-list'>
              {files.map((file, index) => (
                <li key={index}>{file.name} <button className="remove-file" type="button" onClick={() => removeFile(index)}>Удалить файл</button></li>
              ))}
            </ul>
          </div>)}

          {files.length > 0 && activeTab == 0 &&
            (<h3>Выберите период предсказания:</h3>)}
          {files.length > 0 && activeTab == 0 &&
            (<select className='predict-period'
              id="predictionPeriod"
              value={predictionPeriod}
              onChange={(e) => setPredictionPeriod(e.target.value)}
            >
              <option value="1">1 день</option>
              <option value="7">1 неделя</option>
              <option value="30">1 месяц</option>
            </select>)}

          {files.length > 0 && predictionPeriod && (<button className="upload-button" type="submit">Upload files</button>)}
        </form>
      </div>

      {isLoading && <p>Загрузка ...</p>}
      
      {message && <p>{message}</p>}
      {!error && loaded && plots && console.log(plots)}
      {!error && !isLoading && loaded &&
        plots.map((plot, index) => (
          <Plot
            key={index}
            data={plot.data}
            layout={plot.layout}
          />))
      }
    </div>
  );
}

export default App;