import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';


function App() {
  const [files, setFiles] = useState([]);
  const [drag, setDrag] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(true);
  const [message, setMessage] = useState("");
  const [plotdata, setPlotdata] = useState(null);
  const [submit, setSubmit] = useState(false);

  const handleFileChange = (event) => {
    event.preventDefault();
    let files = [...event.dataTransfer.files];
    console.log(files);
    setFiles(files);
    setDrag(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    //files.forEach((file) => {
    console.log(files[0]);
    formData.append('file', files[0]);
    //});

    try {
      setIsLoading(true)
      const response = await axios.post("http://localhost:8000/uploadfile/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setError(false);
      setMessage(response.data.message);
      setPlotdata(response.data.plotdata);
      console.log(response);
      console.log(response.data);
      console.log(response.data.message);
      console.log(response.data.plotdata);
    } catch (error) {
      console.error("Error uploading file:", error);
      setError(true);
      setMessage("Error uploading file");
    } finally {
      setIsLoading(false);
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


  return (
    <div className="App">
      <h1>Upload a CSV File</h1>
      <form onSubmit={handleSubmit}>
        <div className='drop-area'>
          {drag
            ? <div className='files-down'
              onDragStart={e => dragStartHandler(e)}
              onDragLeave={e => dragLeaveHandler(e)}
              onDragOver={e => dragStartHandler(e)}
              onDrop={e => handleFileChange(e)}
            > <p>Отпустите файлы, чтобы загрузить </p></div>
            : <div className='files-up'
              onDragStart={e => dragStartHandler(e)}
              onDragLeave={e => dragLeaveHandler(e)}
              onDragOver={e => dragStartHandler(e)}
            > <p>Переместите файлы, чтобы загрузить </p></div>
          }
        </div>
        
        {files.length > 0 && (<div>
          <h2>Выбранные файлы:</h2>
          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name} <button className="remove-file" type="button" onClick={() => removeFile(index)}>Удалить файл</button></li> 
            ))}
          </ul>
        </div>)}
        {files.length > 0 && (<button className="upload-button" type="submit" onClick={e => setSubmit(true)}>Upload files</button>)}
      </form>

      {isLoading && <p>Загрузка ...</p>}
      {error && submit && !isLoading && <p>Ошибка!!!</p>}
      {message && <p>{message}</p>}
      {plotdata && console.log(plotdata.data)}
      {
        !error && !isLoading && submit &&
        <Plot
          data={
            [
              plotdata.data,
              plotdata.prediction
            ]
          }

        />
      }
    </div>
  );
}

export default App;