import React, { useState, useMemo } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import ParametersDisplay from './ParametersDisplay';
import SkusSearchDisplay from './SkusSearchDisplay';
import MySubplots from './MySubplots';


function App() {
  const [files, setFiles] = useState([]);
  const [predictionPeriod, setPredictionPeriod] = useState('1'); // По умолчанию 1 день
  const [drag, setDrag] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(false);
  const [message, setMessage] = useState("");
  const [plots, setPlots] = useState(null);
  const [loaded, setLoaded] = useState(false);
  const [allSkusFlag, setAllSkusFlag] = useState(false);
  const [choosedSku, setChoosedSku] = useState(null);
  const [skus, setSkus] = useState([]);
  const [choosedCluster, setChoosedCluster] = useState(null);
  const [clusters, setClusters] = useState([]);
  const [activeTab, setActiveTab] = useState(0); // Состояние для активной вкладки
  const [parameters, setParameters] = useState([])

  const tabs = {
    0: 'Прогноз по продукту',
    1: 'Прогноз по категориям',
    2: 'Аналитика'
  };

  const tabsWithSkusFlag = [0, 2];

  const apiMethod = updateApiMethod();
  const submitButtonName = getSubmitButtonName();

  // console.log(allSkusFlag);
  // console.log(skus);
  // console.log(choosedSku);

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
    formData.append('choosed_sku', String(choosedSku)); // Добавляем выбранный период предсказания
    formData.append('choosed_cluster', String(choosedCluster));

    try {
      setIsLoading(true)
      const response = await axios.post("http://localhost:8000/" + apiMethod + "/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setError(false);
      setMessage(response.data.message);
      if (response.data.plots) setPlots(response.data.plots);
      if (response.data.skus) setSkus(response.data.skus);
      if (response.data.clusters) setClusters(response.data.clusters);
      if (response.data.parameters) setParameters(response.data.parameters)
      console.log(response);
      console.log(response.data);
      console.log(response.data.message);
      console.log(response.data.plots);
    } catch (error) {
      console.error("Ошибка загрузки файла:", error);
      setError(true);
      setMessage("Ошибка");
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
    setLoaded(false);
    setChoosedSku(null);
    setAllSkusFlag(false);
    setSkus(null);
    setClusters(null);
    setChoosedCluster(null);
    setMessage(null);
    setPlots(null);
    setParameters(null);
  };

  function updateApiMethod() {
    switch (activeTab) {
      case 0:
        if (allSkusFlag === true || choosedSku != null) {
          return "prediction";
        } else {
          return "getSkus";
        }
      case 1:
        if (allSkusFlag === true || choosedCluster != null) {
          return "clustering";
        } else {
          return "getClusters";
        }
      case 2:
        if (allSkusFlag === true || choosedSku != null) {
          return "analytics";
        } else {
          return "getSkus";
        }
      default:
        console.log("unsupported")
        return;
    }
  }

  function getSubmitButtonName() {
    switch (activeTab) {
      case 0:
        if (allSkusFlag === true || choosedSku != null) {
          return "Получить прогноз";
        } else {
          return "Получить список продуктов";
        }
      case 1:
        if (allSkusFlag === true || choosedCluster != null) {
          return "Получить прогноз по категории";
        } else {
          return "Получить список категорий";
        }
      case 2:
        if (allSkusFlag === true || choosedSku != null) {
          return "Получить аналитику";
        } else {
          return "Получить список продуктов";
        }
      default:
        console.log("unsupported")
        return;
    }
  }



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
          {activeTab != 1 &&
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
            </div>}

          {activeTab != 1 && files.length > 0 && (<div>
            <h3>Выбранные файлы:</h3>
            <ul className='files-list'>
              {files.map((file, index) => (
                <li key={index}>{file.name} <button className="remove-file" type="button" onClick={() => removeFile(index)}>Удалить файл</button></li>
              ))}
            </ul>
          </div>)}

          {/* {files.length > 0 && activeTab == 2 &&
            (<h3>Аналитика по всем продуктам:</h3>)}
          {files.length > 0 && activeTab == 2 &&
            <select className='predict-period'
              id="predictionPeriod"
              value={allSkusFlag}
              onChange={(e) => { setAllSkusFlag(e.target.value === "true"); }}
            >
              <option value={true}>Да</option>
              <option value={false}>Нет</option>
            </select>} */}

          {!error && !isLoading && loaded && files.length > 0 && tabsWithSkusFlag.includes(activeTab) && !allSkusFlag &&
            (<h3>Выберите продукт:</h3>)}
          {!error && activeTab == 1 && clusters &&
            (<h3>Выберите категорию:</h3>)}

          {!error && !isLoading && loaded && files.length > 0 && tabsWithSkusFlag.includes(activeTab) && !allSkusFlag && skus &&
            <SkusSearchDisplay data={skus} onSelect={setChoosedSku} />}

          {!error && clusters && activeTab == 1 &&
            <SkusSearchDisplay data={clusters} onSelect={setChoosedCluster} mode="cluster" />}


          {choosedSku && !allSkusFlag && <h3>Выбранный продукт: {choosedSku}</h3>}
          {choosedCluster && <h3>Выбранная категория: {choosedCluster}</h3>}

          {/* {files.length > 0 && activeTab < 2 &&
            (<h3>Выберите период прогноза:</h3>)}
          {files.length > 0 && activeTab < 2 &&
            (<select className='predict-period'
              id="predictionPeriod"
              value={predictionPeriod}
              onChange={(e) => setPredictionPeriod(e.target.value)}
            >
              <option value="1">1 день</option>
              <option value="7">1 неделя</option>
              <option value="30">1 месяц</option>
            </select>)} */}

          {((activeTab == 1) || (files.length > 0 && predictionPeriod)) && (<button className="upload-button" type="submit">{submitButtonName}</button>)}
        </form>
      </div>

      {isLoading && <p>Загрузка ...</p>}

      {message && <p>{message}</p>}
      {!error && loaded && plots && console.log(plots)}

      {!error && !isLoading && activeTab == 2 && loaded && parameters &&
        (<div className="container">
          <h2 className="heading">Отчёт</h2>
          <ParametersDisplay data={parameters} />
        </div>)}

      {!error && !isLoading && loaded && plots &&
        plots.map((plot, index) => (
          <div key={index} style={{ margin: '15px 0' }}>
            <Plot
              key={index}
              data={plot.data}
              layout={plot.layout}
              config={{ responsive: true }}
            />
         </div>))

      }
    </div>
  );
}

export default App;